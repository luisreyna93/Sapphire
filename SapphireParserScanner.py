# -----------------------------------------------------------------------------
# SapphireParserScanner.py
# -----------------------------------------------------------------------------
import sys
import Lex
from SapphireSemantics import validate_arr,func_dic,delete_local_var_dict,global_vars_dic, get_var,errors, add_to_func, func_is_repeated,get_func_quad, print_func_dict,validate_func_params,get_func_return_type, get_func_vars,add_to_local_var_dict,print_local_var_dict,add_to_global_var_dict,global_var_exists,local_var_exists
from SapphireQuadruples import semantic_cube
from copy import deepcopy
from MapaMemoria import MapaMemoria
import pprint
pp = pprint.PrettyPrinter()

tokens = Lex.tokens

scope = 1 #scope = 1 (global), scope = 2 (local)
paramsTemp = []
tipoActual = []
tipoActualReturn = []
pilao= []
popper= []
quadruplo=[]
actualFunc=""
quadruploStack=[] #saltos para los quadruplos
statusCondicion= -1
whileCondicion=-1
printType=-1
forStackAux=[]
firstMain=0; #variable para saber que es la primera instruccion del main y saber a donde brincar en el primer quadruplo
funcquad=-1; # variable para saber cual es el quadruplo de la primera insturccion de cada funcion
funcParams=0 #numero para saber cuantos parametros tiene la funcion llamada y sacar esa cantidad de pila o 
constant_dict = {}
arrlen= 1 #variable para saber si es arreglo y de cuanto
ret=None # variable para saber si la funcion regreso algo 

mem_local        = MapaMemoria(0, 1000, 2000, 3000,4000)
mem_global       = MapaMemoria(4000,5000, 6000,7000, 8000)
mem_constants    = MapaMemoria(8000,9000,10000, 11000, 12000)
mem_temps        = MapaMemoria(12000,13000,14000,15000,16000)

def p_program(p): 
    '''program : firstquad vars programp main'''
    pp.pprint(quadruplo)
    #pp.pprint(constant_dict)
    #pp.pprint(pilao)

def p_firstquad(p):
    '''firstquad : '''
    quadruplo.append(['goto','-1','-1','-1'])

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
                res =mem_temps.add_type(tipo,1)
                quadruplo.append([operando,op2[0],op1[0],res])
                pilao.append([res,tipo])
            else:
                print errors['TYPE_MISMATCH']
                exit(1)
    # else:
    #     print 'pilaaaaaa'
    #     #pp.pprint(pilao)

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
                res =mem_temps.add_type(tipo,1)
                quadruplo.append([operando,op2[0],op1[0],res])
                pilao.append([res,tipo])
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
                res =mem_temps.add_type(tipo,1)
                quadruplo.append([operando,op2[0],op1[0],res])
                pilao.append([res,tipo])
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
                res =mem_temps.add_type(tipo,1)
                quadruplo.append([operando,op2[0],op1[0],res])
                pilao.append([res,tipo])
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
    if p[-1] not in constant_dict:
        constant_dict[p[-1]] = mem_constants.add_type('int',1)
    pilao.append([constant_dict[p[-1]], 'int'])

def p_tipof(p):
    '''tipof :'''
    global pilao
    if p[-1] not in constant_dict:
        constant_dict[p[-1]] = mem_constants.add_type('float',1)
    pilao.append([constant_dict[p[-1]], 'float'])

def p_tipos(p):
    '''tipos :'''
    global pilao
    if p[-1] not in constant_dict:
        constant_dict[p[-1]] = mem_constants.add_type('string',1)
    pilao.append([constant_dict[p[-1]], 'string'])

def p_returntype(p): 
    '''returntype : VOID
                  | INT
                  | FLOAT''' 
    print p[1]
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
    global arrlen
    arrlen= p[2]

def p_main(p): 
    '''main : MAIN firstmain '(' ')' firstfuncquad block ''' 
    global paramsTemp
    global actualFunc
    if func_is_repeated(p[3]):
        print errors['REPEATED_DECLARATION_FUNC']
        exit(1)
    else:
        actualFunc=p[1]
        add_to_func(p[1], 'None', paramsTemp, -1)
        paramsTemp = []
        #print_func_dict()

