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
        'REPEATED_DECLARATION_FUNC': 'REPEATED_DECLARATION_FUNC: Declaracion de funcion repetida.'
}

def add_to_func(fid, ftype, fparams):
    global local_var_dict
    func_dic[fid] = {
        'type' : ftype,
        'params' : fparams,
        'localVars' : deepcopy(local_var_dict)
    }
    local_var_dict={}

def add_to_local_var_dict(var_id, type):
    global memoryCont
    local_var_dict[var_id] = {
        'type': type,
        'memdir' : memoryCont
    }
    print_local_var_dict()
    memoryCont= memoryCont +1

def add_to_global_var_dict(var_id, type):
    global memoryCont
    global_vars_dic[var_id] = {
        'type': type,
        'memdir' : memoryCont
    }
    print_global_var_dict()
    memoryCont= memoryCont +1

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
