# -----------------------------------------------------------------------------
# SapphireSemantics.py
# -----------------------------------------------------------------------------

import pprint

pp = pprint.PrettyPrinter()

func_dic = {}
local_vars_dic = {}
global_vars_dic = {}

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
    func_dic[fid] = {
        'type' : ftype,
        'params' : fparams
    }

def func_is_repeated(fid):
    if fid in func_dic:
        return True
    else:
        return False

def print_func_dict():
    print "\nFunciones"
    pp.pprint(func_dic)