def p_firstmain(p):
    '''firstmain : '''
    global firstMain
    firstMain=1;

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
            quadruplo[salida] = [quadruplo[salida][0],quadruplo[salida][1][0],'-1',len(quadruplo)]
        
        statusCondicion=-1

def p_body(p): 
    '''body : vars statmp''' 

def p_statmp(p): 
    '''statmp : statm statmp
              | empty''' 
    global firstMain
    if( firstMain):
        quadruplo[0] = [quadruplo[0][0],quadruplo[0][1],'-1',len(quadruplo)]
        firstMain=0;

def p_statm(p): 
    '''statm : asign
             | cond
             | write
             | for
             | while 
             | draw
             | id ';'
             | ret
             | empty''' #todo:checar esto

def p_ret(p):
    '''ret : RETURN sexp ';' '''
    global ret
    ret=pilao.pop()
    tipo=get_func_return_type(actualFunc)
    if ret and (tipo != 'void') and (ret[1]==tipo):
        quadruplo.append(['return',actualFunc,'-1',ret[0]])
        quadruplo.append(['retorno','-1','-1','-1'])
    elif tipo != 'void' or ret:
        print errors['RETURN_TYPE_FUNC_MISSMATCH']
        exit(-1)

def p_functions(p): 
    '''functions : FUNCTION returntype ID '(' functionsp ')' firstfuncquad block firstfuncquad2
            | empty''' 

def p_firstfuncquad(p):
    '''firstfuncquad : '''
    global funcquad
    funcquad= len(quadruplo)
    if firstMain!= 1:
        global paramsTemp
        global tipoActualReturn
        global actualFunc
        global funcquad
        if func_is_repeated(p[-4]):
            print errors['REPEATED_DECLARATION_FUNC']
            exit(1)
        else:
            actualFunc=p[-4]
            tipo=tipoActualReturn.pop()
            add_to_func(p[-4], tipo, paramsTemp,funcquad)
            paramsTemp = []
            #print_func_dict()


def p_firstfuncquad2(p):
    '''firstfuncquad2 : '''
    tipo=get_func_return_type(actualFunc)
    if not ret and tipo!='void':
        print errors['RETURN_TYPE_FUNC_MISSMATCH']
        exit(-1)
        
    if (ret[1]!=tipo) and tipo!='void':
        print errors['RETURN_TYPE_FUNC_MISSMATCH']
        exit(-1)
    global mem_local
    mem_local= MapaMemoria(0, 1000, 2000, 3000,4000)# borrar mem_local para empezar 
    global mem_temps
    mem_temps=MapaMemoria(12000,13000,14000,15000,16000)# borrar mem_local
    delete_local_var_dict()

def p_functionsp(p): 
    '''functionsp : param
                  | empty''' 

def p_param(p): 
    '''param : type ID paramp''' 
    global tipoActual
    tipo= tipoActual.pop()
    paramsTemp.append([p[2],tipo])
    add_to_local_var_dict(mem_local,p[2], tipo,1)

def p_paramp(p): 
    '''paramp : ',' param 
                | empty''' 

def p_vars(p): 
    '''vars : varsp
            | empty''' 
    global scope
    scope=2;
    global firstMain
    if( firstMain):
        quadruplo[0] = [quadruplo[0][0],quadruplo[0][1],'-1',len(quadruplo)]
        firstMain=0;

def p_varsp(p): 
    '''varsp : type varspp ';' varsp
             | empty'''

def p_varspp(p): 
    '''varspp : ID varsppaux'''
    global tipoActual
    global arrlen
    tipo= tipoActual.pop()
    tipoActual.append(tipo)
    if scope==1:
        if global_var_exists(p[1]):
            print errors['REPEATED_DECLARATION_FUNC']
            exit(1)
        else:
            add_to_global_var_dict(mem_global,p[1],tipo,arrlen)
            arrlen=1
    else:
        if local_var_exists(p[1]):
            print errors['REPEATED_DECLARATION_FUNC']
            exit(1)
        else:
            add_to_local_var_dict(mem_local,p[1], tipo,arrlen)
            arrlen=1

def p_varsppaux(p): 
    '''varsppaux : ',' varspp
                  | empty'''

def p_asign(p): 
    '''asign : vars
              | id asignp''' 
