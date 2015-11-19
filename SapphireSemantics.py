# -----------------------------------------------------------------------------
# SapphireSemantics.py
# -----------------------------------------------------------------------------

import pprint
from copy import deepcopy

pp = pprint.PrettyPrinter()

func_dic = {}
local_var_dict = {}
global_vars_dic = {}
memoryCont = 1000

errors = {
        'REPEATED_DECLARATION_VAR': 'REPEATED_DECLARATION_VAR: Declaracion de variable repetida.',
        'REPEATED_DECLARATION_FUNC': 'REPEATED_DECLARATION_FUNC: Declaracion de funcion repetida.',
        'TYPE_MISMATCH' : 'TYPE_MISMATCH: Tipos no compatibles',
        'NOT_DECLARED_FUNCTION' : 'NOT_DECLARED_FUNCTION: funcion no declarada',
        'PARAMS_FUNC_BADQUANT' : 'PARAMS_FUNC_BADQUANT: cantidad de parametros incorrecto',
        'NOT_DECLARED_VAR' : 'NOT_DECLARED_VAR: variable no declarada',
        'RETURN_TYPE_FUNC_MISSMATCH' : 'RETURN_TYPE_FUNC_MISSMATCH: el retorno de la funcion no es valido',
        'ARR_OVERFLOW': 'ARR_OVERFLOW: el arreglo no tiene ese indice'
}
def get_func_vars(func):
    return len(func_dic[func]['localVars'])
    #return len(func_dic[func]['localVars'])+ len(func_dic[func]['params'])


def get_func_quad(func):
    return func_dic[func]['quad']

def get_func_return_type(func):
    return func_dic[func]['type']

def validate_func_params(func,arr):
    if len(func_dic[func]['params']) != len(arr):
        return False
    arr.reverse()
    for x in func_dic[func]['params']:
        y1= arr.pop()[1]
        y2= x[1]
        if(y1 != y2):
            return False
    return True;
def add_to_func(fid, ftype, fparams,fquad):
    global local_var_dict
    func_dic[fid] = {
        'type' : ftype,
        'params' : fparams,
        'localVars' : deepcopy(local_var_dict),
        'quad' : fquad
    }
    print_func_dict()

def delete_local_var_dict():
    local_var_dict={}

def add_to_local_var_dict(mem,var_id, type,cant):
    num= mem.add_type(type,cant)
    local_var_dict[var_id] = {
        'type': type,
        'memdir' : num,
        'size': cant
    }
    #print_local_var_dict()
    #memoryCont= memoryCont +1

def add_to_global_var_dict(mem,var_id, type,cant):
    num= mem.add_type(type,cant)
    global_vars_dic[var_id] = {
        'type': type,
        'memdir' : num,
        'size': cant
    }
    print_global_var_dict()
    #memoryCont= memoryCont +1
def get_var(id):
    #print id
    if id in local_var_dict:
        if 'arr' in local_var_dict[id]['type']:
            print errors['NOT_DECLARED_VAR']
            exit(-1)
        return [local_var_dict[id]['memdir'],local_var_dict[id]['type']]
    elif id in global_vars_dic:
        if 'arr' in global_vars_dic[id]['type']:
            print errors['NOT_DECLARED_VAR']
            exit(-1)
        return [global_vars_dic[id]['memdir'],global_vars_dic[id]['type']]
    else :
        print errors['NOT_DECLARED_VAR']
        pp.pprint(local_var_dict)
        exit(-1)
def func_is_repeated(fid):
    if fid in func_dic:
        return True
    else:
        return False
def global_var_exists(vid):
    if vid in global_vars_dic:
        return True
    else:
        return False
#todo: no creo que deba checar en global porque no podrias declarar una variable global y local con el mismo nombre
def local_var_exists(vid):
    if vid in global_vars_dic or vid in local_var_dict:
        return True
    else:
        return False

# def global_is_repeated(vid):
#     if vid in global_vars_dic:
#         return True
#     else:
#         return False

# def local_is_repeated(vid):
#     if vid in global_vars_dic or vid in local_var_dict:
#         return True
#     else:
#         return False

#similar a get_var() pero para arreglos
def validate_arr(vid):
    error = False
    if vid in local_var_dict:
        if 'arr' not in local_var_dict[vid]['type']:
            error=True
        else:
            print_local_var_dict
            return [local_var_dict[vid]['memdir'],(local_var_dict[vid]['type']).replace('arr',''),local_var_dict[vid]['size']]

    if vid in global_vars_dic:
        if 'arr' not in global_vars_dic[vid]['type']:
            error=True
        else:
            return [global_vars_dic[vid]['memdir'],(global_vars_dic[vid]['type']).replace('arr',''),global_vars_dic[vid]['size']]
    print errors['NOT_DECLARED_VAR']
    exit(-1)



def print_func_dict():
    print "\nFunciones"
    pp.pprint(func_dic)

def print_local_var_dict():
    print "\nVariables locales"
    pp.pprint(local_var_dict)

def print_global_var_dict():
    print "\nVariables globales"
    pp.pprint(global_vars_dic)
