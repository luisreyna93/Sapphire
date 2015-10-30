# -----------------------------------------------------------------------------
# SapphireParserScanner.py
# -----------------------------------------------------------------------------
import sys
import Lex
from SapphireSemantics import errors, add_to_func, func_is_repeated, print_func_dict, add_to_local_var_dict,print_local_var_dict,add_to_global_var_dict,global_var_exists,local_var_exists
from SapphireQuadruples import semantic_cube
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
actualFunc=""
quadruploStack=[]
statusCondicion= -1
whileCondicion=-1
printType=-1
forStackAux=[]
def p_program(p): 
    '''program : vars programp main'''
    pp.pprint(quadruplo)
    pp.pprint(pilao)

def p_programp(p): 
    '''programp : functions programp
                | empty''' 

def p_sexp(p): 
    '''sexp : expression sexprima'''
    if popper:
        if popper[-1] == '&&'  or popper[-1] =='||':
            global quadruplo
            operando= popper.pop()
            op1 =pilao.pop()
            op2=pilao.pop()
            tipo=semantic_cube.get((op2[1],operando, op1[1]), 'error')
            if tipo != 'error' :
                quadruplo.append([operando,op2[0],op1[0],'res'+str(len(quadruplo))])
                pilao.append(['res'+str(len(quadruplo)-1),tipo])
            else:
                print errors['TYPE_MISMATCH']
                exit(1)
    # else:
    #     print 'pilaaaaaa'
    #     pp.pprint(pilao)

def p_sexprima(p): 
    '''sexprima : AND sexp
                | OR sexp
                | empty''' 
    if p[1]:
        popper.append(p[1])

