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
    // init can be var decl or expression, update is expression.
    : FOR LPAREN (variableDeclaration | expression? SEMI) // init part (var decl or expression or empty)
                 (expression? SEMI)                     // condition part (expression or empty)
                 (expression? RPAREN)                   // update part (expression or empty)
           statement
    ;
    // Note: A common C 'for' loop init can be just "expression;"
    // The above allows "expression SEMI" for init, which is fine.
    // If init is variableDeclaration, it already includes a SEMI conceptually if it's a full statement,
    // but here it's part of the for structure, so the grammar expects it without an extra SEMI.
    // Let's refine forStatement to be more C-like if init is expression:
    // forStatement
    //     : FOR LPAREN forInitialization SEMI expression? SEMI expression? RPAREN statement
    //     ;
    // forInitialization
    //     : variableDeclaration // Handled: type IDENTIFIER (= expr)? -- no trailing SEMI needed here
    //     | expression          // Handled: just an expression
    //     |                     // Empty: handled by making expression? in main rule
    //     ;
    // The current structure is:
    // FOR LPAREN (variableDeclaration | expressionStatement | SEMI) (expression? SEMI) (expression? RPAREN) statement
    // This is also workable. `expressionStatement` would be `expression SEMI`.
    // If it's `variableDeclaration`, that already has a SEMI if it has an initializer in its own rule.
    // My VariableDeclaration already ends with SEMI: `typeSpecifier IDENTIFIER (ASSIGN expression)? SEMI`
    // So, for for-loop variable declaration, we should not have an *additional* SEMI.
    // Let's simplify the for-loop init to match typical C more closely:

/*
   Revised forStatement structure:
   for (declaration-or-expression ; expression ; expression) statement
   declaration-or-expression:
       variableDeclaration (without the trailing semicolon if it's a var decl)
       expression
       empty
*/
// The existing one is actually not bad:
// (variableDeclaration | expressionStatement | SEMI)
// - variableDeclaration is fine as is: `int i = 0;`
// - expressionStatement means `i = 0;` if `i` was declared before
// - SEMI means empty init like ` ; i < 10; ...`
// The example output shows a typical for, so let's assume this is fine for now.


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
    | STRING_LITERAL  // <-- This was the important addition
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
// TRUE and FALSE are better handled as part of BOOL_LITERAL directly
// TRUE    : 'true';
// FALSE   : 'false';

// Literals and Identifiers
BOOL_LITERAL    : 'true' | 'false'; // Moved here for clarity, parsed as a literal
IDENTIFIER      : [a-zA-Z_] [a-zA-Z0-9_]*;
INT_LITERAL     : [0-9]+;
CHAR_LITERAL    : '\'' ( ~['\r\n\f\t'\\] | ('\\' .) ) '\''; // Simple char literal, avoid newlines/tabs
STRING_LITERAL  : '"' ( ~["\r\n\f\t\\] | ('\\' .) )*? '"'; // Non-greedy match for content, avoid newlines/tabs

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
BLOCK_COMMENT: '/*' .*? '*/' -> skip; // Skip multi-line comments (non-greedy)