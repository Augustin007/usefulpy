'''
expression checker

DESCRIPTION
A simple CAS system

LICENSE PLATAFORMS and INSTALLATION:
This is a section of usefulpy. See usefulpy.__init__ and usefulpy license
file

RELEASE NOTES:
0
 0.0
  Version 0.0.0:
   Simple mathematical simplifier
  Version 0.0.1:
   Bugfixes
  Version 0.0.2:
   Improvements to work better with mathfunc class
'''

import math as _math

### DUNDERS ###
__author__ = 'Augustin Garcia'
__version__ = '0.0.2'

### IMPORTS ###
from collections import abc
from functools import cache

### UTILITY ###
def _flatten(l):
    '''flatten an iterable'''
    for el in l:
        if isinstance(el, abc.Iterable) and not isinstance(el, (str, bytes)): yield from _flatten(el)
        else: yield el

def _expand(composition:tuple, oper:str)->tuple:
    checked, run = False, []
    for n in composition:
        try:
            if n[0] == oper:
                
                checked = True; run.extend(n[1])
                continue
        except: pass
        run.append(n)
    return tuple(run) if not checked else _expand(tuple(run), oper)

valid_operation = []
operations = {}
verbose = False

def _lookup_alias(dictionary, name):
    def lookup_alias(func):
        dictionary[name] = func
        valid_operation.append(name)
        return func
    return lookup_alias

def _expand(composition:tuple, oper:str)->tuple:
    checked, run = False, []
    for n in composition:
        try:
            if n[0] == oper:
                checked = True; run.extend(n[1])
                continue
        except: pass
        run.append(n)
    return tuple(run) if not checked else _expand(tuple(run), oper)

def _are_equal(c1:tuple, c2:tuple)->bool:
    lc2 = list(c2)
    for c, n in enumerate(c1):
        if n not in lc2:
            return False
        c2 = lc2.index(n)
        lc2.pop(c2)
    if lc2: return False
    return True

def _ueq(a, b):
    if type(a) is tuple:
        if type(b) is tuple:
            return _are_equal(a, b)
        return False
    return a==b

### DATA EXTRACTORS ###
def _add_extract_mul(composition:tuple)->tuple[float, any, bool]:
    lc:list = list(composition[1])
    for c, n in enumerate(composition[1]):
        if isinstance(n, (int, float)):
            lc.pop(c)
            if len(lc) == 1:
                return n, lc[0], False
            return n, ('mul', tuple(lc)), False
    return 1, composition, False

def _add_extract(value)->tuple[float, any, bool]:
    value = _simplify(value)
    if type(value) is tuple:
        if value[0] == 'mul':
            return _add_extract_mul(value)
        if value[0] in ('pow', 'nest'): ##TODO: pow and nest value/count
            return 1, value, False
        raise ValueError(f'invalid operation string recieved {value[0]}')
    if isinstance(value, (int, float)):
        return value, None, True
    if callable(value):
        return 1, value, False
    raise TypeError(f'invalid type recieved, type {value.__class__.__name__}')

##TODO: test _mul_distribute and _mul_add_expand, they are untested with the new changes

def _mul_distribute(composition, mult): 
    lcomposition = list(composition)
    for count, value in enumerate(composition[1]):
        lst = [value]
        lst.extend(mult)
        lcomposition[count] = ('mul', tuple(lst))
    return _simplify(('add', tuple(lcomposition)))

def _mul_add_expand(composition:tuple)->tuple:
    lcomposition=list(composition[1])
    for count, value in enumerate(composition[1]):
        if isinstance(value, tuple):
            if value[0] == 'add':
                return _mul_distribute(value, lcomposition[:count]+lcomposition[count+1:])
    return False

def _mul_extract(value):
    value = _simplify(value)
    if type(value) is tuple:
        if value[0] == 'pow':
            if isinstance(value[1][1], (int, float)):
                return value[1][1], value[1][0], False
            return 1, value, False
        elif value[0] == 'nest':
            return 1, value, False
        raise ValueError(f'invalid operation string recieved {value[0]}')
    if isinstance(value, (int, float)):
        return value, None, True
    if callable(value):
        return 1, value, False
    raise TypeError(f'invalid type recieved, type {value.__class__.__name__}')        

### SIMPLIFIERS ###
@_lookup_alias(operations, 'add')
def _simplify_add(composition:tuple)->tuple:
    if type(composition) is not tuple:
        raise ValueError(f'composition should be a tuple, not a {composition.__class__.__name__}')
    if len(composition) != 2:
        raise ValueError(f'tuple should be of length 2')
    if composition[0] != 'add':
        raise ValueError(f'invalid string recieved, should be \'add\', got \'{composition[0]}\'')
    if len(composition[1]) == 0:
        return 0
    if len(composition[1]) == 1:
        return _simplify(composition[1][0])

    list_composition:list=list(_expand(composition[1], 'add'))

    run_list_composition:list = []
    while list_composition:
        value = list_composition.pop(0)
        count, value, constant = _add_extract(value)
        runcount = 0
        for new_value in list_composition.copy():
            if constant:
                if isinstance(new_value, (int, float)):
                    count += list_composition.pop(runcount)
                    continue
                runcount += 1
                continue
            newcount, newvalue = _add_extract(new_value)[0:2]
            if newvalue == value:
                count += newcount
                list_composition.pop(runcount)
                continue
            if isinstance(value, abc.Iterable) and isinstance(newvalue, abc.Iterable):
                if value[0] == 'mul' and newvalue[0] == 'mul':
                    if _ueq(value[1], newvalue[1]):
                        count += newcount
                        list_composition.pop(runcount)
                        continue
            runcount += 1
            continue
        if constant:
            if count != 0:
                run_list_composition.append(count)
        else:
            if count != 0:
                if count != 1:
                    if type(value) == tuple:
                        if value[0] == 'mul':
                            run_list_composition.append(('mul', (*value[1], count)))
                            continue
                    run_list_composition.append(('mul', (value, count)))
                else:
                    run_list_composition.append(value)
    
    if len(run_list_composition) == 0:
        return 0
    if len(run_list_composition) == 1:
        return _simplify(run_list_composition[0])
    return ('add', tuple(set(run_list_composition)))

