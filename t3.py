# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables.   This is from O'Reilly's
# "Lex and Yacc", p. 63.
# -----------------------------------------------------------------------------
# como se menciona arriba me base en el ejemplo descrito
# modified by Luis Reyna
import sys
sys.path.insert(0,"../..")

if sys.version_info[0] >= 3:
    raw_input = input
#lo pide si no marca error not know why
reserved = {
    "program":"PROGRAM",
    "int":"INT",
    "float":"FLOAT",
    "else":"ELSE",
    "print":"PRINT",
    "if":"IF",
    "else":"ELSE",
    "print":"PRINT",
    "var":"VAR"
}
tokens = (
    'PROGRAM','IF','PRINT','ELSE','VAR','INT','FLOAT','ID','CTEI','CTEF','CTES','DIFF',
    )

#literals = ['=','+','-','*','/', '(',')',';',':'] no funciona asi 
literals = ";:}{><+-*/)(="
# Tokens

t_ignore = ' \t'
t_CTEI   = '[0-9]+'
t_CTEF   = '[0-9]+\.[0-9]+'
t_CTES   = '".*"'
t_DIFF   = '<>'

def t_ID(t):
    '[a-zA-Z][a-zA-Z0-9]*'
    t.type = reserved.get(t.value,'ID')
    return t
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lex.lex()


def p_programa(p): 
    '''programa : PROGRAM ID ';' programa2 bloque''' 
 
def p_programa2(p): 
    '''programa2 : vars
                 | empty''' 

def p_vars(p): 
    '''vars : VAR vars2'''
 
def p_vars2(p): 
    '''vars2 : ID vars3'''
 
def p_vars3(p): 
    '''vars3 : ',' vars2
             | ':' tipo ';' vars4'''
 
def p_vars4(p): 
    '''vars4 : vars2
             | empty'''
  
def p_tipo(p):
    '''tipo : INT
            | FLOAT'''

def p_bloque(p):
    '''bloque : '{' bloque2 '}' '''

def p_bloque2(p):
    '''bloque2 : estatuto bloque2
               | empty '''

def p_estatuto(p):
    '''estatuto : asignacion
                | condicion
                | escritura'''

def p_asignacion(p):
    '''asignacion : ID '=' expresion ';' '''
 
def p_expresion(p):
    '''expresion : exp expresion2 '''
 
def p_expresion2(p):
    '''expresion2 : '>' exp 
                  | '<' exp
                  | DIFF exp 
                  | empty''' 

def p_condicion(p):
    '''condicion : IF '(' expresion ')' bloque condicion2 ';' '''

def p_condicion2(p):
    '''condicion2 : ELSE bloque
                  | empty '''

def p_escritura(p):
    '''escritura : PRINT  '(' escritura2 ')' ';' '''

def p_escritura2(p):
    '''escritura2 : expresion escritura3
                  | CTES escritura3'''
 
def p_escritura3(p):
    '''escritura3 : ',' escritura2
    | empty '''
 
def p_exp(p):
    '''exp : termino exp2'''

def p_exp2(p):
    '''exp2 : '+' exp
            | '-' exp
            | empty''' 

def p_termino(p): 
    '''termino : factor termino2'''

def p_termino2(p):
    '''termino2 : '*' termino
                | '/' termino
                | empty '''

def p_factor(p): 
    '''factor : '(' expresion ')'
              | factor2 '''

def p_factor2(p):
    '''factor2 : '+' varcte
               | '-' varcte
               | varcte '''

def p_varcte(p):
    '''varcte : ID
              | CTEI
              | CTEF'''
def p_empty(p): 
    '''empty :''' 
    pass 
def p_error(p):
    if p: 
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

import ply.yacc as yacc 
yacc.yacc() 
 
while 1:
    try: 
        s = raw_input('calc > ') 
    except EOFError: 
        break
    if not s: continue 
    yacc.parse(s) 
 