#todo: asignacion de arreglos
def p_asignp(p): 
    '''asignp : '=' sexp ';'
              | '[' sexp ']' '=' sexp ';' '''
    if p[1] == '[':
        aux1=pilao.pop() # por la forma de la sintaxis este es el valor a igualar
        aux=pilao.pop()
        if(aux[1] != 'int'): #validar si la superexp es id para marcar error
            print errors['TYPE_MISMATCH']
            exit(-1)
        res1=validate_arr(p[-1]) #por ser sexp se hace pop
        quadruplo.append(['ver', aux[0],0,int(res1[2])-1])
        res =mem_temps.add_type('int',1)
        if str(res1[0]) not in constant_dict:
            constant_dict[str(res1[0])] = mem_constants.add_type('int',1)
        quadruplo.append(['+', aux[0],constant_dict[str(res1[0])],res])
        quadruplo.append(['=',  aux1[0], '-1', res])
        pp.pprint(constant_dict)
    else:
        pp.pprint(pilao)
        quadruplo.append(['=',  pilao.pop()[0], '-1', pilao.pop()[0] ])

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
    #quadruplo.append(['+','1','-1',forStackAux.pop()])
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
    #checar
    #if local_var_exists(id1[0]):
    quadruplo.append(['=',valor[0],'-1',id1[0]])
    forStackAux.append(id1[0])
    # else:
    #     print '111'
    #     print_local_var_dict()
    #     print errors['NOT_DECLARED_VAR']
    #     exit(1)
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
    global funcParams 
    elmt= p[1]
    if elmt == '[':
        aux=pilao.pop()
        if(aux[1] != 'int'): #validar si la superexp es id para marcar error
            print errors['TYPE_MISMATCH']
            exit(-1)
        res1=validate_arr(p[-1]) #por ser sexp se hace pop
        quadruplo.append(['ver', aux[0],0,int(res1[2])-1])
        res =mem_temps.add_type('int',1)
        quadruplo.append(['+', aux[0],res1[0],res])
        pilao.append([[res], res1[1]]) # el quadruplo cuando es arreglo lo ponemos diferente para identificar que hay que checar onruntime
    elif elmt == '(':
        if func_is_repeated(p[-1]):
            tempparams=[]
            for x in range(0,funcParams):
                tempparams.append(pilao.pop())
            if validate_func_params(p[-1],deepcopy(tempparams)):
                quadruplo.append(['era', get_func_vars(p[-1]),p[-1],'-1'])
                for x in tempparams:
                    quadruplo.append(['param',x[0],'-1', funcParams ])
                    funcParams= funcParams-1
                quadruplo.append(['gosub', get_func_quad(p[-1]),p[-1],'-1'])
                if get_func_return_type(p[-1]) != 'void':
                    res =mem_temps.add_type(get_func_return_type(p[-1]),1)
                    quadruplo.append(['=', p[-1],'-1',res])
                    pilao.append([res, get_func_return_type(p[-1]) ])
                pp.pprint(pilao)
                pp.pprint(constant_dict)
            else:
                print errors['PARAMS_FUNC_BADQUANT']
                exit(-1)

        else: 
            print errors['NOT_DECLARED_FUNCTION']
            exit(-1)
    else:
        res=get_var(p[-1])
        pilao.append([res[0], res[1]])

def p_idpp(p): 
    '''idpp : sexp idppaux
            | empty''' 

def p_idppaux(p): 
    '''idppaux : ',' idpp 
                | empty'''  
    global funcParams
    funcParams= funcParams +1

def p_line(p): 
    '''line : LINE '(' sexp ',' sexp ',' sexp ',' sexp ')' ';' '''
    ##pp.pprint(pilao)
    par1=pilao.pop() 
    par2=pilao.pop() 
    par3=pilao.pop()
    par4=pilao.pop()
    if par1[1] != 'float' or par2[1] != 'float' or par3[1] != 'float' or par4[1] != 'float' :
        print errors['TYPE_MISMATCH']
        exit(1)
    else:
        quadruplo.append(['line',[par4[0],par3[0],par2[0],par1[0]],'-1','-1'])


def p_rect(p): 
    '''rect : RECT '(' sexp ',' sexp ',' sexp ',' sexp ')' ';' ''' 
    #pp.pprint(pilao)
    par1=pilao.pop() 
    par2=pilao.pop() 
    par3=pilao.pop()
    par4=pilao.pop()
    if par1[1] != 'float' or par2[1] != 'float' or par3[1] != 'float' or par4[1] != 'float' :
        print errors['TYPE_MISMATCH']
        exit(1)
    else:
        quadruplo.append(['rect',[par4[0],par3[0],par2[0],par1[0]],'-1','-1'])

