grammar MiniC;

// Entry rule
program: (declaration)* EOF;

declaration
    : variableDeclaration
    | functionDeclaration
    ;

variableDeclaration
    : typeSpecifier IDENTIFIER (ASSIGN expression)? SEMI
    ;

typeSpecifier
    : INT | CHAR | BOOL
    ;

functionDeclaration
    : typeSpecifier IDENTIFIER LPAREN parameters? RPAREN block
    ;

parameters
    : parameter (COMMA parameter)*
    ;

parameter
    : typeSpecifier IDENTIFIER
    ;

block
    : LBRACE (statement)* RBRACE
    ;

statement
    : variableDeclaration
    | expressionStatement
    | ifStatement
    | whileStatement
    | forStatement      // Uses the version below
    | returnStatement
    | block
    | SEMI
    ;

expressionStatement
    : expression SEMI
    ;

ifStatement
    : IF LPAREN expression RPAREN statement (ELSE statement)?
    ;

whileStatement
    : WHILE LPAREN expression RPAREN statement
    ;

// Revised forStatement using an intermediate rule for initialization
forStatement
    : FOR LPAREN init=forInitialization SEMI cond=expression? SEMI upd=expression? RPAREN body=statement
    ;

forInitialization  // Intermediate rule for the init part of a for loop
    : varInit=variableDeclaration   // Label the variableDeclaration alternative
    | exprInit=expression?          // Label the expression alternative (can be empty)
    ;                               // Implicitly allows empty init if exprInit matches nothing

returnStatement
    : RETURN expression? SEMI
    ;

// Expressions
expression
    : assignmentExpression
    ;

assignmentExpression
    : logicalOrExpression (ASSIGN assignmentExpression)?
    ;

logicalOrExpression
    : logicalAndExpression (OR logicalAndExpression)*
    ;

logicalAndExpression
    : equalityExpression (AND equalityExpression)*
    ;

equalityExpression
    : relationalExpression ((EQ | NEQ) relationalExpression)*
    ;

relationalExpression
    : additiveExpression ((LT | LTE | GT | GTE) additiveExpression)*
    ;

additiveExpression
    : multiplicativeExpression ((PLUS | MINUS) multiplicativeExpression)*
    ;

multiplicativeExpression
    : unaryExpression ((MUL | DIV | MOD) unaryExpression)*
    ;

unaryExpression
    : PLUS unaryExpression
    | MINUS unaryExpression
    | NOT unaryExpression
    | primaryExpression
    ;

primaryExpression
    : IDENTIFIER
    | constant
    | LPAREN expression RPAREN
    | functionCall
    ;

functionCall
    : IDENTIFIER LPAREN arguments? RPAREN
    ;

arguments
    : expression (COMMA expression)*
    ;

constant
    : INT_LITERAL
    | CHAR_LITERAL
    | BOOL_LITERAL
    | STRING_LITERAL
    ;

// Keywords
IF      : 'if';
ELSE    : 'else';
WHILE   : 'while';
FOR     : 'for';
RETURN  : 'return';
INT     : 'int';
CHAR    : 'char';
BOOL    : 'bool';

// Literals and Identifiers
BOOL_LITERAL    : 'true' | 'false';
IDENTIFIER      : [a-zA-Z_] [a-zA-Z0-9_]*;
INT_LITERAL     : [0-9]+;

// Corrected CHAR_LITERAL and STRING_LITERAL to avoid warnings and be more standard
CHAR_LITERAL    : '\'' ( '\\' . | ~[\\'] ) '\''; // Content: escape OR any char not backslash or single quote
STRING_LITERAL  : '"' ( '\\' . | ~[\\"] )*? '"';// Content: escape OR any char not backslash or double quote (non-greedy)


// Operators and Punctuation
LPAREN  : '(';
RPAREN  : ')';
LBRACE  : '{';
RBRACE  : '}';
SEMI    : ';';
COMMA   : ',';
ASSIGN  : '=';
GT      : '>';
LT      : '<';
EQ      : '==';
LTE     : '<=';
GTE     : '>=';
NEQ     : '!=';
AND     : '&&';
OR      : '||';
NOT     : '!';
PLUS    : '+';
MINUS   : '-';
MUL     : '*';
DIV     : '/';
MOD     : '%';

// Whitespace and Comments
WS          : [ \t\r\n]+ -> skip;
COMMENT     : '//' ~[\r\n]* -> skip;
BLOCK_COMMENT: '/*' .*? '*/' -> skip;