import os.path
import re
import subprocess
import threading
import time
from typing import Union, List, Dict, Any, Callable

import chess

from chess_engines.parser import parser

_engines_path = 'Engines'


class UciProtocol:
    """
    This class represents a UCI protocol. Via this class, it is possible
    to communicate with an engine that supports this protocol. The
    constructor requires an executable in order to establish a communication
    with the engine. This communication can be used with the 'cmd' method.
    """

    def __init__(self, exe: str = None):
        """
        Establishes a communication with a chess engine that supports the UCI
        protocol. This connection is available under the attribute 'process'.

        :param exe:
            The path to the engine's executable
        """
        self.process: Union[subprocess.Popen, None] = None
        if exe is not None:
            self.process = subprocess.Popen(exe, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def cmd(self, command: str, delay: float = 0, callback: Callable[[str], None] = None) -> str:
        """
        Sends a command to the engine. After that, the output stream is
        read until the engine sends the command 'readyok'. The total output
        is then returned as a string.

        :param command:
            The command to send to the engine

        :param delay:
            The seconds to wait after the command has been sent

        :param callback:
            A function that is called each time the engine prints
            something to the output stream. The only argument of
            the function is a string (the line that was printed).

        :return:
            The engine's output as a string
        """
        self.process.stdin.write(f'{command}\n'.encode())
        self.process.stdin.flush()
        time.sleep(delay)

        tmp = []
        if command != 'quit':
            self.process.stdin.write('isready\n'.encode())
            self.process.stdin.flush()
            while True:
                text = self.process.stdout.readline().strip()
                if callback is not None:
                    callback(str(text))
                if text == 'readyok'.encode():
                    break
                elif text != ''.encode():
                    tmp.append(str(text))
        else:
            tmp.append('readyok')

        return '\n'.join(tmp)


class Engine(UciProtocol):
    """
    This class represents a chess engine. Note that this
    is not an implementation of a chess engine, but an abstract
    class which should be extended by implementations.
    """

    def __init__(self, exe: str = None, fen: str = None, props: Dict[str, Any] = None):
        """
        Initializes this engine with the given FEN position. If no
        position is specified, the position is set to the starting
        chess position.

        :param exe:
            The path to the engine's executable

        :param fen:
            The FEN representation of the position

        :param props:
            The properties of this engine
        """
        super().__init__(exe)

        self.fen: str = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
        if fen is not None:
            self.fen = fen

        self.props: Dict[str, Any] = props
        if props is None:
            self.props = {}

    def __del__(self):
        """
        Kills the current process and closes the connection to
        the engine permanently.
        """
        if self.process is not None:
            self.cmd('quit')
            self.process.terminate()

    def __enter__(self):
        """
        Enters the 'with' statement.
        :return: self
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exits the 'with' statement. Delegates to '__del__()'.
        """
        self.__del__()

    def ascii(self) -> str:
        """
        Returns an ASCII representation of the current FEN position.

        :return:
            The ASCII representation of the current FEN position
        """
        return chess.Board(self.fen).__str__()

    def play_moves_san(self, moves: Union[List[str], str]):
        """
        Plays a series of moves in SAN notation on the board. No additional actions are taken
        by the engine: This method is meant to update the position only.

        :param moves:
            Either a list of SAN moves (e.g. ['e4', 'e5', 'Nf3', 'Nc6']) or a
            string that represents the moves (e.g. '1. e4 e5 2. Nf3 Nc6'),
            though the former is faster.
        """
        if isinstance(moves, str):
            # parse moves if necessary
            tmp = parser.PgnParser(moves).moves
            moves = []
            for turn in tmp:
                for move in turn:
                    moves.append(move['move'])

        board = chess.Board(self.fen)
        for move in moves:
            if move is not None:
                board.push_san(move)
        self.fen = board.fen()

    def play_moves_uci(self, moves: List[str]):
        """
        Plays a series of moves in UCI notation on the board. No additional actions are taken
        by the engine: This method is meant to update the position only.

        :param moves:
            A list of UCI moves (e.g. ['e2e4', 'e7e5', 'g1f3', 'b8f6'])
        """
        board = chess.Board(self.fen)
        for move in moves:
            board.push_uci(move)
        self.fen = board.fen()

    def apply_props(self):
        """
        Applies all props to the engine. Possible props may
        include: Hash table size, FEN position, openings database,
        etc.
        """
        self.cmd('uci')
        self.cmd(f'position fen {self.fen}')

    def best_move_uci(self, max_secs: float = 0, callback: Callable[[str], None] = None) -> str:
        """
        Finds the best move in the current position. The move is
        returned in UCI notation.

        :param max_secs:
            Maximum time to think about the current position

        :param callback:
            A function that is called each time the engine finds a potential
            'best move'. The function accepts a string as an argument (the move
            in UCI notation). Therefore, the last call of this function is called
            with the best move found.

        :return:
            The best move in UCI notation.
        """
        x = ''
        thinking = True

        # called after each line read
        def _call(line):
            m = re.findall('pv [a-h][1-8][a-h][1-8][qrnb]?', line)
            if len(m) > 0:
                nonlocal x
                u = m[-1][3:]
                x = u
                if callback is not None:
                    callback(u)

        # stop thinking after timer runs out
        def _timer():
            nonlocal thinking
            self.process.stdin.write('isready\n'.encode())
            self.process.stdin.flush()
            thinking = False

        self.apply_props()

        #######################
        # start finding moves #
        #######################

        self.process.stdin.write('go ponder\n'.encode())
        self.process.stdin.flush()
        threading.Timer(max_secs, _timer).start()

        while True:
            text = str(self.process.stdout.readline().strip())
            _call(text)
            if not thinking or 'bestmove' in text or 'readyok' in text:
                break

        ########################
        # stopped finding moves
        ########################

        self.cmd('stop')

        return x

    def best_move_san(self, max_secs: float = 0, callback: Callable[[str], None] = None) -> str:
        """
        Finds the best move in the current position. The move is
        returned in SAN notation. Note that this method a wrapper
        for Engine.best_move_uci().

        :param max_secs:
            Maximum time to think about the current position

        :param callback:
            A function that is called each time the engine finds a potential
            'best move'. The function accepts a string as an argument (the move
            in SAN notation). Therefore, the last call of this function is called
            with the best move found.

        :return:
            The best move in SAN notation.
        """

        def _call(m):
            if callback is not None:
                callback(chess.Board(self.fen).san(chess.Move.from_uci(m)))

        uci = self.best_move_uci(max_secs, callback=_call)
        board = chess.Board(self.fen)
        move = chess.Move.from_uci(uci)
        return board.san(move)


class Stockfish(Engine):
    """
    This class is an implementation of Stockfish.
    """

    def __init__(self, exe: str = None, fen: str = None, props: Dict[str, Any] = None):
        """
        Connects to the Stockfish executable. By default, Stockfish 14.1 is used,
        if no executable is specified.

        :param exe:
            The Stockfish executable (default: sf-v.14.1)

        :param fen:
            The FEN position of the board (default: starting position)

        :param props:
            Optional properties for Stockfish
        """
        if exe is None:
            exe = _engines_path + '/Stockfish/Stockfish-sf_14.1/src/stockfish'
        super().__init__(exe, fen, props)


class Leela(Engine):
    """
    This class is an implementation for Leela Chess Zero (lc0).
    """

    def __init__(self, exe: str = None, fen: str = None, props: Dict[str, Any] = None):
        """
        Connects to the Leela Chess Zero executable. If no executable is specified, a
        default version is used instead.

        :param exe:
            The lc0 executable

        :param fen:
            The FEN position of the board (default: starting position)

        :param props:
            Optionals properties for lc0
        """
        if exe is None:
            exe = _engines_path + '/Leela/lc0-master/build/release/lc0'
        super().__init__(exe, fen, props)
