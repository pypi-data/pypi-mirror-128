# Generated from /home/mario/Documents/PYTHON/chessEngines/parser/gen/pgn.g4 by ANTLR 4.9.2
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\24")
        buf.write("d\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16")
        buf.write("\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23\t\23")
        buf.write("\3\2\3\2\3\3\3\3\3\4\3\4\3\5\3\5\3\6\3\6\3\7\3\7\3\b\3")
        buf.write("\b\3\t\3\t\3\t\3\t\3\n\3\n\3\n\3\n\3\n\3\n\3\13\3\13\3")
        buf.write("\f\3\f\3\r\3\r\3\16\3\16\3\17\6\17I\n\17\r\17\16\17J\3")
        buf.write("\20\3\20\3\20\3\20\3\20\3\20\3\20\3\20\3\20\3\20\3\20")
        buf.write("\3\20\3\20\5\20Z\n\20\3\21\6\21]\n\21\r\21\16\21^\3\22")
        buf.write("\3\22\3\23\3\23\2\2\24\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21")
        buf.write("\n\23\13\25\f\27\r\31\16\33\17\35\20\37\21!\22#\23%\24")
        buf.write("\3\2\t\3\2cj\3\2\63:\6\2DDMMPPST\6\2##%%--AA\3\2\62;\4")
        buf.write("\2C\\c|\5\2\13\f\17\17\"\"\2g\2\3\3\2\2\2\2\5\3\2\2\2")
        buf.write("\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17")
        buf.write("\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2\25\3\2\2\2\2\27\3")
        buf.write("\2\2\2\2\31\3\2\2\2\2\33\3\2\2\2\2\35\3\2\2\2\2\37\3\2")
        buf.write("\2\2\2!\3\2\2\2\2#\3\2\2\2\2%\3\2\2\2\3\'\3\2\2\2\5)\3")
        buf.write("\2\2\2\7+\3\2\2\2\t-\3\2\2\2\13/\3\2\2\2\r\61\3\2\2\2")
        buf.write("\17\63\3\2\2\2\21\65\3\2\2\2\239\3\2\2\2\25?\3\2\2\2\27")
        buf.write("A\3\2\2\2\31C\3\2\2\2\33E\3\2\2\2\35H\3\2\2\2\37Y\3\2")
        buf.write("\2\2!\\\3\2\2\2#`\3\2\2\2%b\3\2\2\2\'(\7$\2\2(\4\3\2\2")
        buf.write("\2)*\7}\2\2*\6\3\2\2\2+,\7\177\2\2,\b\3\2\2\2-.\7]\2\2")
        buf.write(".\n\3\2\2\2/\60\7_\2\2\60\f\3\2\2\2\61\62\7z\2\2\62\16")
        buf.write("\3\2\2\2\63\64\7?\2\2\64\20\3\2\2\2\65\66\7Q\2\2\66\67")
        buf.write("\7/\2\2\678\7Q\2\28\22\3\2\2\29:\7Q\2\2:;\7/\2\2;<\7Q")
        buf.write("\2\2<=\7/\2\2=>\7Q\2\2>\24\3\2\2\2?@\7\60\2\2@\26\3\2")
        buf.write("\2\2AB\t\2\2\2B\30\3\2\2\2CD\t\3\2\2D\32\3\2\2\2EF\t\4")
        buf.write("\2\2F\34\3\2\2\2GI\t\5\2\2HG\3\2\2\2IJ\3\2\2\2JH\3\2\2")
        buf.write("\2JK\3\2\2\2K\36\3\2\2\2LM\7\63\2\2MN\7/\2\2NZ\7\62\2")
        buf.write("\2OP\7\62\2\2PQ\7/\2\2QZ\7\63\2\2RS\7\63\2\2ST\7\61\2")
        buf.write("\2TU\7\64\2\2UV\7/\2\2VW\7\63\2\2WX\7\61\2\2XZ\7\64\2")
        buf.write("\2YL\3\2\2\2YO\3\2\2\2YR\3\2\2\2Z \3\2\2\2[]\t\6\2\2\\")
        buf.write("[\3\2\2\2]^\3\2\2\2^\\\3\2\2\2^_\3\2\2\2_\"\3\2\2\2`a")
        buf.write("\t\7\2\2a$\3\2\2\2bc\t\b\2\2c&\3\2\2\2\6\2JY^\2")
        return buf.getvalue()


class pgnLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    T__4 = 5
    T__5 = 6
    T__6 = 7
    T__7 = 8
    T__8 = 9
    T__9 = 10
    FILE = 11
    RANK = 12
    PIECE = 13
    GLYPH = 14
    RESULT = 15
    INT = 16
    CHAR = 17
    WS = 18

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'\"'", "'{'", "'}'", "'['", "']'", "'x'", "'='", "'O-O'", "'O-O-O'", 
            "'.'" ]

    symbolicNames = [ "<INVALID>",
            "FILE", "RANK", "PIECE", "GLYPH", "RESULT", "INT", "CHAR", "WS" ]

    ruleNames = [ "T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "T__6", 
                  "T__7", "T__8", "T__9", "FILE", "RANK", "PIECE", "GLYPH", 
                  "RESULT", "INT", "CHAR", "WS" ]

    grammarFileName = "pgn.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


    tags = {}
    moves = []


