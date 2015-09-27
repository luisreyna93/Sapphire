# -----------------------------------------------------------------------------
# SapphireParserScanner.py
# -----------------------------------------------------------------------------

import sys
sys.path.insert(0,"../..")

if sys.version_info[0] >= 3:
    raw_input = input

reserved = {
    #"program":"PROGRAM",
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
    #"var":"VAR",
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
    "main":"MAIN"
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

def p_program(p): 
    '''program : vars programp main''' 

def p_programp(p): 
    '''programp : functions programp
                | empty''' 

def p_sexp(p): 
    '''sexp : expression sexprima''' 

def p_sexprima(p): 
    '''sexprima : AND sexp
                | OR sexp
                | empty''' 

def p_expression(p): 
    '''expression : exp expressionp''' 

def p_expressionp(p): 
    '''expressionp : '<' exp
                    | '>' exp
                    | LTEQ exp 
                    | GTEQ exp
                    | EQ exp
                    | DIFF exp 
                    | empty''' 

def p_exp(p): 
    '''exp : term expp''' 

def p_expp(p): 
    '''expp : '+' exp
            | '-' exp
            | empty''' 

def p_term(p): 
    '''term : factor termp''' 

def p_termp(p): 
    '''termp : '/' term 
             | '*' term 
             | empty''' 

def p_factor(p): 
    '''factor : cons
              | '(' sexp ')' ''' 

def p_cons(p): 
    '''cons : id
            | CTEI
            | CTEF
            | CTES''' 

def p_returntype(p): 
    '''returntype : VOID
                  | INT
                  | FLOAT''' 

def p_type(p): 
    '''type : INT
            | FLOAT
            | ARRINT arrp
            | ARRFLOAT arrp'''

def p_arrp(p): 
    '''arrp : '[' CTEI ']' '''  

def p_main(p): 
    '''main : MAIN '(' ')' block ''' 

def p_block(p): 
    '''block : '{' body '}' ''' 

def p_body(p): 
    '''body : vars statmp''' 

def p_statmp(p): 
    '''statmp : statm statmp
              | empty''' 

def p_statm(p): 
    '''statm : asign
             | cond
             | write
             | for
             | while 
             | draw
             | empty''' #checar esto

def p_functions(p): 
    '''functions : FUNCTION returntype ID '(' functionsp ')' block
            | empty''' 

def p_functionsp(p): 
    '''functionsp : param
                  | empty''' 

def p_param(p): 
    '''param : type ID paramp''' 

def p_paramp(p): 
    '''paramp : ',' param 
                | empty''' 

def p_vars(p): 
    '''vars : varsp
            | empty''' 

def p_varsp(p): 
    '''varsp : type varspp ';' varsp
             | empty''' 

def p_varspp(p): 
    '''varspp : ID varsppaux''' 

def p_varsppaux(p): 
    '''varsppaux : ',' varspp
                  | empty''' 

def p_asign(p): 
    '''asign : vars
              | ID asignp''' 

def p_asignp(p): 
    '''asignp : '=' sexp ';'
              | '[' sexp ']' '=' sexp ';' ''' 

def p_cond(p): 
    '''cond : IF '(' sexp ')' block condp''' 

def p_condp(p): 
    '''condp : ELSE block 
             | empty''' 

def p_write(p): 
    '''write : PRINT '(' writep ')' ';' ''' 

def p_writep(p): 
    '''writep : sexp writepp
              | CTES writepp
              | id writepp''' 

def p_writepp(p): 
    '''writepp : ',' writep
                | empty''' 

def p_for(p): 
    '''for : FOR '(' asign ';' sexp ';' sexp ')' block''' 

def p_while(p): 
    '''while : WHILE '(' sexp ')' block'''

def p_draw(p): 
    '''draw : line
            | rect
            | teapot
            | cube
            | color
            | triangle
            | circle
            | arc
            | width''' 

def p_id(p): 
    '''id : ID idp''' 

def p_idp(p): 
    '''idp : '[' sexp ']' 
            | '(' idpp ')'
            | empty'''   

def p_idpp(p): 
    '''idpp : sexp idppaux
            | empty'''  

def p_idppaux(p): 
    '''idppaux : ',' idpp 
                | empty'''  

def p_line(p): 
    '''line : LINE '(' sexp ',' sexp ',' sexp ',' sexp ')' ';' ''' 

def p_rect(p): 
    '''rect : RECT '(' sexp ',' sexp ',' sexp ',' sexp ')' ';' ''' 

def p_teapot(p): 
    '''teapot : TEAPOT '(' sexp ',' sexp ',' sexp ',' sexp ')' ';' '''

def p_triangle(p): 
    '''triangle : TRIANGLE '(' sexp ',' sexp ',' sexp ',' sexp ')' ';' '''

def p_cube(p): 
    '''cube : CUBE '(' sexp ',' sexp ',' sexp ',' sexp ')' ';' '''

def p_color(p): 
    '''color : COLOR '(' sexp ',' sexp ',' sexp ')' ';' '''

def p_arc(p): 
    '''arc : ARC '(' sexp ',' sexp ',' sexp ',' sexp ')' ';' '''

def p_circe(p): 
    '''circle : CIRCLE '(' sexp ',' sexp ',' sexp ')' ';' '''

def p_width(p): 
    '''width : WIDTH '(' sexp ')' ';' '''

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
 
if(len(sys.argv) > 1):
    if sys.argv[1] == "-f":
        f = open(sys.argv[2], "r")
        s = f.readlines()
    string = ""
    for line in s:
        string += line + '\n'
    print string
    result = yacc.parse(string)
else:
    print "Error"
 