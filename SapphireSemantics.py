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
        'PARAMETER_LENGTH_MISMATCH': 'Function {0} expects {1} parameters and received {2} parameters at line: {3} ',
        'REPEATED_DECLARATION_FUNC': 'Declaracion de funcion repetida.',
        'REPEATED_FUNC_DECLARATION': 'Repeated declaration of function {0} found at line: {1} ',
        'UNDECLARED_VARIABLE': 'Undeclared variable {0} found at line: {1} ',
        'UNDECLARED_FUNCTION': 'Undeclared function {0} found at line: {1} ',
        'STACKOVERFLOW': 'Stackoverflow, the program is too big.',
        'PARAMETER_TYPE_MISMATCH': 'Function {0}, expected type {1} and received type {2} in position {3}',
        'PARAMETER_LENGTH_MISMATCH': 'Function {0}, expected {1} parameters',
        'INVALID_ARRAY_DECLARATION': 'Variable {0} of type array in line {1}, should be declared with constant dimensions.'
}

def add_to_func(fid, ftype, fparams):
    global local_var_dict
    func_dic[fid] = {
        'type' : ftype,
        'params' : fparams,
        'localVars' : deepcopy(local_var_dict)
    }
    local_var_dict={}

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
def print_func_dict():
    print "\nFunciones"
    pp.pprint(func_dic)

def print_local_var_dict():
    print "\nLOCAL VAR DICT"
    pp.pprint(local_var_dict)

def print_global_var_dict():
    print "\nGLOBAL VAR DICT"
    pp.pprint(global_vars_dic)

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
