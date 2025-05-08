# Generated from grammar/MiniC.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,37,251,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,
        1,0,5,0,56,8,0,10,0,12,0,59,9,0,1,0,1,0,1,1,1,1,3,1,65,8,1,1,2,1,
        2,1,2,1,2,3,2,71,8,2,1,2,1,2,1,3,1,3,1,4,1,4,1,4,1,4,3,4,81,8,4,
        1,4,1,4,1,4,1,5,1,5,1,5,5,5,89,8,5,10,5,12,5,92,9,5,1,6,1,6,1,6,
        1,7,1,7,5,7,99,8,7,10,7,12,7,102,9,7,1,7,1,7,1,8,1,8,1,8,1,8,1,8,
        1,8,1,8,1,8,3,8,114,8,8,1,9,1,9,1,9,1,10,1,10,1,10,1,10,1,10,1,10,
        1,10,3,10,126,8,10,1,11,1,11,1,11,1,11,1,11,1,11,1,12,1,12,1,12,
        1,12,3,12,138,8,12,1,12,3,12,141,8,12,1,12,3,12,144,8,12,1,12,1,
        12,1,12,3,12,149,8,12,1,12,1,12,1,12,1,12,1,13,1,13,3,13,157,8,13,
        1,13,1,13,1,14,1,14,1,15,1,15,1,15,3,15,166,8,15,1,16,1,16,1,16,
        5,16,171,8,16,10,16,12,16,174,9,16,1,17,1,17,1,17,5,17,179,8,17,
        10,17,12,17,182,9,17,1,18,1,18,1,18,5,18,187,8,18,10,18,12,18,190,
        9,18,1,19,1,19,1,19,5,19,195,8,19,10,19,12,19,198,9,19,1,20,1,20,
        1,20,5,20,203,8,20,10,20,12,20,206,9,20,1,21,1,21,1,21,5,21,211,
        8,21,10,21,12,21,214,9,21,1,22,1,22,1,22,1,22,1,22,1,22,1,22,3,22,
        223,8,22,1,23,1,23,1,23,1,23,1,23,1,23,1,23,3,23,232,8,23,1,24,1,
        24,1,24,3,24,237,8,24,1,24,1,24,1,25,1,25,1,25,5,25,244,8,25,10,
        25,12,25,247,9,25,1,26,1,26,1,26,0,0,27,0,2,4,6,8,10,12,14,16,18,
        20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,0,6,1,0,6,8,2,
        0,23,23,26,26,2,0,21,22,24,25,1,0,30,31,1,0,32,34,2,0,9,9,11,13,
        257,0,57,1,0,0,0,2,64,1,0,0,0,4,66,1,0,0,0,6,74,1,0,0,0,8,76,1,0,
        0,0,10,85,1,0,0,0,12,93,1,0,0,0,14,96,1,0,0,0,16,113,1,0,0,0,18,
        115,1,0,0,0,20,118,1,0,0,0,22,127,1,0,0,0,24,133,1,0,0,0,26,154,
        1,0,0,0,28,160,1,0,0,0,30,162,1,0,0,0,32,167,1,0,0,0,34,175,1,0,
        0,0,36,183,1,0,0,0,38,191,1,0,0,0,40,199,1,0,0,0,42,207,1,0,0,0,
        44,222,1,0,0,0,46,231,1,0,0,0,48,233,1,0,0,0,50,240,1,0,0,0,52,248,
        1,0,0,0,54,56,3,2,1,0,55,54,1,0,0,0,56,59,1,0,0,0,57,55,1,0,0,0,
        57,58,1,0,0,0,58,60,1,0,0,0,59,57,1,0,0,0,60,61,5,0,0,1,61,1,1,0,
        0,0,62,65,3,4,2,0,63,65,3,8,4,0,64,62,1,0,0,0,64,63,1,0,0,0,65,3,
        1,0,0,0,66,67,3,6,3,0,67,70,5,10,0,0,68,69,5,20,0,0,69,71,3,28,14,
        0,70,68,1,0,0,0,70,71,1,0,0,0,71,72,1,0,0,0,72,73,5,18,0,0,73,5,
        1,0,0,0,74,75,7,0,0,0,75,7,1,0,0,0,76,77,3,6,3,0,77,78,5,10,0,0,
        78,80,5,14,0,0,79,81,3,10,5,0,80,79,1,0,0,0,80,81,1,0,0,0,81,82,
        1,0,0,0,82,83,5,15,0,0,83,84,3,14,7,0,84,9,1,0,0,0,85,90,3,12,6,
        0,86,87,5,19,0,0,87,89,3,12,6,0,88,86,1,0,0,0,89,92,1,0,0,0,90,88,
        1,0,0,0,90,91,1,0,0,0,91,11,1,0,0,0,92,90,1,0,0,0,93,94,3,6,3,0,
        94,95,5,10,0,0,95,13,1,0,0,0,96,100,5,16,0,0,97,99,3,16,8,0,98,97,
        1,0,0,0,99,102,1,0,0,0,100,98,1,0,0,0,100,101,1,0,0,0,101,103,1,
        0,0,0,102,100,1,0,0,0,103,104,5,17,0,0,104,15,1,0,0,0,105,114,3,
        4,2,0,106,114,3,18,9,0,107,114,3,20,10,0,108,114,3,22,11,0,109,114,
        3,24,12,0,110,114,3,26,13,0,111,114,3,14,7,0,112,114,5,18,0,0,113,
        105,1,0,0,0,113,106,1,0,0,0,113,107,1,0,0,0,113,108,1,0,0,0,113,
        109,1,0,0,0,113,110,1,0,0,0,113,111,1,0,0,0,113,112,1,0,0,0,114,
        17,1,0,0,0,115,116,3,28,14,0,116,117,5,18,0,0,117,19,1,0,0,0,118,
        119,5,1,0,0,119,120,5,14,0,0,120,121,3,28,14,0,121,122,5,15,0,0,
        122,125,3,16,8,0,123,124,5,2,0,0,124,126,3,16,8,0,125,123,1,0,0,
        0,125,126,1,0,0,0,126,21,1,0,0,0,127,128,5,3,0,0,128,129,5,14,0,
        0,129,130,3,28,14,0,130,131,5,15,0,0,131,132,3,16,8,0,132,23,1,0,
        0,0,133,134,5,4,0,0,134,140,5,14,0,0,135,141,3,4,2,0,136,138,3,28,
        14,0,137,136,1,0,0,0,137,138,1,0,0,0,138,139,1,0,0,0,139,141,5,18,
        0,0,140,135,1,0,0,0,140,137,1,0,0,0,141,143,1,0,0,0,142,144,3,28,
        14,0,143,142,1,0,0,0,143,144,1,0,0,0,144,145,1,0,0,0,145,146,5,18,
        0,0,146,148,1,0,0,0,147,149,3,28,14,0,148,147,1,0,0,0,148,149,1,
        0,0,0,149,150,1,0,0,0,150,151,5,15,0,0,151,152,1,0,0,0,152,153,3,
        16,8,0,153,25,1,0,0,0,154,156,5,5,0,0,155,157,3,28,14,0,156,155,
        1,0,0,0,156,157,1,0,0,0,157,158,1,0,0,0,158,159,5,18,0,0,159,27,
        1,0,0,0,160,161,3,30,15,0,161,29,1,0,0,0,162,165,3,32,16,0,163,164,
        5,20,0,0,164,166,3,30,15,0,165,163,1,0,0,0,165,166,1,0,0,0,166,31,
        1,0,0,0,167,172,3,34,17,0,168,169,5,28,0,0,169,171,3,34,17,0,170,
        168,1,0,0,0,171,174,1,0,0,0,172,170,1,0,0,0,172,173,1,0,0,0,173,
        33,1,0,0,0,174,172,1,0,0,0,175,180,3,36,18,0,176,177,5,27,0,0,177,
        179,3,36,18,0,178,176,1,0,0,0,179,182,1,0,0,0,180,178,1,0,0,0,180,
        181,1,0,0,0,181,35,1,0,0,0,182,180,1,0,0,0,183,188,3,38,19,0,184,
        185,7,1,0,0,185,187,3,38,19,0,186,184,1,0,0,0,187,190,1,0,0,0,188,
        186,1,0,0,0,188,189,1,0,0,0,189,37,1,0,0,0,190,188,1,0,0,0,191,196,
        3,40,20,0,192,193,7,2,0,0,193,195,3,40,20,0,194,192,1,0,0,0,195,
        198,1,0,0,0,196,194,1,0,0,0,196,197,1,0,0,0,197,39,1,0,0,0,198,196,
        1,0,0,0,199,204,3,42,21,0,200,201,7,3,0,0,201,203,3,42,21,0,202,
        200,1,0,0,0,203,206,1,0,0,0,204,202,1,0,0,0,204,205,1,0,0,0,205,
        41,1,0,0,0,206,204,1,0,0,0,207,212,3,44,22,0,208,209,7,4,0,0,209,
        211,3,44,22,0,210,208,1,0,0,0,211,214,1,0,0,0,212,210,1,0,0,0,212,
        213,1,0,0,0,213,43,1,0,0,0,214,212,1,0,0,0,215,216,5,30,0,0,216,
        223,3,44,22,0,217,218,5,31,0,0,218,223,3,44,22,0,219,220,5,29,0,
        0,220,223,3,44,22,0,221,223,3,46,23,0,222,215,1,0,0,0,222,217,1,
        0,0,0,222,219,1,0,0,0,222,221,1,0,0,0,223,45,1,0,0,0,224,232,5,10,
        0,0,225,232,3,52,26,0,226,227,5,14,0,0,227,228,3,28,14,0,228,229,
        5,15,0,0,229,232,1,0,0,0,230,232,3,48,24,0,231,224,1,0,0,0,231,225,
        1,0,0,0,231,226,1,0,0,0,231,230,1,0,0,0,232,47,1,0,0,0,233,234,5,
        10,0,0,234,236,5,14,0,0,235,237,3,50,25,0,236,235,1,0,0,0,236,237,
        1,0,0,0,237,238,1,0,0,0,238,239,5,15,0,0,239,49,1,0,0,0,240,245,
        3,28,14,0,241,242,5,19,0,0,242,244,3,28,14,0,243,241,1,0,0,0,244,
        247,1,0,0,0,245,243,1,0,0,0,245,246,1,0,0,0,246,51,1,0,0,0,247,245,
        1,0,0,0,248,249,7,5,0,0,249,53,1,0,0,0,24,57,64,70,80,90,100,113,
        125,137,140,143,148,156,165,172,180,188,196,204,212,222,231,236,
        245
    ]

