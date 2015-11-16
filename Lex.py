# -----------------------------------------------------------------------------
# Lex.py
# -----------------------------------------------------------------------------

import sys
sys.path.insert(0,"../..")

if sys.version_info[0] >= 3:
    raw_input = input

reserved = {
    "int":"INT",
    "arrint":"ARRINT",
    "float":"FLOAT",
    "arrfloat":"ARRFLOAT",
    "else":"ELSE",
    "print":"PRINT",
    "if":"IF",
    "else":"ELSE",
    "for":"FOR",
    "while":"WHILE",
    "print":"PRINT",
    "void":"VOID",
    "line":"LINE",
    "rect":"RECT",
    "teapot":"TEAPOT",
    "cube":"CUBE",
    "color":"COLOR",
    "triangle":"TRIANGLE",
    "circle":"CIRCLE",
    "arc":"ARC",
    "width":"WIDTH",
    "function":"FUNCTION",
    "void":"VOID",
    "main":"MAIN",
    "return": "RETURN"
}
tokens = [
    'CTEI', 'CTEF', 'CTES', 'DIFF', 'EQ', 'GTEQ', 'LTEQ', 'AND', 'OR', 'ID'
    ] + list(reserved.values())

literals = ";:,{}[]()<>&|+-*/="

# Tokens
t_ignore = ' \t'
t_CTEI   = r'[0-9]+'
t_CTEF   = r'[0-9]+\.[0-9]+'
t_CTES   = r'".*"'
t_DIFF   = r'<>'
t_EQ   = r'=='
t_GTEQ = r'>='
t_LTEQ = r'<='
t_AND = r'&&'
t_OR = r'\|\|'

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = reserved.get(t.value,'ID')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lex.lex()