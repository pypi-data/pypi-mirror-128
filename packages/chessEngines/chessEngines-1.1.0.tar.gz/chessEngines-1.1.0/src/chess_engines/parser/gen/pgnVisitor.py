# Generated from /home/mario/Documents/PYTHON/chessEngines/parser/gen/pgn.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .pgnParser import pgnParser
else:
    from pgnParser import pgnParser

# This class defines a complete generic visitor for a parse tree produced by pgnParser.

class pgnVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by pgnParser#string.
    def visitString(self, ctx:pgnParser.StringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pgnParser#comment.
    def visitComment(self, ctx:pgnParser.CommentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pgnParser#tag.
    def visitTag(self, ctx:pgnParser.TagContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pgnParser#square.
    def visitSquare(self, ctx:pgnParser.SquareContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pgnParser#piece.
    def visitPiece(self, ctx:pgnParser.PieceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pgnParser#halfMove.
    def visitHalfMove(self, ctx:pgnParser.HalfMoveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pgnParser#fullMove.
    def visitFullMove(self, ctx:pgnParser.FullMoveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pgnParser#game.
    def visitGame(self, ctx:pgnParser.GameContext):
        return self.visitChildren(ctx)



del pgnParser