def p_teapot(p): 
    '''teapot : TEAPOT '(' sexp ',' sexp ',' sexp ',' sexp ')' ';' '''
    #pp.pprint(pilao)
    par1=pilao.pop() 
    par2=pilao.pop() 
    par3=pilao.pop()
    par4=pilao.pop()
    if par1[1] != 'float' or par2[1] != 'float' or par3[1] != 'float' or par4[1] != 'float' :
        print errors['TYPE_MISMATCH']
        exit(1)
    else:
        quadruplo.append(['teapot',[par4[0],par3[0],par2[0],par1[0]],'-1','-1'])

def p_triangle(p): 
    '''triangle : TRIANGLE '(' sexp ',' sexp ',' sexp ',' sexp ')' ';' '''
    #pp.pprint(pilao)
    par1=pilao.pop() 
    par2=pilao.pop() 
    par3=pilao.pop()
    par4=pilao.pop()
    if par1[1] != 'float' or par2[1] != 'float' or par3[1] != 'float' or par4[1] != 'float' :
        print errors['TYPE_MISMATCH']
        exit(1)
    else:
        quadruplo.append(['triangle',[par4[0],par3[0],par2[0],par1[0]],'-1','-1'])

def p_cube(p): 
    '''cube : CUBE '(' sexp ',' sexp ',' sexp ',' sexp ')' ';' '''
    #pp.pprint(pilao)
    par1=pilao.pop() 
    par2=pilao.pop() 
    par3=pilao.pop()
    par4=pilao.pop()
    if par1[1] != 'float' or par2[1] != 'float' or par3[1] != 'float' or par4[1] != 'float' :
        print errors['TYPE_MISMATCH']
        exit(1)
    else:
        quadruplo.append(['cube',[par4[0],par3[0],par2[0],par1[0]],'-1','-1'])

def p_color(p): 
    '''color : COLOR '(' sexp ',' sexp ',' sexp ')' ';' '''
    #pp.pprint(pilao)
    par1=pilao.pop() 
    par2=pilao.pop() 
    par3=pilao.pop()
    if par1[1] != 'float' or par2[1] != 'float' or par3[1] != 'float' :
        print errors['TYPE_MISMATCH']
        exit(1)
    else:
        quadruplo.append(['color',[par3[0],par2[0],par1[0]],'-1','-1'])

def p_arc(p): 
    '''arc : ARC '(' sexp ',' sexp ',' sexp ',' sexp ')' ';' '''
    #pp.pprint(pilao)
    par1=pilao.pop() 
    par2=pilao.pop() 
    par3=pilao.pop()
    par4=pilao.pop()
    if par1[1] != 'float' or par2[1] != 'float' or par3[1] != 'float' or par4[1] != 'float' :
        print errors['TYPE_MISMATCH']
        exit(1)
    else:
        quadruplo.append(['arc',[par4[0],par3[0],par2[0],par1[0]],'-1','-1'])

def p_circe(p): 
    '''circle : CIRCLE '(' sexp ',' sexp ',' sexp ')' ';' '''
    #pp.pprint(pilao)
    par1=pilao.pop() 
    par2=pilao.pop() 
    par3=pilao.pop()
    if par1[1] != 'float' or par2[1] != 'float' or par3[1] != 'float' :
        print errors['TYPE_MISMATCH']
        exit(1)
    else:
        quadruplo.append(['circle',[par3[0],par2[0],par1[0]],'-1','-1'])

def p_width(p): 
    '''width : WIDTH '(' sexp ')' ';' '''
    #pp.pprint(pilao)
    par1=pilao.pop()
    if par1[1] != 'float' :
        print errors['TYPE_MISMATCH']
        exit(1)
    else:
        quadruplo.append(['width',par1[0],'-1','-1'])

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

output_dict = {
            'funcs': func_dic,
            'quadruples': quadruplo ,
            'constants': constant_dict,
            'globals': global_vars_dic,
    }
import json
with open('obj.json', 'w') as fp:
    json.dump(output_dict,fp)


 