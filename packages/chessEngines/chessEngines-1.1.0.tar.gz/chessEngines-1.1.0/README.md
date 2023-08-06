# chessEngines

This project is a wrapper for chess engines supporting the UCI protocol.
It allows you to create a connection to a compiled chess engine and communicate
with it. By default, the following engines are distributed with this project:

- Stockfish
- Leela Chess Zero

These distributions can be found under /Engines. The distributions are original and no
changes have been made.


## Usage

In the following we will connect to the default distribution of Stockfish
and find the best move in a set position:

```Python
from chess_engines import engines


# called each time stockfish finds a potential 'best move'
def on_move_found(move):
  print(move)
  

# load Stockfish
sf = engines.Stockfish()
# set starting position
sf.play_moves_san('1. e4 e5 2. Nf3 Nc6 3. Bc4')
# find the best move within 2 seconds
best_move = sf.best_move_san(max_secs=2, callback=on_move_found)

print(f'Best move: {best_move}')
```