@_lookup_alias(operations, 'mul')
def _simplify_mul(composition:tuple)->tuple:
    if type(composition) is not tuple:
        raise ValueError(f'composition should be a tuple, not a {composition.__class__.__name__}')
    if len(composition) != 2:
        raise ValueError(f'tuple should be of length 2')
    if composition[0] != 'mul':
        raise ValueError(f'invalid string recieved, should be \'mul\', got \'{composition[0]}\'')
    test = _mul_add_expand(composition)
    if test != False:
        return test
    if len(composition[1]) == 0:
        return 1
    if len(composition[1]) == 1:
        return _simplify(composition[1][0])
    if 0 in composition[1]:
        return 0
    list_composition:list = list(_expand(composition[1], 'mul'))
    run_list_composition:list = []
    
    while list_composition:
        value = list_composition.pop(0)
        count, value, constant = _mul_extract(value)
        runcount = 0
        for new_value in list_composition.copy():
            if constant:
                if isinstance(new_value, (int, float)):
                    count *= list_composition.pop(runcount)
                    continue
                runcount += 1
                continue
            newcount, newvalue = _mul_extract(new_value)[0:2]
            if newvalue == value:
                count += newcount
                list_composition.pop(runcount)
                continue
            runcount += 1
            continue
        if constant:
            if count == 0:
                return 0
            if count != 1:
                run_list_composition.append(count)
        else:
            if count != 0:
                if count != 1:
                    run_list_composition.append(('pow', (value, count)))
                else:
                    run_list_composition.append(value)
    if len(run_list_composition) == 0:
        return 1
    if len(run_list_composition) ==1:
        return run_list_composition[0]
    return ('mul', tuple(set(run_list_composition)))

@_lookup_alias(operations, 'pow')
def _simplify_pow(composition:tuple)->tuple: ##TODO: _simplify_pow method is not quite finished
    assert len(composition) == 2
    assert len(composition[1]) == 2
    assert composition[0] == 'pow'
    
    if isinstance(composition[1][0], (int, float)) and isinstance(composition[1][1], (int, float)):
        return composition[1][0]**composition[1][1]
    return composition

@_lookup_alias(operations, 'nest')
def _simplify_nest(composition:tuple)->tuple:
    assert len(composition) == 2
    assert len(composition[1]) == 2
    assert composition[0] == 'nest'
    if isinstance(composition[1][1], (int, float)):
        return composition[1][0](composition[1][1])
    return composition

def _simplify(composition:tuple)->tuple:
    if verbose:
        print()
        print()
        print(composition)
    if type(composition) is not tuple: return composition
    if len(composition) != 2:
        raise ValueError(f'length of {composition} != 2')
    composition = (composition[0], tuple(map(_simplify, composition[1])))
    return operations[composition[0]](composition)


### STRING TOOLS ###
def view_string(composition):
    return tup_to_str(composition).replace('<x>', 'x')

def function_string(composition):
    return tup_to_str(composition)

def tup_to_str(composition:tuple) -> str:
    data_type = composition[0]
    data = composition[1]
    if data_type == 'add':
        return '+'.join(map(expression_str, data)).replace('+-', '-')
    if data_type == 'mul':
        return '*'.join(map(p_expression_str, data))
    if data_type == 'pow':
        return p_expression_str(data[0])+'**'+p_expression_str(data[1])
    if data_type == 'nest':
        return expression_str(data[0]).replace('<x>', expression_str(data[1]))

def expression_str(comp)->str:
    if isinstance(comp, (int, float)):
        return str(comp)
    if callable(comp):
        try: return comp.function
        except:return comp.__name__+'(<x>)'
    if isinstance(comp, tuple):
        return tup_to_str(comp)
    raise ValueError(f'Invalid input, {comp}')

def p_expression_str(comp)->str:
    if isinstance(comp, (int, float)):
        return str(comp)
    if callable(comp):
        try: return comp.function
        except: return comp.__name__ + '(<x>)'
    return '('+expression_str(comp)+')'

def from_str(string):
    return NotImplemented

@cache
def tup_to_func(comp):
    if callable(comp):
        return comp
    _simplify(comp)
    callables = {n.__name__:n for n in set(_flatten(comp)) if callable(n)}
    return eval('lambda x : '+view_string(comp), callables)

def binomial_coeficient(k, n):
    return _math.factorial(n)/(_math.factorial(n-k)*_math.factorial(k))

if __name__ == '__main__':
    verbose = True
    identity = lambda x:x
    identity.function = '<x>'
    test1 = ('mul', (('add', (identity, 3)), ('add', (identity, 3))))
