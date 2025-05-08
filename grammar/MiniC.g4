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
    : variableDeclaration // Local variable declarations
    | expressionStatement
    | ifStatement
    | whileStatement
    | forStatement
    | returnStatement
    | block // Nested blocks
    | SEMI // Empty statement
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

forStatement
    // Simplified: for(init; condition; update) statement
    // init and update can be expression statements or var declarations for init
    : FOR LPAREN (variableDeclaration | expressionStatement | SEMI)
                 (expression? SEMI)
                 (expression? RPAREN) statement
    ;

returnStatement
    : RETURN expression? SEMI
    ;

// Expressions
expression
    : assignmentExpression
    ;

assignmentExpression
    : logicalOrExpression (ASSIGN assignmentExpression)? // Right-associative
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
    ;

// Keywords (define before IDENTIFIER in Lexer rules)
IF      : 'if';
ELSE    : 'else';
WHILE   : 'while';
FOR     : 'for';
RETURN  : 'return';
INT     : 'int';
CHAR    : 'char';
BOOL    : 'bool';
TRUE    : 'true'; // For BOOL_LITERAL
FALSE   : 'false';// For BOOL_LITERAL
PRINTF  : 'printf'; // Treat as keyword for now, or handle as ID in functionCall
SCANF   : 'scanf';  // Treat as keyword for now

// Literals and Identifiers
IDENTIFIER      : [a-zA-Z_] [a-zA-Z0-9_]*;
INT_LITERAL     : [0-9]+;
CHAR_LITERAL    : '\'' ( ~('\''|'\\') | ('\\' .) ) '\''; // Simple char literal
BOOL_LITERAL    : TRUE | FALSE;
STRING_LITERAL  : '"' ( ~('\\'|'"') | ('\\' .) )* '"'; // For printf/scanf

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
WS          : [ \t\r\n]+ -> skip; // Skip whitespace
COMMENT     : '//' ~[\r\n]* -> skip; // Skip single-line comments
BLOCK_COMMENT: '/*' .*? '*/' -> skip; // Skip multi-line comments