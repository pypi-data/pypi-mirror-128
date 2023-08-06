# Generated from /home/mario/Documents/PYTHON/chessEngines/parser/gen/pgn.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .pgnParser import pgnParser
else:
    from pgnParser import pgnParser

# This class defines a complete listener for a parse tree produced by pgnParser.
class pgnListener(ParseTreeListener):

    # Enter a parse tree produced by pgnParser#string.
    def enterString(self, ctx:pgnParser.StringContext):
        pass

    # Exit a parse tree produced by pgnParser#string.
    def exitString(self, ctx:pgnParser.StringContext):
        pass


    # Enter a parse tree produced by pgnParser#comment.
    def enterComment(self, ctx:pgnParser.CommentContext):
        pass

    # Exit a parse tree produced by pgnParser#comment.
    def exitComment(self, ctx:pgnParser.CommentContext):
        pass


    # Enter a parse tree produced by pgnParser#tag.
    def enterTag(self, ctx:pgnParser.TagContext):
        pass

    # Exit a parse tree produced by pgnParser#tag.
    def exitTag(self, ctx:pgnParser.TagContext):
        pass


    # Enter a parse tree produced by pgnParser#square.
    def enterSquare(self, ctx:pgnParser.SquareContext):
        pass

    # Exit a parse tree produced by pgnParser#square.
    def exitSquare(self, ctx:pgnParser.SquareContext):
        pass


    # Enter a parse tree produced by pgnParser#piece.
    def enterPiece(self, ctx:pgnParser.PieceContext):
        pass

    # Exit a parse tree produced by pgnParser#piece.
    def exitPiece(self, ctx:pgnParser.PieceContext):
        pass


    # Enter a parse tree produced by pgnParser#halfMove.
    def enterHalfMove(self, ctx:pgnParser.HalfMoveContext):
        pass

    # Exit a parse tree produced by pgnParser#halfMove.
    def exitHalfMove(self, ctx:pgnParser.HalfMoveContext):
        pass


    # Enter a parse tree produced by pgnParser#fullMove.
    def enterFullMove(self, ctx:pgnParser.FullMoveContext):
        pass

    # Exit a parse tree produced by pgnParser#fullMove.
    def exitFullMove(self, ctx:pgnParser.FullMoveContext):
        pass


    # Enter a parse tree produced by pgnParser#game.
    def enterGame(self, ctx:pgnParser.GameContext):
        pass

    # Exit a parse tree produced by pgnParser#game.
    def exitGame(self, ctx:pgnParser.GameContext):
        pass



del pgnParser