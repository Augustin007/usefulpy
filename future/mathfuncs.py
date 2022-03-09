'''
mathfunc

DESCRIPTION
This file implements a cas system that works with a series of new types and the use of wrappers
around standard and custom math functions.

LICENSE PLATAFORMS and INSTALLATION:
This is a section of usefulpy. See usefulpy.__init__ and usefulpy license
file

RELEASE NOTES:
0
 0.0
  Version 0.0.0:
   Merging of eq, mathfunc, and Expression classes into one class in one file.
  Version 0.0.1:
   bugfixes
 0.1
  Version 0.1.0:
   Improved useability, ability to calculate derivatives.
   Recursiveness battled
   more versatility
   trig func and inverse trig func decorators
   functions moved here
  Version 0.1.1:
   Small bugfixes. Changing small internal bits.
   Documentation
1
 1.0
  Version 1.0.0:
   Reimplemented CAS system, removed expression_check, now supports multiple
   variables using the cas_variable class.
   __all__ added.
  1.1
   Version 1.1.0:
    Adds hooks and new features to CAS
'''

if __name__ == '__main__':  # To account for relative imports when run
    __package__ = 'usefulpy.mathematics'

# SETUP FOR TESTING #
import logging

if __name__ == '__main__':
    print('Debug: 10', 'Info: 20', 'Warn: 30', 'Error: 40', 'Critical: 50', sep='\n')
    level = input('enter logging level: ')
    if level == '':
        level = '30'
    while not level.isnumeric():
        level = input('Invalid\nenter logging level: ')
        if level == '':
            level = '30'
    lvl = int(level)
    fmt = '[%(levelname)s] %(name)s - %(message)s'
    logging.basicConfig(format=fmt, level=lvl)

# IMPORTS #
# Relative imports
from .. import validation
from .. import decorators
# Utilities
from abc import abstractmethod
import types
import typing
from functools import cache, wraps
from contextlib import suppress
from collections import OrderedDict
# Maths
import math
import cmath
from decimal import Decimal
from fractions import Fraction
from numbers import Number

# CHECKS #

constants = (int, float, complex, Decimal, Fraction, Number)
exact_constants = (int, Fraction)


def is_constant(n) -> bool:
    '''Checks whether n is constant for cas engine'''
    if isinstance(n, constants):
        return True
    try:
        return bool(n.is_constant())
    except AttributeError:
        return False


def is_rational(n):
    if isinstance(cas_exact, *constants):
        return True
    try:
        return bool(n.is_rational())
    except AttributeError:
        return False


def is_exact(n):
    if isinstance(cas_exact_object, *constants):
        return True
    try:
        return bool(n.is_exact())
    except AttributeError:
        return False


# DATA HANDLING #

def create_variables(*names):
    return tuple(map(cas_variable, names))


def remove_duplicates(tup):
    return tuple(OrderedDict.fromkeys(tup).keys())


def get_args(args, selector):
    '''get args according to selector'''
    return [args[select] for select in selector]

# TYPE VALIDATION AND CONVERSION TOOLS #


def cas_safe(n):
    if type(n) is mathfunc:
        n = n.composition
    if isinstance(n, cas_variable):
        if n.value is not None:
            n = n.value
    if is_constant(n):
        if not isinstance(n, cas_exact_object):
            logging.debug(f'converting {n} to cas_exact')
            try:
                return cas_exact(n)
            except Exception as error:
                logging.warn(f'{error.__class__.__name__}: {error.args[0]}')
        return n
    if isinstance(n, cas_function):
        return n
    if isinstance(n, (cas_expression)):
        return n._evaluate()
    if not isinstance(n, cas_object):
        raise TypeError(f'Invalid CAS types, {type(n)}')
    if callable(n):
        return n(*map(cas_safe, n.args))
    return n

# ALTERNATE STRING TOOLS #


def getLaTeX(value):
    if hasattr(value, 'LaTeX'):
        LaTeX = value.LaTeX
        if callable(LaTeX):
            return LaTeX()
        return LaTeX
    return str(value)


def print_raw_LaTeX(value):
    print(getLaTeX(value))


def evaluateable_string(value):
    if hasattr(value, 'evalstr'):
        evalstr = value.evalstr
        if callable(evalstr):
            return evalstr()
        return evalstr
    return str(value)

# MATH TOOLS #


def _comp_derive(n, var, k):
    '''Computes the kth partial derivative of n with respect to var'''
    # Making sure k is valid
    assert k >= 0
    assert type(k) is int

    # 0th derivative means nothing
    if k == 0:
        return n

    # logging computation
    log = f'Computing {k} partial of {str(n)} with respect to {var.name}'
    logging.info(log)

    # catch trivial and identity derivatives
    if k == 1 and var == n:
        return 1

    elif is_constant(n) or isinstance(n, cas_variable):
        return 0

    # Call attributes
    if isinstance(n, (cas_expression, cas_function)):
        return n._comp_derive(var, k)

    raise TypeError(f'Invalid type, type {type(n)}')


def _mul_derive_expansion(f, g, v, k, n):
    f_p = _comp_derive(f, v, n)
    g_p = _comp_derive(g, v, k-n)
    c_p = binomial_coeficient(n, k)
    return mul_expression((c_p, f_p, g_p))