def p_expression(p): 
    '''expression : exp expressionp'''
    if popper:
        if popper[-1] == '>'  or popper[-1] =='<' or popper[-1] =='<=' or popper[-1] =='>=' or popper[-1] =='==' or popper[-1] =='<>':
            global quadruplo
            operando= popper.pop()
            op1 =pilao.pop()
            op2=pilao.pop()
            tipo=semantic_cube.get((op2[1],operando, op1[1]), 'error')
            if tipo != 'error' :
                quadruplo.append([operando,op2[0],op1[0],'res'+str(len(quadruplo))])
                pilao.append(['res'+str(len(quadruplo)-1),tipo])
            else:
                print errors['TYPE_MISMATCH']
                exit(1)

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
            operando= popper.pop()
            op1 =pilao.pop()
            op2=pilao.pop()
            tipo=semantic_cube.get((op2[1],operando, op1[1]), 'error')
            if tipo != 'error' :
                quadruplo.append([operando,op2[0],op1[0],'res'+str(len(quadruplo))])
                pilao.append(['res'+str(len(quadruplo)-1),tipo])
            else:
                print errors['TYPE_MISMATCH']
                exit(1)

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
            operando= popper.pop()
            op1 =pilao.pop()
            op2=pilao.pop()
            tipo=semantic_cube.get((op2[1],operando, op1[1]), 'error')
            if tipo != 'error' :
                quadruplo.append([operando,op2[0],op1[0],'res'+str(len(quadruplo))])
                pilao.append(['res'+str(len(quadruplo)-1),tipo])
            else:
                print errors['TYPE_MISMATCH']
                exit(1)

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
            | CTEI tipoi
            | CTEF tipof 
            | CTES tipos'''
def p_tipoi(p):
    '''tipoi :'''
    global pilao
    pilao.append([p[-1], 'int'])

def p_tipof(p):
    '''tipof :'''
    global pilao
    pilao.append([p[-1], 'float'])

def p_tipos(p):
    '''tipos :'''
    global pilao
    pilao.append([p[-1], 'string'])

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
    global actualFunc
    if func_is_repeated(p[3]):
        print errors['REPEATED_DECLARATION_FUNC']
        exit(1)
    else:
        actualFunc=p[1]
        add_to_func(p[1], 'None', paramsTemp)
        paramsTemp = {}
        #print_func_dict()

def p_block(p): 
    '''block : '{' body '}' ''' 
    global statusCondicion
    if statusCondicion>0:
        if whileCondicion>0:
            falso= quadruploStack.pop()
            retorno=quadruploStack.pop()
            quadruplo.append(['goto','-1','-1',retorno])
            quadruplo[falso] = [quadruplo[falso][0],quadruplo[falso][1][0],'-1',len(quadruplo)]
        else:
            global quadruploStack
            salida= quadruploStack.pop()
            quadruplo[salida] = [quadruplo[salida][0],quadruplo[salida][1][0],'-1',len(quadruplo)+1]
        
        statusCondicion=-1

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
    global actualFunc
    if func_is_repeated(p[3]):
        print errors['REPEATED_DECLARATION_FUNC']
        exit(1)
    else:
        actualFunc=p[3]
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
    quadruplo.append(['=',  pilao.pop()[0], '-1', p[-1] ])

def p_cond(p): 
    '''cond : IF '(' sexp ')' condaux block condp''' 

def p_condaux(p): 
    '''condaux :'''
    global statusCondicion
    statusCondicion=1
    cond=pilao.pop()
    if cond[1] != 'bool':
        print errors['TYPE_MISMATCH']
        exit(1)
    else:
        global quadruploStack
        quadruploStack.append(len(quadruplo))
        quadruplo.append(['gotof',cond,'-1','-1'])
def p_condp(p): 
    '''condp : ELSE condpaux block 
             | empty'''

def p_condpaux(p): 
    '''condpaux : '''
    quadruploStack.append(len(quadruplo))
    quadruplo.append(['goto',['-1','-1'],'-1','-1'])
    global statusCondicion
    statusCondicion=1

def p_write(p): 
    '''write : PRINT '(' writep ')' ';' ''' 

def p_writep(p): 
    '''writep : sexp writepaux writepp
              | CTES writepaux2 writepp
              | id writepaux3 writepp''' 

def p_writepaux(p): 
    '''writepaux : ''' 
    global printType
    printType=1

def p_writepaux2(p): 
    '''writepaux2 : '''
    global printType
    printType=2

def p_writepaux3(p): 
    '''writepaux3 : '''
    global printType
    printType=3

def p_writepp(p): 
    '''writepp : ',' writeppaux writep
                | empty writeppaux''' 

def p_writeppaux(p): 
    '''writeppaux : ''' 
    global printType
    if printType==1:
        quadruplo.append(['print','-1','-1',pilao.pop()[0]])
    elif printType==2:
        quadruplo.append(['print','-1','-1',p[-1]])
    elif printType==3:
        quadruplo.append(['print','-1','-1',p[-1]])

def p_for(p): 
    '''for : FOR '(' id '=' sexp  foraux ';' sexp foraux2 ')' block foraux3'''

def p_foraux3(p):
    '''foraux3 : '''
    global quadruploStack
    salida= quadruploStack.pop()
    quadruplo[salida] = [quadruplo[salida][0],quadruplo[salida][1],'-1',len(quadruplo)+1]
    quadruplo.append(['+','1','-1',forStackAux.pop()])
    quadruplo.append(['goto','-1','-1',salida-1])

def p_foraux2(p):
    '''foraux2 : '''
    cond = pilao.pop()
    quadruploStack.append(len(quadruplo))
    quadruplo.append(['gotof',cond[0],'-1','-1'])


def p_foraux(p):
    '''foraux : '''
    valor=pilao.pop()
    id1=pilao.pop()
    if local_var_exists(id1[0]):
        quadruplo.append(['=',valor[0],'-1',id1[0]])
        forStackAux.append(id1[0])
    else:
        print errors['REPEATED_DECLARATION_FUNC']
        exit(1)
def p_while(p): 
    '''while : WHILE whileaux '(' sexp ')' whileaux2 block'''

def p_whileaux2(p): 
    '''whileaux2 : '''
    cond = pilao.pop()
    if cond[1] != 'bool':
        print errors['TYPE_MISMATCH']
        exit(1)
    else:
        global quadruploStack
        quadruploStack.append(len(quadruplo))
        quadruplo.append(['gotof',cond,'-1','-1'])

def p_whileaux(p): 
    '''whileaux : '''
    global quadruploStack
    global statusCondicion
    global whileCondicion
    whileCondicion=1
    statusCondicion=1
    quadruploStack.append(len(quadruplo))

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
    global pilao 
    elmt= p[1]
    if elmt == '[':
        pilao.append([p[-1], 'int'])
    elif elmt == '(':
        pilao.append([p[-1], 'float'])
    else:
        pilao.append([p[-1], 'float'])

def p_idpp(p): 
    '''idpp : sexp idppaux
            | empty'''  

def p_idppaux(p): 
    '''idppaux : ',' idpp 
                | empty'''  

def p_line(p): 
    '''line : LINE '(' sexp ',' sexp ',' sexp ',' sexp ')' ';' '''
    pp.pprint(pilao)
    par1=pilao.pop() 
    par2=pilao.pop() 
    par3=pilao.pop()
    par4=pilao.pop()
    if par1[1] != 'float' or par2[1] != 'float' or par3[1] != 'float' or par4[1] != 'float' :
        print errors['TYPE_MISMATCH']
        print p.lineno(1)
        print p.lineno(2)
        print p.lineno(3)
        exit(1)
    else:
        quadruplo.append(['line',[par4[0],par3[0],par2[0],par1[0]],'-1','-1'])


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
 