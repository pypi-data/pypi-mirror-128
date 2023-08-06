from typing import List

import antlr4

import json

from chess_engines.parser.gen import pgnLexer as _lexer, pgnParser as _parser


def moves_to_string(moves: List[str], color: str = 'w', turn: int = 1) -> str:
    """
    Converts the given moves to a string. Example:

    ['e4', 'e5', 'Nf3', 'Nc6'] -> '1. e4 e5 2. Nf3 Nc6'

    :param moves:
        A list containing the moves to convert

    :param color:
        The color to start with (either 'w' or 'b')

    :param turn:
        The turn to start with
    """
    i = 0
    tmp = []
    _moves = moves[:]
    if color == 'b':
        tmp.append(f'{i + turn}..{_moves[0]} ')
        _moves.pop(0)
        i += 1

    for (j, move) in enumerate(_moves):
        if j % 2 == 0:
            tmp.append(f'{i + turn}. {move} ')
            i += 1
        else:
            tmp.append(f'{move} ')

    return ''.join(tmp)[:-1]


class PgnParser:
    """
    This class is an ANTLR4 parser for PGNs. It is possible to read
    and extract information from PGN chess games.
    """

    def __init__(self, pgn: str = None):
        """
        Creates a PGN parser and parses given pgn.
        By default, no pgn is set.
        """
        self.tags = {}
        self.moves = []
        if pgn is not None:
            self.parse_pgn(pgn)

    def parse_pgn(self, pgn: str):
        """
        Parses the given pgn (if given). The result is saved under the attributes
        'tags' (Dict[str, str]) and 'moves' (List[Dict[str, str]).
        The tags are a dictionary that maps each tag to its corresponding
        value, e.g.:

        {
            'White': 'Bobby Fischer',
            'Opening': 'Sicilian Defence'
        }

        The moves are a list of dictionaries with the following properties:

        [
            {
                'move': 'e4',
                'glyph': None,
                'comment: None,
            },
            {
                'move': 'a6',
                'glyph': '?!',
                'comment': 'This is not a good move'
            }
        ]

        """
        pgn_ = antlr4.InputStream(pgn)
        lexer = _lexer.pgnLexer(pgn_)
        stream = antlr4.CommonTokenStream(lexer)
        parser = _parser.pgnParser(stream)
        parser.game()
        self.tags = parser.tags
        self.moves = parser.moves

    def json(self, pgn: str = None) -> str:
        """
        Parses the given pgn (if given) and returns the JSON representation
        of this object as a string.

        :return:
            The JSON representation of this object as a string.
        """
        if pgn is not None:
            self.parse_pgn(pgn)
        return json.dumps({
            'tags': self.tags,
            'moves': self.moves
        }, indent=4)
