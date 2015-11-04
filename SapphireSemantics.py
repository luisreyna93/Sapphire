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
        'NOT_DECLARED_VAR' : 'NOT_DECLARED_VAR: variable no declarada'
}
def get_func_vars(func):
    return len(func_dic[func]['localVars'])+ len(func_dic[func]['params'])


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
    local_var_dict={}

def add_to_local_var_dict(mem,var_id, type):
    num= mem.add_type(type)
    local_var_dict[var_id] = {
        'type': type,
        'memdir' : num
    }
    #print_local_var_dict()
    #memoryCont= memoryCont +1

def add_to_global_var_dict(mem,var_id, type):
    num= mem.add_type(type)
    global_vars_dic[var_id] = {
        'type': type,
        'memdir' : num
    }
    #print_global_var_dict()
    #memoryCont= memoryCont +1
def get_var(id):
    #print id
    if id in local_var_dict:
        return [local_var_dict[id]['memdir'],local_var_dict[id]['type']]
    elif id in global_vars_dic:
        return [global_vars_dic[id]['memdir'],global_vars_dic[id]['type']]
    else :
        print errors['NOT_DECLARED_VAR']
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
def local_var_exists(vid):
    if vid in global_vars_dic or vid in local_var_dict:
        return True
    else:
        return False

def global_is_repeated(vid):
    if vid in global_vars_dic:
        return True
    else:
        return False

def local_is_repeated(vid):
    if vid in global_vars_dic or vid in local_var_dict:
        return True
    else:
        return False

def print_func_dict():
    print "\nFunciones"
    pp.pprint(func_dic)

def print_local_var_dict():
    print "\nVariables locales"
    pp.pprint(local_var_dict)

def print_global_var_dict():
    print "\nVariables globales"
    pp.pprint(global_vars_dic)