class MiniCParser ( Parser ):

    grammarFileName = "MiniC.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'if'", "'else'", "'while'", "'for'", 
                     "'return'", "'int'", "'char'", "'bool'", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "'('", "')'", "'{'", "'}'", "';'", "','", "'='", "'>'", 
                     "'<'", "'=='", "'<='", "'>='", "'!='", "'&&'", "'||'", 
                     "'!'", "'+'", "'-'", "'*'", "'/'", "'%'" ]

    symbolicNames = [ "<INVALID>", "IF", "ELSE", "WHILE", "FOR", "RETURN", 
                      "INT", "CHAR", "BOOL", "BOOL_LITERAL", "IDENTIFIER", 
                      "INT_LITERAL", "CHAR_LITERAL", "STRING_LITERAL", "LPAREN", 
                      "RPAREN", "LBRACE", "RBRACE", "SEMI", "COMMA", "ASSIGN", 
                      "GT", "LT", "EQ", "LTE", "GTE", "NEQ", "AND", "OR", 
                      "NOT", "PLUS", "MINUS", "MUL", "DIV", "MOD", "WS", 
                      "COMMENT", "BLOCK_COMMENT" ]

    RULE_program = 0
    RULE_declaration = 1
    RULE_variableDeclaration = 2
    RULE_typeSpecifier = 3
    RULE_functionDeclaration = 4
    RULE_parameters = 5
    RULE_parameter = 6
    RULE_block = 7
    RULE_statement = 8
    RULE_expressionStatement = 9
    RULE_ifStatement = 10
    RULE_whileStatement = 11
    RULE_forStatement = 12
    RULE_returnStatement = 13
    RULE_expression = 14
    RULE_assignmentExpression = 15
    RULE_logicalOrExpression = 16
    RULE_logicalAndExpression = 17
    RULE_equalityExpression = 18
    RULE_relationalExpression = 19
    RULE_additiveExpression = 20
    RULE_multiplicativeExpression = 21
    RULE_unaryExpression = 22
    RULE_primaryExpression = 23
    RULE_functionCall = 24
    RULE_arguments = 25
    RULE_constant = 26

    ruleNames =  [ "program", "declaration", "variableDeclaration", "typeSpecifier", 
                   "functionDeclaration", "parameters", "parameter", "block", 
                   "statement", "expressionStatement", "ifStatement", "whileStatement", 
                   "forStatement", "returnStatement", "expression", "assignmentExpression", 
                   "logicalOrExpression", "logicalAndExpression", "equalityExpression", 
                   "relationalExpression", "additiveExpression", "multiplicativeExpression", 
                   "unaryExpression", "primaryExpression", "functionCall", 
                   "arguments", "constant" ]

    EOF = Token.EOF
    IF=1
    ELSE=2
    WHILE=3
    FOR=4
    RETURN=5
    INT=6
    CHAR=7
    BOOL=8
    BOOL_LITERAL=9
    IDENTIFIER=10
    INT_LITERAL=11
    CHAR_LITERAL=12
    STRING_LITERAL=13
    LPAREN=14
    RPAREN=15
    LBRACE=16
    RBRACE=17
    SEMI=18
    COMMA=19
    ASSIGN=20
    GT=21
    LT=22
    EQ=23
    LTE=24
    GTE=25
    NEQ=26
    AND=27
    OR=28
    NOT=29
    PLUS=30
    MINUS=31
    MUL=32
    DIV=33
    MOD=34
    WS=35
    COMMENT=36
    BLOCK_COMMENT=37

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(MiniCParser.EOF, 0)

        def declaration(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MiniCParser.DeclarationContext)
            else:
                return self.getTypedRuleContext(MiniCParser.DeclarationContext,i)


        def getRuleIndex(self):
            return MiniCParser.RULE_program

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgram" ):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)




    def program(self):

        localctx = MiniCParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 57
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 448) != 0):
                self.state = 54
                self.declaration()
                self.state = 59
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 60
            self.match(MiniCParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def variableDeclaration(self):
            return self.getTypedRuleContext(MiniCParser.VariableDeclarationContext,0)


        def functionDeclaration(self):
            return self.getTypedRuleContext(MiniCParser.FunctionDeclarationContext,0)


        def getRuleIndex(self):
            return MiniCParser.RULE_declaration

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDeclaration" ):
                return visitor.visitDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def declaration(self):

        localctx = MiniCParser.DeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_declaration)
        try:
            self.state = 64
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 62
                self.variableDeclaration()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 63
                self.functionDeclaration()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VariableDeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def typeSpecifier(self):
            return self.getTypedRuleContext(MiniCParser.TypeSpecifierContext,0)


        def IDENTIFIER(self):
            return self.getToken(MiniCParser.IDENTIFIER, 0)

        def SEMI(self):
            return self.getToken(MiniCParser.SEMI, 0)

        def ASSIGN(self):
            return self.getToken(MiniCParser.ASSIGN, 0)

        def expression(self):
            return self.getTypedRuleContext(MiniCParser.ExpressionContext,0)


        def getRuleIndex(self):
            return MiniCParser.RULE_variableDeclaration

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVariableDeclaration" ):
                return visitor.visitVariableDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def variableDeclaration(self):

        localctx = MiniCParser.VariableDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_variableDeclaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 66
            self.typeSpecifier()
            self.state = 67
            self.match(MiniCParser.IDENTIFIER)
            self.state = 70
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==20:
                self.state = 68
                self.match(MiniCParser.ASSIGN)
                self.state = 69
                self.expression()


            self.state = 72
            self.match(MiniCParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TypeSpecifierContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT(self):
            return self.getToken(MiniCParser.INT, 0)

        def CHAR(self):
            return self.getToken(MiniCParser.CHAR, 0)

        def BOOL(self):
            return self.getToken(MiniCParser.BOOL, 0)

        def getRuleIndex(self):
            return MiniCParser.RULE_typeSpecifier

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTypeSpecifier" ):
                return visitor.visitTypeSpecifier(self)
            else:
                return visitor.visitChildren(self)




    def typeSpecifier(self):

        localctx = MiniCParser.TypeSpecifierContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_typeSpecifier)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 74
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 448) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FunctionDeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def typeSpecifier(self):
            return self.getTypedRuleContext(MiniCParser.TypeSpecifierContext,0)


        def IDENTIFIER(self):
            return self.getToken(MiniCParser.IDENTIFIER, 0)

        def LPAREN(self):
            return self.getToken(MiniCParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(MiniCParser.RPAREN, 0)

        def block(self):
            return self.getTypedRuleContext(MiniCParser.BlockContext,0)


        def parameters(self):
            return self.getTypedRuleContext(MiniCParser.ParametersContext,0)


        def getRuleIndex(self):
            return MiniCParser.RULE_functionDeclaration

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionDeclaration" ):
                return visitor.visitFunctionDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def functionDeclaration(self):

        localctx = MiniCParser.FunctionDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_functionDeclaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 76
            self.typeSpecifier()
            self.state = 77
            self.match(MiniCParser.IDENTIFIER)
            self.state = 78
            self.match(MiniCParser.LPAREN)
            self.state = 80
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 448) != 0):
                self.state = 79
                self.parameters()


            self.state = 82
            self.match(MiniCParser.RPAREN)
            self.state = 83
            self.block()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParametersContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def parameter(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MiniCParser.ParameterContext)
            else:
                return self.getTypedRuleContext(MiniCParser.ParameterContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(MiniCParser.COMMA)
            else:
                return self.getToken(MiniCParser.COMMA, i)

        def getRuleIndex(self):
            return MiniCParser.RULE_parameters

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParameters" ):
                return visitor.visitParameters(self)
            else:
                return visitor.visitChildren(self)




    def parameters(self):

        localctx = MiniCParser.ParametersContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_parameters)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 85
            self.parameter()
            self.state = 90
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==19:
                self.state = 86
                self.match(MiniCParser.COMMA)
                self.state = 87
                self.parameter()
                self.state = 92
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParameterContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def typeSpecifier(self):
            return self.getTypedRuleContext(MiniCParser.TypeSpecifierContext,0)


        def IDENTIFIER(self):
            return self.getToken(MiniCParser.IDENTIFIER, 0)

        def getRuleIndex(self):
            return MiniCParser.RULE_parameter

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParameter" ):
                return visitor.visitParameter(self)
            else:
                return visitor.visitChildren(self)




    def parameter(self):

        localctx = MiniCParser.ParameterContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_parameter)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 93
            self.typeSpecifier()
            self.state = 94
            self.match(MiniCParser.IDENTIFIER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LBRACE(self):
            return self.getToken(MiniCParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(MiniCParser.RBRACE, 0)

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MiniCParser.StatementContext)
            else:
                return self.getTypedRuleContext(MiniCParser.StatementContext,i)


        def getRuleIndex(self):
            return MiniCParser.RULE_block

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBlock" ):
                return visitor.visitBlock(self)
            else:
                return visitor.visitChildren(self)




    def block(self):

        localctx = MiniCParser.BlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_block)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 96
            self.match(MiniCParser.LBRACE)
            self.state = 100
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 3758456826) != 0):
                self.state = 97
                self.statement()
                self.state = 102
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 103
            self.match(MiniCParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def variableDeclaration(self):
            return self.getTypedRuleContext(MiniCParser.VariableDeclarationContext,0)


        def expressionStatement(self):
            return self.getTypedRuleContext(MiniCParser.ExpressionStatementContext,0)


        def ifStatement(self):
            return self.getTypedRuleContext(MiniCParser.IfStatementContext,0)


        def whileStatement(self):
            return self.getTypedRuleContext(MiniCParser.WhileStatementContext,0)


        def forStatement(self):
            return self.getTypedRuleContext(MiniCParser.ForStatementContext,0)


        def returnStatement(self):
            return self.getTypedRuleContext(MiniCParser.ReturnStatementContext,0)


        def block(self):
            return self.getTypedRuleContext(MiniCParser.BlockContext,0)


        def SEMI(self):
            return self.getToken(MiniCParser.SEMI, 0)

        def getRuleIndex(self):
            return MiniCParser.RULE_statement

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStatement" ):
                return visitor.visitStatement(self)
            else:
                return visitor.visitChildren(self)




    def statement(self):

        localctx = MiniCParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_statement)
        try:
            self.state = 113
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [6, 7, 8]:
                self.enterOuterAlt(localctx, 1)
                self.state = 105
                self.variableDeclaration()
                pass
            elif token in [9, 10, 11, 12, 13, 14, 29, 30, 31]:
                self.enterOuterAlt(localctx, 2)
                self.state = 106
                self.expressionStatement()
                pass
            elif token in [1]:
                self.enterOuterAlt(localctx, 3)
                self.state = 107
                self.ifStatement()
                pass
            elif token in [3]:
                self.enterOuterAlt(localctx, 4)
                self.state = 108
                self.whileStatement()
                pass
            elif token in [4]:
                self.enterOuterAlt(localctx, 5)
                self.state = 109
                self.forStatement()
                pass
            elif token in [5]:
                self.enterOuterAlt(localctx, 6)
                self.state = 110
                self.returnStatement()
                pass
            elif token in [16]:
                self.enterOuterAlt(localctx, 7)
                self.state = 111
                self.block()
                pass
            elif token in [18]:
                self.enterOuterAlt(localctx, 8)
                self.state = 112
                self.match(MiniCParser.SEMI)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpressionStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self):
            return self.getTypedRuleContext(MiniCParser.ExpressionContext,0)


        def SEMI(self):
            return self.getToken(MiniCParser.SEMI, 0)

        def getRuleIndex(self):
            return MiniCParser.RULE_expressionStatement

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpressionStatement" ):
                return visitor.visitExpressionStatement(self)
            else:
                return visitor.visitChildren(self)




    def expressionStatement(self):

        localctx = MiniCParser.ExpressionStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_expressionStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 115
            self.expression()
            self.state = 116
            self.match(MiniCParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IfStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IF(self):
            return self.getToken(MiniCParser.IF, 0)

        def LPAREN(self):
            return self.getToken(MiniCParser.LPAREN, 0)

        def expression(self):
            return self.getTypedRuleContext(MiniCParser.ExpressionContext,0)


        def RPAREN(self):
            return self.getToken(MiniCParser.RPAREN, 0)

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MiniCParser.StatementContext)
            else:
                return self.getTypedRuleContext(MiniCParser.StatementContext,i)


        def ELSE(self):
            return self.getToken(MiniCParser.ELSE, 0)

        def getRuleIndex(self):
            return MiniCParser.RULE_ifStatement

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIfStatement" ):
                return visitor.visitIfStatement(self)
            else:
                return visitor.visitChildren(self)




    def ifStatement(self):

        localctx = MiniCParser.IfStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_ifStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 118
            self.match(MiniCParser.IF)
            self.state = 119
            self.match(MiniCParser.LPAREN)
            self.state = 120
            self.expression()
            self.state = 121
            self.match(MiniCParser.RPAREN)
            self.state = 122
            self.statement()
            self.state = 125
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,7,self._ctx)
            if la_ == 1:
                self.state = 123
                self.match(MiniCParser.ELSE)
                self.state = 124
                self.statement()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WhileStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def WHILE(self):
            return self.getToken(MiniCParser.WHILE, 0)

        def LPAREN(self):
            return self.getToken(MiniCParser.LPAREN, 0)

        def expression(self):
            return self.getTypedRuleContext(MiniCParser.ExpressionContext,0)


        def RPAREN(self):
            return self.getToken(MiniCParser.RPAREN, 0)

        def statement(self):
            return self.getTypedRuleContext(MiniCParser.StatementContext,0)


        def getRuleIndex(self):
            return MiniCParser.RULE_whileStatement

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWhileStatement" ):
                return visitor.visitWhileStatement(self)
            else:
                return visitor.visitChildren(self)




    def whileStatement(self):

        localctx = MiniCParser.WhileStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_whileStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 127
            self.match(MiniCParser.WHILE)
            self.state = 128
            self.match(MiniCParser.LPAREN)
            self.state = 129
            self.expression()
            self.state = 130
            self.match(MiniCParser.RPAREN)
            self.state = 131
            self.statement()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ForStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FOR(self):
            return self.getToken(MiniCParser.FOR, 0)

        def LPAREN(self):
            return self.getToken(MiniCParser.LPAREN, 0)

        def statement(self):
            return self.getTypedRuleContext(MiniCParser.StatementContext,0)


        def variableDeclaration(self):
            return self.getTypedRuleContext(MiniCParser.VariableDeclarationContext,0)


        def SEMI(self, i:int=None):
            if i is None:
                return self.getTokens(MiniCParser.SEMI)
            else:
                return self.getToken(MiniCParser.SEMI, i)

        def RPAREN(self):
            return self.getToken(MiniCParser.RPAREN, 0)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MiniCParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(MiniCParser.ExpressionContext,i)


        def getRuleIndex(self):
            return MiniCParser.RULE_forStatement

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitForStatement" ):
                return visitor.visitForStatement(self)
            else:
                return visitor.visitChildren(self)




    def forStatement(self):

        localctx = MiniCParser.ForStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_forStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 133
            self.match(MiniCParser.FOR)
            self.state = 134
            self.match(MiniCParser.LPAREN)
            self.state = 140
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [6, 7, 8]:
                self.state = 135
                self.variableDeclaration()
                pass
            elif token in [9, 10, 11, 12, 13, 14, 18, 29, 30, 31]:
                self.state = 137
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 3758128640) != 0):
                    self.state = 136
                    self.expression()


                self.state = 139
                self.match(MiniCParser.SEMI)
                pass
            else:
                raise NoViableAltException(self)

            self.state = 143
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 3758128640) != 0):
                self.state = 142
                self.expression()


            self.state = 145
            self.match(MiniCParser.SEMI)

            self.state = 148
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 3758128640) != 0):
                self.state = 147
                self.expression()


            self.state = 150
            self.match(MiniCParser.RPAREN)
            self.state = 152
            self.statement()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ReturnStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def RETURN(self):
            return self.getToken(MiniCParser.RETURN, 0)

        def SEMI(self):
            return self.getToken(MiniCParser.SEMI, 0)

        def expression(self):
            return self.getTypedRuleContext(MiniCParser.ExpressionContext,0)


        def getRuleIndex(self):
            return MiniCParser.RULE_returnStatement

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReturnStatement" ):
                return visitor.visitReturnStatement(self)
            else:
                return visitor.visitChildren(self)




    def returnStatement(self):

        localctx = MiniCParser.ReturnStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_returnStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 154
            self.match(MiniCParser.RETURN)
            self.state = 156
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 3758128640) != 0):
                self.state = 155
                self.expression()


            self.state = 158
            self.match(MiniCParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def assignmentExpression(self):
            return self.getTypedRuleContext(MiniCParser.AssignmentExpressionContext,0)


        def getRuleIndex(self):
            return MiniCParser.RULE_expression

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpression" ):
                return visitor.visitExpression(self)
            else:
                return visitor.visitChildren(self)




    def expression(self):

        localctx = MiniCParser.ExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_expression)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 160
            self.assignmentExpression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AssignmentExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def logicalOrExpression(self):
            return self.getTypedRuleContext(MiniCParser.LogicalOrExpressionContext,0)


        def ASSIGN(self):
            return self.getToken(MiniCParser.ASSIGN, 0)

        def assignmentExpression(self):
            return self.getTypedRuleContext(MiniCParser.AssignmentExpressionContext,0)


        def getRuleIndex(self):
            return MiniCParser.RULE_assignmentExpression

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssignmentExpression" ):
                return visitor.visitAssignmentExpression(self)
            else:
                return visitor.visitChildren(self)




    def assignmentExpression(self):

        localctx = MiniCParser.AssignmentExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_assignmentExpression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 162
            self.logicalOrExpression()
            self.state = 165
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==20:
                self.state = 163
                self.match(MiniCParser.ASSIGN)
                self.state = 164
                self.assignmentExpression()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LogicalOrExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def logicalAndExpression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MiniCParser.LogicalAndExpressionContext)
            else:
                return self.getTypedRuleContext(MiniCParser.LogicalAndExpressionContext,i)


        def OR(self, i:int=None):
            if i is None:
                return self.getTokens(MiniCParser.OR)
            else:
                return self.getToken(MiniCParser.OR, i)

        def getRuleIndex(self):
            return MiniCParser.RULE_logicalOrExpression

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLogicalOrExpression" ):
                return visitor.visitLogicalOrExpression(self)
            else:
                return visitor.visitChildren(self)




    def logicalOrExpression(self):

        localctx = MiniCParser.LogicalOrExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_logicalOrExpression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 167
            self.logicalAndExpression()
            self.state = 172
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==28:
                self.state = 168
                self.match(MiniCParser.OR)
                self.state = 169
                self.logicalAndExpression()
                self.state = 174
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LogicalAndExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def equalityExpression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MiniCParser.EqualityExpressionContext)
            else:
                return self.getTypedRuleContext(MiniCParser.EqualityExpressionContext,i)


        def AND(self, i:int=None):
            if i is None:
                return self.getTokens(MiniCParser.AND)
            else:
                return self.getToken(MiniCParser.AND, i)

        def getRuleIndex(self):
            return MiniCParser.RULE_logicalAndExpression

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLogicalAndExpression" ):
                return visitor.visitLogicalAndExpression(self)
            else:
                return visitor.visitChildren(self)




    def logicalAndExpression(self):

        localctx = MiniCParser.LogicalAndExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_logicalAndExpression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 175
            self.equalityExpression()
            self.state = 180
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==27:
                self.state = 176
                self.match(MiniCParser.AND)
                self.state = 177
                self.equalityExpression()
                self.state = 182
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class EqualityExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def relationalExpression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MiniCParser.RelationalExpressionContext)
            else:
                return self.getTypedRuleContext(MiniCParser.RelationalExpressionContext,i)


        def EQ(self, i:int=None):
            if i is None:
                return self.getTokens(MiniCParser.EQ)
            else:
                return self.getToken(MiniCParser.EQ, i)

        def NEQ(self, i:int=None):
            if i is None:
                return self.getTokens(MiniCParser.NEQ)
            else:
                return self.getToken(MiniCParser.NEQ, i)

        def getRuleIndex(self):
            return MiniCParser.RULE_equalityExpression

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEqualityExpression" ):
                return visitor.visitEqualityExpression(self)
            else:
                return visitor.visitChildren(self)




    def equalityExpression(self):

        localctx = MiniCParser.EqualityExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_equalityExpression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 183
            self.relationalExpression()
            self.state = 188
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==23 or _la==26:
                self.state = 184
                _la = self._input.LA(1)
                if not(_la==23 or _la==26):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 185
                self.relationalExpression()
                self.state = 190
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RelationalExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def additiveExpression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MiniCParser.AdditiveExpressionContext)
            else:
                return self.getTypedRuleContext(MiniCParser.AdditiveExpressionContext,i)


        def LT(self, i:int=None):
            if i is None:
                return self.getTokens(MiniCParser.LT)
            else:
                return self.getToken(MiniCParser.LT, i)

        def LTE(self, i:int=None):
            if i is None:
                return self.getTokens(MiniCParser.LTE)
            else:
                return self.getToken(MiniCParser.LTE, i)

        def GT(self, i:int=None):
            if i is None:
                return self.getTokens(MiniCParser.GT)
            else:
                return self.getToken(MiniCParser.GT, i)

        def GTE(self, i:int=None):
            if i is None:
                return self.getTokens(MiniCParser.GTE)
            else:
                return self.getToken(MiniCParser.GTE, i)

        def getRuleIndex(self):
            return MiniCParser.RULE_relationalExpression

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRelationalExpression" ):
                return visitor.visitRelationalExpression(self)
            else:
                return visitor.visitChildren(self)




    def relationalExpression(self):

        localctx = MiniCParser.RelationalExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_relationalExpression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 191
            self.additiveExpression()
            self.state = 196
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 56623104) != 0):
                self.state = 192
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 56623104) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 193
                self.additiveExpression()
                self.state = 198
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AdditiveExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def multiplicativeExpression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MiniCParser.MultiplicativeExpressionContext)
            else:
                return self.getTypedRuleContext(MiniCParser.MultiplicativeExpressionContext,i)


        def PLUS(self, i:int=None):
            if i is None:
                return self.getTokens(MiniCParser.PLUS)
            else:
                return self.getToken(MiniCParser.PLUS, i)

        def MINUS(self, i:int=None):
            if i is None:
                return self.getTokens(MiniCParser.MINUS)
            else:
                return self.getToken(MiniCParser.MINUS, i)

        def getRuleIndex(self):
            return MiniCParser.RULE_additiveExpression

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAdditiveExpression" ):
                return visitor.visitAdditiveExpression(self)
            else:
                return visitor.visitChildren(self)




    def additiveExpression(self):

        localctx = MiniCParser.AdditiveExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_additiveExpression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 199
            self.multiplicativeExpression()
            self.state = 204
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==30 or _la==31:
                self.state = 200
                _la = self._input.LA(1)
                if not(_la==30 or _la==31):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 201
                self.multiplicativeExpression()
                self.state = 206
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MultiplicativeExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def unaryExpression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MiniCParser.UnaryExpressionContext)
            else:
                return self.getTypedRuleContext(MiniCParser.UnaryExpressionContext,i)


        def MUL(self, i:int=None):
            if i is None:
                return self.getTokens(MiniCParser.MUL)
            else:
                return self.getToken(MiniCParser.MUL, i)

        def DIV(self, i:int=None):
            if i is None:
                return self.getTokens(MiniCParser.DIV)
            else:
                return self.getToken(MiniCParser.DIV, i)

        def MOD(self, i:int=None):
            if i is None:
                return self.getTokens(MiniCParser.MOD)
            else:
                return self.getToken(MiniCParser.MOD, i)

        def getRuleIndex(self):
            return MiniCParser.RULE_multiplicativeExpression

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMultiplicativeExpression" ):
                return visitor.visitMultiplicativeExpression(self)
            else:
                return visitor.visitChildren(self)




    def multiplicativeExpression(self):

        localctx = MiniCParser.MultiplicativeExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_multiplicativeExpression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 207
            self.unaryExpression()
            self.state = 212
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 30064771072) != 0):
                self.state = 208
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 30064771072) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 209
                self.unaryExpression()
                self.state = 214
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class UnaryExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PLUS(self):
            return self.getToken(MiniCParser.PLUS, 0)

        def unaryExpression(self):
            return self.getTypedRuleContext(MiniCParser.UnaryExpressionContext,0)


        def MINUS(self):
            return self.getToken(MiniCParser.MINUS, 0)

        def NOT(self):
            return self.getToken(MiniCParser.NOT, 0)

        def primaryExpression(self):
            return self.getTypedRuleContext(MiniCParser.PrimaryExpressionContext,0)


        def getRuleIndex(self):
            return MiniCParser.RULE_unaryExpression

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnaryExpression" ):
                return visitor.visitUnaryExpression(self)
            else:
                return visitor.visitChildren(self)




    def unaryExpression(self):

        localctx = MiniCParser.UnaryExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_unaryExpression)
        try:
            self.state = 222
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [30]:
                self.enterOuterAlt(localctx, 1)
                self.state = 215
                self.match(MiniCParser.PLUS)
                self.state = 216
                self.unaryExpression()
                pass
            elif token in [31]:
                self.enterOuterAlt(localctx, 2)
                self.state = 217
                self.match(MiniCParser.MINUS)
                self.state = 218
                self.unaryExpression()
                pass
            elif token in [29]:
                self.enterOuterAlt(localctx, 3)
                self.state = 219
                self.match(MiniCParser.NOT)
                self.state = 220
                self.unaryExpression()
                pass
            elif token in [9, 10, 11, 12, 13, 14]:
                self.enterOuterAlt(localctx, 4)
                self.state = 221
                self.primaryExpression()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrimaryExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(MiniCParser.IDENTIFIER, 0)

        def constant(self):
            return self.getTypedRuleContext(MiniCParser.ConstantContext,0)


        def LPAREN(self):
            return self.getToken(MiniCParser.LPAREN, 0)

        def expression(self):
            return self.getTypedRuleContext(MiniCParser.ExpressionContext,0)


        def RPAREN(self):
            return self.getToken(MiniCParser.RPAREN, 0)

        def functionCall(self):
            return self.getTypedRuleContext(MiniCParser.FunctionCallContext,0)


        def getRuleIndex(self):
            return MiniCParser.RULE_primaryExpression

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrimaryExpression" ):
                return visitor.visitPrimaryExpression(self)
            else:
                return visitor.visitChildren(self)




    def primaryExpression(self):

        localctx = MiniCParser.PrimaryExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_primaryExpression)
        try:
            self.state = 231
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,21,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 224
                self.match(MiniCParser.IDENTIFIER)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 225
                self.constant()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 226
                self.match(MiniCParser.LPAREN)
                self.state = 227
                self.expression()
                self.state = 228
                self.match(MiniCParser.RPAREN)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 230
                self.functionCall()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FunctionCallContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(MiniCParser.IDENTIFIER, 0)

        def LPAREN(self):
            return self.getToken(MiniCParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(MiniCParser.RPAREN, 0)

        def arguments(self):
            return self.getTypedRuleContext(MiniCParser.ArgumentsContext,0)


        def getRuleIndex(self):
            return MiniCParser.RULE_functionCall

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionCall" ):
                return visitor.visitFunctionCall(self)
            else:
                return visitor.visitChildren(self)




    def functionCall(self):

        localctx = MiniCParser.FunctionCallContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_functionCall)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 233
            self.match(MiniCParser.IDENTIFIER)
            self.state = 234
            self.match(MiniCParser.LPAREN)
            self.state = 236
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 3758128640) != 0):
                self.state = 235
                self.arguments()


            self.state = 238
            self.match(MiniCParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArgumentsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MiniCParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(MiniCParser.ExpressionContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(MiniCParser.COMMA)
            else:
                return self.getToken(MiniCParser.COMMA, i)

        def getRuleIndex(self):
            return MiniCParser.RULE_arguments

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArguments" ):
                return visitor.visitArguments(self)
            else:
                return visitor.visitChildren(self)




    def arguments(self):

        localctx = MiniCParser.ArgumentsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_arguments)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 240
            self.expression()
            self.state = 245
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==19:
                self.state = 241
                self.match(MiniCParser.COMMA)
                self.state = 242
                self.expression()
                self.state = 247
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ConstantContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT_LITERAL(self):
            return self.getToken(MiniCParser.INT_LITERAL, 0)

        def CHAR_LITERAL(self):
            return self.getToken(MiniCParser.CHAR_LITERAL, 0)

        def BOOL_LITERAL(self):
            return self.getToken(MiniCParser.BOOL_LITERAL, 0)

        def STRING_LITERAL(self):
            return self.getToken(MiniCParser.STRING_LITERAL, 0)

        def getRuleIndex(self):
            return MiniCParser.RULE_constant

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitConstant" ):
                return visitor.visitConstant(self)
            else:
                return visitor.visitChildren(self)




    def constant(self):

        localctx = MiniCParser.ConstantContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_constant)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 248
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 14848) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





