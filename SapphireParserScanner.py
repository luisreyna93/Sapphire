# -----------------------------------------------------------------------------
# SapphireParserScanner.py
# -----------------------------------------------------------------------------
import sys
import Lex
from SapphireSemantics import errors, add_to_func, func_is_repeated, print_func_dict, add_to_local_var_dict,print_local_var_dict,add_to_global_var_dict,global_var_exists,local_var_exists
from copy import deepcopy
import pprint
pp = pprint.PrettyPrinter()

tokens = Lex.tokens

scope = 1 #scope = 1 (global), scope = 2 (local)
paramsTemp = {}
tipoActual = []
tipoActualReturn = []
pilao= []
popper= []
quadruplo=[]

def p_program(p): 
    '''program : vars programp main''' 

def p_programp(p): 
    '''programp : functions programp
                | empty''' 

def p_sexp(p): 
    '''sexp : expression sexprima'''
    if popper:
        if popper[-1] == '&&'  or popper[-1] =='||':
            global quadruplo
            quadruplo.append([popper.pop(),pilao.pop(),pilao.pop(),'res'+str(len(quadruplo))])
            pilao.append('res'+str(len(quadruplo)))

def p_sexprima(p): 
    '''sexprima : AND sexp
                | OR sexp
                | empty''' 
    if p[1]:
        popper.append(p[1])
        pp.pprint(popper)

def p_expression(p): 
    '''expression : exp expressionp'''
    if popper:
        if popper[-1] == '>'  or popper[-1] =='<' or popper[-1] =='<=' or popper[-1] =='>=' or popper[-1] =='==' or popper[-1] =='<>':
                global quadruplo
                quadruplo.append([popper.pop(),pilao.pop(),pilao.pop(),'res'+str(len(quadruplo))])
                pilao.append('res'+str(len(quadruplo))) 

def p_expressionp(p): 
    '''expressionp : '<' exp
                    | '>' exp
                    | LTEQ exp 
                    | GTEQ exp
                    | EQ exp
                    | DIFF exp 
                    | empty'''
    if p[1]:
        popper.append(p[1])

def p_exp(p): 
    '''exp : term expp'''
    if popper: 
        if popper[-1] == '+' or popper[-1] =='-':
            global quadruplo
            quadruplo.append([popper.pop(),pilao.pop(),pilao.pop(),'res'+str(len(quadruplo))])
            pilao.append('res'+str(len(quadruplo))) 

def p_expp(p): 
    '''expp : '+' exp
            | '-' exp
            | empty''' 
    global popper
    if p[1]:
        popper.append(p[1])

def p_term(p): 
    '''term : factor termp'''
    if popper: 
        if popper[-1] == '*' or popper[-1] =='/':
            global quadruplo
            quadruplo.append([popper.pop(),pilao.pop(),pilao.pop(),'res'+str(len(quadruplo))])
            pilao.append('res'+str(len(quadruplo)))

def p_termp(p): 
    '''termp : '/' term 
             | '*' term 
             | empty''' 
    global popper
    if p[1]:
        popper.append(p[1])

def p_factor(p): 
    '''factor : cons
              | bracketl sexp bracketr '''


def p_bracketl(p):
    '''bracketl : '(' '''
    global popper
    popper.append(p[1])

def p_bracketr(p):
    '''bracketr : ')' '''
    global popper
    popper.pop()

def p_cons(p): 
    '''cons : id
            | CTEI
            | CTEF
            | CTES'''
    global pilao
    pilao.append(p[1])

def p_returntype(p): 
    '''returntype : VOID
                  | INT
                  | FLOAT''' 
    global tipoActualReturn 
    tipoActualReturn.append(p[1])

def p_type(p): 
    '''type : INT
            | FLOAT
            | ARRINT arrp
            | ARRFLOAT arrp'''
    global tipoActual
    tipoActual.append(p[1])

def p_arrp(p): 
    '''arrp : '[' CTEI ']' '''  

def p_main(p): 
    '''main : MAIN '(' ')' block ''' 
    global paramsTemp
    global tipoActualReturn
    if func_is_repeated(p[3]):
        print errors['REPEATED_DECLARATION_FUNC']
        exit(1)
    else:
        add_to_func(p[1], 'None', paramsTemp)
        paramsTemp = {}
        #print_func_dict()

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
    global paramsTemp
    global tipoActualReturn
    if func_is_repeated(p[3]):
        print errors['REPEATED_DECLARATION_FUNC']
        exit(1)
    else:
        add_to_func(p[3], tipoActualReturn.pop(), paramsTemp)
        paramsTemp = {}
        #print_func_dict()


def p_functionsp(p): 
    '''functionsp : param
                  | empty''' 

def p_param(p): 
    '''param : type ID paramp''' 
    global tipoActual
    paramsTemp.update({p[2] : tipoActual.pop()})

def p_paramp(p): 
    '''paramp : ',' param 
                | empty''' 

def p_vars(p): 
    '''vars : varsp
            | empty''' 
    global scope
    scope=2;

def p_varsp(p): 
    '''varsp : type varspp ';' varsp
             | empty'''

def p_varspp(p): 
    '''varspp : ID varsppaux'''
    global tipoActual
    tipo= tipoActual.pop()
    tipoActual.append(tipo)
    if scope==1:
        if global_var_exists(p[1]):
            print errors['REPEATED_DECLARATION_FUNC']
            exit(1)
        else:
            add_to_global_var_dict(p[1],tipo)
    else:
        if local_var_exists(p[1]):
            print errors['REPEATED_DECLARATION_FUNC']
            exit(1)
        else:
            add_to_local_var_dict(p[1], tipo)

def p_varsppaux(p): 
    '''varsppaux : ',' varspp
                  | empty'''

def p_asign(p): 
    '''asign : vars
              | ID asignp''' 

def p_asignp(p): 
    '''asignp : '=' sexp ';'
              | '[' sexp ']' '=' sexp ';' ''' 
    pp.pprint(quadruplo)

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
    #print string
    result = yacc.parse(string)
else:
    print "Error"
 