def binomial_coeficient(k, n):
    return math.factorial(n)/(math.factorial(n-k)*math.factorial(k))

# DECORATORS #


def hook(name: str, varnum: int=None, r: bool=False, riter: tuple[int]=(), preface: str='', ignore: tuple[int]=(), custom: dict[int: str]={}):
    '''hook

    Create a decorator that intercepts calls to the given function and checks for `hooks` within the arguments
    to redirect it towards another function. If new function returns NotImplemented then it will default to original
    function

    Parameters
    ----------
    name : str
        Base name of hook
    varnum : int, optional
        Number of input variables to hook, by default None
    r : bool, optional
        reversed (add hooking compared to radd hooking), by default False
    riter : tuple[int], optional
        Individually reversed cases, integers refers to individual arguments so (0, 2, 3)
        would reverse the 0, 2, and 3 indeces, by default ()
    preface : str, optional
        Add a prefact to all default and r hooks, by default empty string.
    ignore : tuple[int], optional
        ignored cases, by default ()
    custom : dict[int : str], optional
        individually custom hooks or tags to look for, by default {}
    '''
    if type(name) is not str:
        raise TypeError(f'Invalid type recieved for argument `name`, recieved {type(name)} and not str')
    if varnum is not None:
        if type(varnum) is not int:
            raise TypeError(f'Invalid type recieved for argument `varnum`, recieved {type(varnum)} and not int')
    if type(r) is not bool:
        raise TypeError(f'Invalid type recieved for argument `r`, recieved {type(r)} and not bool')
    if type(riter) is not tuple:
        raise TypeError(f'Invalid type recieved for argument `riter` recieved {type(riter)} and not tuple')
    if not all(map(lambda x: type(x) is int, riter)):
        raise ValueError('All values of `riter` must be int')
    if type(ignore) is not tuple:
        raise TypeError(f'Invalid type recieved for argument `ignore` recieved {type(ignore)} and not tuple')
    if not all(map(lambda x: type(x) is int, ignore)):
        raise ValueError('All values of `ignore` must be int')
    fhook = f'__{preface}{"r" if r else ""}{name}hook__'
    bhook = f'__{preface}{"r" if not r else ""}{name}hook__'

    def decorator(function):
        lvarnum = varnum if varnum is not None else function.__code__.co_varnames
        attrs = tuple([custom.get(n, fhook if n not in riter else bhook) if n not in ignore else None for n in range(lvarnum)])

        @wraps(function)
        def wrapper(*args):
            for arg, attr in zip(args, attrs):
                if hasattr(arg, attr):
                    value = getattr(arg, attr)(*args)
                    if value is not NotImplemented:
                        return value
            return function(*args)
        return wrapper
    return decorator


def math_return_dec(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return_val = function(*args, **kwargs)
            return cas_object._math_return(return_val)
        except Exception as error:
            logging.error(f'{error.__class__.__name__}: {error.args[0]}')
            return NotImplemented
    return wrapper


def log_call(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        logging.debug(f'{function.__name__} called with args {args} and kwargs {kwargs}')
        return function(*args, **kwargs)
    return wrapper


class CAS:
    pass


class cas_object(CAS):
    pass


class cas_callable:
    pass


class cas_variable(cas_object):
    pass


class cas_exact_object(CAS):
    pass


class cas_constant(cas_exact_object):
    pass


class cas_exact(cas_exact_object):
    pass


class cas_expression(cas_object):
    pass


class cas_exact_expression(cas_exact_object):
    pass


class commutative_expression(cas_expression, tuple):
    pass


class non_commutative_expression(cas_expression):
    pass


class cas_exact_commutative_expression(cas_exact_expression, tuple):
    pass


class cas_exact_non_commutative_expression(cas_exact_expression):
    pass


class add_exact_expression(cas_exact_commutative_expression):
    pass


class cas_d:
    pass


class cas_differentiator(cas_expression):
    pass


class cas_differential(CAS):
    pass


class cas_limit(cas_expression):
    pass


class cas_integrator(CAS):
    pass


class add_expression(commutative_expression):
    pass


add_exact_expression.cas_inexact = add_expression


class mul_exact_expression(cas_exact_commutative_expression):
    pass


class mul_expression(commutative_expression):
    pass


mul_exact_expression.cas_inexact = mul_expression


class div_exact_shortcut(cas_exact_non_commutative_expression):
    pass


class div_shortcut(non_commutative_expression):
    pass


class pow_exact_expression(cas_exact_non_commutative_expression):
    pass


class pow_expression(non_commutative_expression):
    pass


class cas_exact_nest(cas_exact_expression):
    pass


class cas_function:
    pass


def cas_func_wrap(func):
    '''Wraps a function to make it work in the cas engine.'''

    @wraps(func)
    def wrap(*args):
        if all(map(is_constant, args)):
            if any(map(is_exact, args)):
                return cas_exact_nest(wrap, args)
            return func(*args)
        return mathfunc(cas_function(wrap, args))

    wrap.original = func
    wrap = cas_callable(wrap)
    wrap.original = func
    wrap.prime = {}
    wrap.format = None
    wrap.prime_cycle = {}
    return wrap


class mathfunc(cas_object):
    pass
