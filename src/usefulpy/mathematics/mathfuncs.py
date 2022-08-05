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
   Version 1.1.1:
    Bugfixes and more thorough documentation.
'''

if __name__ == '__main__':  # To account for relative imports when run directly
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
from functools import wraps
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
MathAttributes = ('__add__', '__radd__', '__sub__', '__mul__', '__rsub__', '__rmul__',
                  '__truediv__', '__rtruediv__', '__pow__', '__rpow__')


def is_constant(n) -> bool:
    '''Checks whether n is constant for cas engine'''
    if isinstance(n, constants):
        return True
    if 'is_constant' in dir(n):
        with suppress(Exception):
            if callable(n.is_constant):
                return bool(n.is_constant())
            else:
                return bool(n.is_constant)
    if isinstance(n, (mathfunc, cas_function, cas_object)):
        return False
    if all(map(lambda x: hasattr(n, x), MathAttributes)):
        return True
    return False


def is_rational(n):
    '''Checks whether n is rational for cas engine'''
    return isinstance(n, (cas_exact, *constants))


def is_exact(n):
    '''Checks whether a number is stored 'exactly' in the engine'''
    return isinstance(n, cas_exact_object)


# DATA HANDLING #
def create_variables(*names):
    '''Creates CAS variables for a set of names.
Intended usage: x, y, z = create_variables('x', 'y', 'z')'''
    return tuple(map(cas_variable, names))


def remove_duplicates(tup):
    '''Removes duplicates from a list'''
    return tuple(OrderedDict.fromkeys(tup).keys())


def get_args(args, selector):
    '''get args according to selector'''
    return [args[select] for select in selector]


def getValue(n):
    '''gets 'value' attribute when value exists and is not None'''
    if hasattr(n, 'value') and n.value is not None:
        return n.value
    return n


# TYPE VALIDATION AND CONVERSION TOOLS #
def cas_safe(n):
    '''Makes sure n can be used in CAS, tries to return a 'safe' version of n'''
    if type(n) is mathfunc:
        # mathfunc is just a wrapper. Not a functioning part of CAS.
        n = n.composition
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
    if not isinstance(n, cas_object):
        raise TypeError(f'Invalid CAS types, {type(n)}')
    return n


def _get(current):
    '''gets current according to variable values'''
    if is_constant(current):
        return current
    if isinstance(current, cas_variable):
        return current.value
    if type(current) is mathfunc:
        return _get(current.composition)
    if isinstance(current, cas_expression):
        return current._evaluate()
    if callable(current):
        return current.func(*map(_get, current.args))
    return current


# ALTERNATE STRING TOOLS #

def getLaTeX(value):
    '''Gets LaTeX representation of value'''
    if hasattr(value, 'LaTeX'):
        LaTeX = value.LaTeX
        if callable(LaTeX):
            return LaTeX()
        return LaTeX
    return str(value)


def print_raw_LaTeX(value):
    ''''Utility for easier copy/pasting'''
    print(getLaTeX(value))


def evaluateable_string(value):
    '''Generates evaluateable string representation of CAS expression'''
    if hasattr(value, 'evalstr'):
        evalstr = value.evalstr
        if callable(evalstr):
            return evalstr()
        return evalstr
    return str(value)


# MATH TOOLS #

def _comp_derive(n, var, k):
    '''Computes the kth partial derivative of n with respect to var'''
    # logging computation
    logging.info(f'Computing {k} partial of {str(n)} with respect to {var.name}')

    # Making sure k is valid
    assert k >= 0  # Integrals not implemented yet
    assert type(k) is int  # Decimal derivatives also not implemented yet

    # 0th derivative means nothing
    if k == 0:
        return n

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
    '''nth term of kth partial with respect to v of f*g'''
    f_p = _comp_derive(f, v, n)
    g_p = _comp_derive(g, v, k-n)
    c_p = binomial_coeficient(n, k)
    return mul_expression((c_p, f_p, g_p))


def binomial_coeficient(k, n):
    ''' n!/((n-k)!*k!)'''
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
        Add a prefact to all default and r hooks, by default ''.
    ignore : tuple[int], optional
        ignored cases, by default ()
    custom : dict[int : str], optional
        individually custom hooks or tags to look for, by default {}
    '''
    # Validation of input parameters
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

    # Formulating checked hooks
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
    '''Makes sure returns are cas_safe'''
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
    '''Logs all calls of wrapped function'''
    @wraps(function)
    def wrapper(*args, **kwargs):
        logging.debug(f'{function.__name__} called with args {args} and kwargs {kwargs}')
        return function(*args, **kwargs)
    return wrapper


class cas_object:
    '''Master type for cas engine, contains methods for the
standard arithmatic functions'''
    safe: typing.Any

    @staticmethod
    def _math_return(return_val):
        '''Makes return_val cas_safe'''
        if return_val is NotImplemented:
            return NotImplemented
        logging.info(f'math return: {return_val}')
        if is_constant(return_val):
            if not isinstance(return_val, cas_exact_object):
                try:
                    return cas_exact(return_val)
                except Exception as error:
                    logging.error(f'{error.__class__.__name__}: {error.args[0]}')
                    return return_val
            return return_val
        if isinstance(return_val, cas_variable):
            return return_val
        try:
            return mathfunc(return_val)
        except Exception as error:
            logging.error(f'{error.__class__.__name__}: {error.args[0]}')
            return return_val

    @log_call
    def __pos__(self):
        '''Return +self'''
        return self

    @math_return_dec
    @log_call
    def __neg__(self):
        '''Return -self'''
        return mul_expression((-1, self))

    @math_return_dec
    @hook('add', 2, False, (1,))
    @log_call
    def __add__(self, other):
        '''Return self+other'''
        return add_expression((self, other))

    @math_return_dec
    @hook('add', 2, True, (1,))
    @log_call
    def __radd__(self, other):
        '''Return other+self'''
        return self+other

    @math_return_dec
    @hook('sub', 2, False, (1,))
    @log_call
    def __sub__(self, other):
        '''Return self-other'''
        return self+(-other)

    @math_return_dec
    @hook('sub', 2, True, (1,))
    @log_call
    def __rsub__(self, other):
        '''Return other-self'''
        return other+(-self)

    @math_return_dec
    @hook('mul', 2, False, (1,))
    @log_call
    def __mul__(self, other):
        '''Return self*other'''
        return mul_expression((self, other))

    @math_return_dec
    @hook('mul', 2, True, (1,))
    @log_call
    def __rmul__(self, other):
        '''Return other*self'''
        return self*other

    @math_return_dec
    @log_call
    def reciprocal(self):
        '''Return 1/self'''
        return pow_expression(self, -1)

    @math_return_dec
    @hook('truediv', 2, False, (1,))
    @log_call
    def __truediv__(self, other):
        '''Return self/other'''
        if type(other) is mathfunc:
            return self*other.reciprocal()
        return div_shortcut(self, other)

    @math_return_dec
    @hook('truediv', 2, True, (1,))
    @log_call
    def __rtruediv__(self, other):
        '''Return other/self'''
        return self.reciprocal()*other

    @math_return_dec
    @hook('pow', 2, False, (1,))
    @log_call
    def __pow__(self, other):
        '''Return self**other'''
        return pow_expression(self, other)

    @math_return_dec
    @hook('pow', 2, True, (1,))
    @log_call
    def __rpow__(self, other):
        '''Return other**self'''
        return pow_expression(other, self)

    def __repr__(self):
        ''' representation string for CAS objects '''
        return f'CAS[ {self} ]'


class cas_callable:
    '''Generic function for cas_engine that implements
basic calling abilities and custom setattr getattr methods'''
    fn: tuple
    var: tuple
    __data: dict
    __doc__: str
    shortcut_function: types.FunctionType
    function: str
    __name__: str
    inverse: types.FunctionType
    interval: typing.Any
    composition: typing.Any
    exact_composition: typing.Any
    __is_frozen: bool = False
    arguments_comp: tuple
    arguments_call: tuple
    domain_restrictions: tuple
    safe: typing.Any
    custom_latex: str
    custom_composition: typing.Any

    def __new__(cls, func):
        assert callable(func)
        self = super(cas_callable, cls).__new__(cls)
        self.__data = {'inputs': {}, 'pass': {}, 'oper': {}, 'custom_data': {}}
        self.special = {'arguments_comp': self._set_args_comp}
        self.truecall = func
        self.arguments_comp = func.original.__code__.co_varnames
        self.__name__ = func.__name__
        self.func = func
        return self

    def check_domain(self, *args):
        '''Not implemented: Raises ValueError
if args are not in domain as defined by domain restrictions
or interval'''
        return NotImplemented

    @log_call
    def __call__(self, *args):
        if all(map(is_constant, args)) and not any(map(is_exact, args)):
            return self.original(*args)  # Call original function
        args = tuple(map(cas_safe, args))
        self.check_domain(args)
        if hasattr(self, '__callhook__'):
            return_val = cas_object._math_return(self.__callhook__(*args))
            if return_val is not NotImplemented:
                return return_val
        for varname, a in zip(self.arguments_comp, args):
            if hasattr(a, 'hook_intercept'):
                idict = self.__data['inputs'][varname]
                if a.hook_intercept in idict:
                    return_val = cas_object._math_return(idict[a.hook_intercept](*args))
                    if return_val is not NotImplemented:
                        return return_val
        return self.truecall(*args)

    def _get_data_copy(self):
        return self.__data.copy()

    def _get_data_item_copy(self, index):
        return self.__data[index]

    def _set_args_comp(self, value):
        for n in value:
            self.__data['inputs'][n] = {}

    def __setattr__(self, name: str, value) -> None:
        '''Intercepts attribute setting, for customized storage'''
        if self.__is_frozen:
            raise AttributeError(f'attributes of {self!r} are no longer writeable')
        if name == '__call__':
            super.__setattr__(self, name, value)
            return
        if name in {**cas_callable.__annotations__, **self.__annotations__}:
            if name in ('arguments_call', 'fn', 'var') and hasattr(self, name):
                raise AttributeError('this attribute is not writeable')
            super.__setattr__(self, name, value)
            if name in self.special:
                self.special[name](value)
            return
        if name.endswith('hook__'):
            if not callable(value):
                raise AttributeError(f'{name} attribute must be callable')
            if name.startswith('__pass'):
                vmethod = name[6:-6]
                for var in self.arguments_comp:
                    if vmethod.startswith(var):
                        self.__data['inputs'][var][vmethod[len(var):]] = value
                        return
                raise ValueError('Invalid name')
            if name.startswith('__'):
                self.__data['oper'][name[2:-6]] = value
                return
        self.__data['custom_data'][name] = value

    def __getattr__(self, name):
        '''Customized attribute storage also necesitates custom attribute lookup'''
        if name.endswith('hook__'):
            if name.startswith('__pass'):
                vmethod = name[6:-6]
                for var in self.arguments_comp:
                    with suppress(KeyError):
                        if vmethod.startswith(var):
                            return self.__data['inputs'][var][vmethod[len(var):]]
            if name.startswith('__'):
                with suppress(KeyError):
                    return self.__data['oper'][name[2:-6]]
        with suppress(KeyError):
            return self.__data['custom_data'][name]
        raise AttributeError(f'{self.__class__.__name__!r} object has no attribute {name!r}')

    def __repr__(self):
        ''' representation string for cas_variable '''
        return f'<Callable {self.__name__} at {hex(id(self))}'

    special: dict = {'arguments_comp': _set_args_comp}


class cas_variable(cas_object):
    '''variable class for cas engine'''

    name: str
    names: dict = {}  # stores all created variables
    value: typing.Any = None

    # INITIALIZATION #

    def __new__(cls, name):
        '''__new__ for cas_variable'''
        if name in cls.names:
            return cls.names[name]

        # Check name validity
        e = False
        try:
            assert type(name) == str
            assert len(name) in range(1, 4)
            assert '.' not in name
            exec(f'{name}=0')
        except Exception:
            e = True
        if e:
            raise ValueError(f'Invalid name recieved: {name!r}')

        # create and log the variable
        logging.info(f'Variable created: {name!r}')
        self = super(cas_variable, cls).__new__(cls)

        self.name = name
        self.names[name] = self

        return self

    # SET/RESET #
    # set and reset for internal capabilities

    def _set(self, value):
        self.value = value

    def _reset(self):
        self.value = None

    # CONVERSIONS #

    def __str__(self):
        ''' str for cas_variable '''
        return self.name


class cas_exact_object:
    '''Master class for constants'''
    value: typing.Any

    def __pos__(self):
        '''Return +self'''
        return self

    @math_return_dec
    @log_call
    def __neg__(self):
        '''Return -self'''
        try:
            return cas_exact(-self.value)
        except Exception:
            return mul_exact_expression((-1, self.value))

    @math_return_dec
    @hook('add', 2, False, (1,), 'exact')
    @log_call
    def __add__(self, other):
        '''Return self+other'''
        if is_rational(other) and is_rational(self):
            if type(other) is not cas_exact:
                other = cas_exact(other)
            return self.value + other.value
        return add_exact_expression((self, other))

    @math_return_dec
    @hook('add', 2, True, (1,), 'exact')
    @log_call
    def __radd__(self, other):
        '''Return other+self'''
        return self+other

    @math_return_dec
    @hook('sub', 2, False, (1,), 'exact')
    @log_call
    def __sub__(self, other):
        '''Return self-other'''
        return self+(-other)

    @math_return_dec
    @hook('sub', 2, True, (1,), 'exact')
    @log_call
    def __rsub__(self, other):
        '''Return other-self'''
        return other+(-self)

    @math_return_dec
    @hook('mul', 2, False, (1,), 'exact')
    @log_call
    def __mul__(self, other):
        '''Return self*other'''
        if is_rational(other) and is_rational(self):
            if type(other) is not cas_exact:
                other = cas_exact(other)
            return self.value * other.value
        return mul_exact_expression((self, other))

    @math_return_dec
    @hook('mul', 2, True, (1,), 'exact')
    @log_call
    def __rmul__(self, other):
        '''Return other*self'''
        return self*other

    @math_return_dec
    @log_call
    def reciprocal(self):
        '''Return 1/self'''
        return pow_exact_expression(self, -1)

    @math_return_dec
    @hook('truediv', 2, False, (1,), 'exact')
    @log_call
    def __truediv__(self, other):
        '''Return self/other'''
        if type(other) is mathfunc:
            return self*other.reciprocal()
        return div_exact_shortcut(self, other)

    @math_return_dec
    @hook('truediv', 2, True, (1,), 'exact')
    @log_call
    def __rtruediv__(self, other):
        '''Return other/self'''
        return self.reciprocal()*other

    @math_return_dec
    @hook('pow', 2, False, (1,), 'exact')
    @log_call
    def __pow__(self, other):
        '''Return self**other'''
        return pow_exact_expression(self, other)

    @math_return_dec
    @hook('pow', 2, True, (1,), 'exact')
    @log_call
    def __rpow__(self, other):
        '''Return other**self'''
        return pow(other, self)

    def is_constant(self):
        return True

    def __eq__(self, other):
        if hasattr(other, 'value'):
            return self.value == other.value
        return self.value == other

    def __repr__(self):
        ''' representation string for CAS objects '''
        return f'CAS[ {self} ]'


class cas_constant(cas_exact_object):
    '''constant class for cas engine'''

    name: str
    names: dict = cas_variable.names  # stores all created variables
    value: typing.Any = None
    LaTeX: str

    # INITIALIZATION #

    def __new__(cls, name, value, LaTeX=None):
        '''__new__ for cas_variable'''
        assert is_constant(value)
        if name in cls.names:
            return cls.names[name]

        # Check name validity
        e = False
        try:
            assert type(name) == str
            assert len(name) in range(1, 4)
            assert '.' not in name
            exec(f'{name}=0')
        except Exception:
            e = True
        if e:
            raise ValueError(f'Invalid name recieved: {name!r}')

        # create and log the variable
        logging.info(f'Constant created: {name!r}')
        self = super(cas_constant, cls).__new__(cls)

        if LaTeX is None:
            LaTeX = name

        self.name = name
        self.names[name] = self
        self.value = value
        self.LaTeX = LaTeX

        return self

    # CONVERSIONS #
    def __str__(self):
        ''' str for cas_variable '''
        return self.name

    def evalstr(self):
        '''evaluateable_string'''
        return str(self.value)

    def __float__(self):
        return float(self.value)

    def __int__(self):
        return int(self.value)


class cas_exact(cas_exact_object):
    '''Stores an exact version of a variable as an int or Fraction'''
    def __init__(self, value):
        if validation.is_integer(value):
            self.value = int(float(value))
            return
        elif isinstance(value, (Decimal, Fraction)):
            self.value = Fraction(value)
            return
        elif validation.is_float(value):
            self.value = Fraction(str(value))
            return
        elif type(value) is str:
            n = value.split('/')
            if len(n) == 2:
                if validation.are_integers(*n):
                    self.value = Fraction(int(n[0]), int(n[1]))
                    return
                if validation.are_floats(*n):
                    self.value = Fraction(str(n[0]/n[1]))
                    return
        raise TypeError('Invalid Type')

    def __str__(self):
        return str(self.value)

    def __float__(self):
        return float(self.value)

    def __int__(self):
        return int(self.value)


class cas_expression(cas_object):
    oper: str
    hook_intercept: str
    cas_exact: typing.Any

    @abstractmethod
    def _simplify(self, /):
        '''abstract method: called during initialization
Return a simplified version of current expression'''
        pass

    @abstractmethod
    def _comp_derive(self, k, /):
        '''abstract method: called by external _comp_derive
Return cas derivative of self'''
        pass

    def evaluate(self, *args):
        '''Return self evaluated with args as values for variables'''
        if len(self.var) != len(args):
            raise ValueError('Incorrect number of arguments entered')
        for arg, var in zip(args, self.var):
            var._set(arg)
        value = self._evaluate()
        for var in self.var:
            var._reset()
        return value

    @abstractmethod
    def _evaluate(self, /):
        '''abstract method: called by __call__
Return self evaluated at values of variables'''
        pass

    @abstractmethod
    def __str__(self, /):
        '''abstract method: called by str
Return self converted into a string'''
        pass


class cas_exact_expression(cas_exact_object):
    @abstractmethod
    def _simplify(self, /):
        '''abstract method: called during initialization
Return a simplified version of current expression'''
        pass

    def _comp_derive(self, k, n, /):
        '''Return cas derivative of self'''
        return 0

    @abstractmethod
    def __str__(self, /):
        '''abstract method: called by str
Return self converted into a string'''
        pass


class commutative_expression(cas_expression, tuple):
    LaTeXoper: str

    def __new__(cls, iterable=()):
        '''__new__ for any communative expressions'''
        iterable = tuple(map(cas_safe, iterable))
        if all(map(is_constant, iterable)):
            return cls.cas_exact(iterable)
        self = tuple.__new__(cls, map(cas_safe, iterable))
        self = self._simplify()
        if not isinstance(self, cls):
            return self
        check = self._check_hooks()
        if check is not NotImplemented:
            return check
        if not isinstance(self, cls):
            return self

        # Creating a list of all involved variables for reference.
        var = []
        for n in self:
            if type(n) is cas_variable:
                var.append(n)
            elif isinstance(n, cas_expression):
                var.extend(n.var)
            elif callable(n):
                var.extend(n.var)
        self.var = remove_duplicates(var)

        # Creating a list of all involved functions for reference.
        fn = []
        for n in self:
            if isinstance(n, cas_expression) or callable(n):
                fn.extend(n.fn)
        self.fn = remove_duplicates(fn)
        return self

    def __eq__(self, other, /):
        ''' Return self==other'''
        if isinstance(other, cas_expression):
            if self.oper == other.oper:
                return set(self) == set(other)
        return False

    def _expand(self, /):
        ''' Expands according to assosiative property'''
        for n in self:
            if type(n) == type(self):
                yield from n
                continue
            yield n

    def _extract_num(self, /):
        ''' seperates constant and non-constant values'''
        numbers = []
        expressions = []
        for n in self._expand():
            if is_constant(n):
                numbers.append(n)
                continue
            expressions.append(n)
        return numbers, expressions

    def __hash__(self, /):
        '''hash for communative expression '''
        return hash((self.oper, tuple(self)))

    def __str__(self, /):
        '''string for communative expression'''
        return '('+self.oper.join(map(str, self))+')'

    def evalstr(self):
        return '('+self.oper.join(map(evaluateable_string, self))+')'

    def _evaluate(self):
        '''evaluate self at values of variables'''
        return self.__class__(map(_get, self))

    def LaTeX(self):
        return '{'+f'}}{self.LaTeXoper}{{'.join(map(getLaTeX, self))+'}'


class non_commutative_expression(cas_expression):
    var: tuple
    fn: tuple

    @abstractmethod
    def __eq__(self, other):
        '''eq for non-commutative expression'''
        pass

    @abstractmethod
    def __hash__(self):
        '''hash'''
        pass

    @abstractmethod
    def _evaluate(self):
        pass


class cas_exact_commutative_expression(cas_exact_expression, tuple):
    oper: str
    hook_intercept: str
    cas_inexact: typing.Any
    true_operation: typing.Any
    value: typing.Any
    LaTeXoper: str
    start: typing.Any

    def __new__(cls, iterable=()):
        '''__new__ for any communative expressions'''
        iterable = tuple(map(cas_safe, iterable))
        if not all(map(is_constant, iterable)):
            return cls.cas_inexact(iterable)
        self = tuple.__new__(cls, map(cas_safe, iterable))
        self = self._simplify()

        if not isinstance(self, cls):
            return self

        run = cls.start
        for n in iterable:
            if hasattr(n, 'value'):
                run = cls.true_operation(run, n.value)
                continue
            run = cls.true_operation(run, n)
        self.value = run
        return self

    def __eq__(self, other, /):
        ''' Return self==other'''
        if hasattr(other, 'value'):
            return self.value == other.value
        return self.value == other

    def _expand(self, /):
        ''' Expands according to assosiative property'''
        for n in self:
            if type(n) == type(self):
                yield from n
                continue
            yield n

    def __hash__(self, /):
        '''hash for communative expression '''
        return hash(self.value)

    def __str__(self, /):
        return self.oper.join(map(str, self))

    def evalstr(self, /):
        '''string for communative expression'''
        return '('+evaluateable_string(self.value)+')'

    def _extract_num(self, /):
        ''' seperates rationals from non-rational expressions'''
        rationals = []
        nonrationals = []
        for n in self._expand():
            if is_rational(n):
                rationals.append(n)
                continue
            nonrationals.append(n)
        return rationals, nonrationals

    def LaTeX(self):
        return '{'+f'}}{self.LaTeXoper}{{'.join(map(getLaTeX, self))+'}'


class cas_exact_non_commutative_expression(cas_exact_expression):
    pass


class add_exact_expression(cas_exact_commutative_expression):
    oper = '+'
    LaTeXoper = '+'
    hook_intercept = 'add'
    true_operation = lambda x, y: x+y
    start = 0

    def _simplify(self, /):
        '''Simplifies addition expression'''
        # Fast cases
        if len(self) == 1:
            return self[0]
        if len(self) == 0:
            return 0

        # Seperates rationals out
        numbers, expressions = self._extract_num()
        # adds rationals
        number = sum(numbers)
        # extracts count, value data from expressions
        expressions_extract = list(map(self._data_extract, expressions))

        # Loop through creating a new list of simplified data
        expressions_short = []
        while expressions_extract:
            count, value = expressions_extract.pop(0)
            runcount = 0
            for new_count, new_value in tuple(expressions_extract):
                if new_value == value:
                    count += new_count
                    expressions_extract.pop(runcount)
                    continue
                runcount += 1
                continue
            if count != 0:
                if count != 1:
                    expressions_short.append(mul_exact_expression((count, value)))
                    continue
                expressions_short.append(value)

        # Return clean results
        if len(expressions_short) == 0:
            return number
        if number == 0:
            if len(expressions_short) == 1:
                return expressions_short[0]
            return tuple.__new__(self.__class__, expressions_short)
        return tuple.__new__(self.__class__, (number, *expressions_short))

    def _data_extract(self, value, /):
        '''extracts count and truevalue data from value'''
        if isinstance(value, cas_exact_expression):
            if value.oper == '*':
                value_sub = value._extract_num()
                return math.prod(value_sub[0]), mul_expression(value_sub[1])
            # pow value count not implemented
            return 1, value

        if isinstance(value, cas_constant):
            return 1, value
        raise TypeError(f'invalid type recieved: type {type(value)}')

    def _comp_derive(self, var, k, /):
        '''computes kth partial of self with respect to var'''
        return 0


class add_expression(commutative_expression):
    oper = '+'
    hook_intercept = 'add'
    LaTeXoper = '+'
    cas_exact = add_exact_expression

    def _simplify(self, /):
        '''Simplifies addition expression'''
        # Fast cases
        if len(self) == 1:
            return self[0]
        if len(self) == 0:
            return 0

        # Seperates constants out
        numbers, expressions = self._extract_num()
        # adds constants
        number = add_exact_expression(numbers)
        # extracts count, value data from expressions
        expressions_extract = list(map(self._data_extract, expressions))

        # Loop through creating a new list of simplified data
        expressions_short = []
        while expressions_extract:
            count, value = expressions_extract.pop(0)
            runcount = 0
            for new_count, new_value in tuple(expressions_extract):
                if new_value == value:
                    count += new_count
                    expressions_extract.pop(runcount)
                    continue
                runcount += 1
                continue
            if count != 0:
                if count != 1:
                    expressions_short.append(mul_expression((count, value)))
                    continue
                expressions_short.append(value)

        # Return clean results
        if len(expressions_short) == 0:
            return number
        if number == 0:
            if len(expressions_short) == 1:
                return expressions_short[0]
            return tuple.__new__(self.__class__, expressions_short)
        return tuple.__new__(self.__class__, (number, *expressions_short))

    def _check_hooks(self):
        for i, n in enumerate(self):
            if isinstance(n, cas_function):
                if hasattr(n.func, '__addcheckhook__'):
                    return n.func.__addcheckhook__(self)
        return NotImplemented

    def _data_extract(self, value, /):
        '''extracts count and truevalue data from value'''
        if type(value) is mathfunc:
            value = value.composition

        if isinstance(value, cas_expression):
            if value.oper == '*':
                value_sub = value._extract_num()
                return math.prod(value_sub[0]), mul_expression(value_sub[1])
            # pow value count not implemented
            return 1, value

        if isinstance(value, cas_function):
            return 1, value

        if isinstance(value, cas_variable):
            return 1, value
        raise TypeError(f'invalid type recieved: type {type(value)}')

    def _comp_derive(self, var, k, /):
        '''computes kth partial of self with respect to var'''
        return add_expression(map(lambda x: _comp_derive(x, var, k), self))


add_exact_expression.cas_inexact = add_expression


class mul_exact_expression(cas_exact_commutative_expression):
    oper = '*'
    hook_intercept = 'mul'
    true_operation = lambda x, y: x*y
    start = 1
    LaTeXoper = ''

    def _simplify(self, /):
        '''Simplifies multiplication expression'''
        # fast return
        if len(self) == 1:
            return self[0]
        if len(self) == 0:
            return 1
        if 0 in self:
            return 0

        # expands accross addition expressions within it
        for count, value in enumerate(self):
            if type(value) == add_expression:

                def distributor(x):
                    data = (x, *self[: count], *self[count+1:])
                    return mul_expression(data)

                run = tuple(map(distributor, value))
                return add_expression(run)

        # extracts rationals
        numbers, expressions = self._extract_num()
        # product of rationals
        number = math.prod(numbers)
        # extracts count value information from expressions
        expressions_extract = list(map(self._data_extract, expressions))

        # Loop through creating a list of simplified data
        expressions_short = []
        while expressions_extract:
            count, value = expressions_extract.pop(0)
            runcount = 0
            for new_count, new_value in tuple(expressions_extract):
                if new_value == value:
                    count += new_count
                    expressions_extract.pop(runcount)
                    continue
                runcount += 1
                continue
            if count != 0:
                if count != 1:
                    expressions_short.append(pow_expression(value, count))
                    continue
                expressions_short.append(value)

        # Return clean results
        if len(expressions_short) == 0:
            return number
        if number == 1:
            if len(expressions_short) == 1:
                return expressions_short[0]
            return tuple.__new__(self.__class__, expressions_short)
        return tuple.__new__(self.__class__, (number, *expressions_short))

    def _data_extract(self, value, /):
        ''' Extract count and truevalue from data'''
        if isinstance(value, cas_exact_expression):
            if value.oper == '**':
                if is_constant(value.b):
                    return value.b, value.a
            return 1, value

        if isinstance(value, cas_constant):
            return 1, value

        raise TypeError(f'invalid type recieved: type {type(value)}')

    def _comp_derive(self, var, k, /):
        return 0


class mul_expression(commutative_expression):
    oper = '*'
    hook_intercept = 'mul'
    cas_exact = mul_exact_expression
    LaTeXoper = ''

    def _simplify(self, /):
        '''Simplifies multiplication expression'''
        # fast return
        if len(self) == 1:
            return self[0]
        if len(self) == 0:
            return 1
        if 0 in self:
            return 0

        # expands accross addition expressions within it
        for count, value in enumerate(self):
            if type(value) == add_expression:

                def distributor(x):
                    data = (x, *self[: count], *self[count+1:])
                    return mul_expression(data)

                run = tuple(map(distributor, value))
                return add_expression(run)

        # extracts constants
        numbers, expressions = self._extract_num()
        # product of constants
        number = mul_exact_expression(numbers)
        # extracts count value information from expressions
        expressions_extract = list(map(self._data_extract, expressions))

        # Loop through creating a list of simplified data
        expressions_short = []
        while expressions_extract:
            count, value = expressions_extract.pop(0)
            runcount = 0
            for new_count, new_value in tuple(expressions_extract):
                if new_value == value:
                    count += new_count
                    expressions_extract.pop(runcount)
                    continue
                runcount += 1
                continue
            if count != 0:
                if count != 1:
                    expressions_short.append(pow_expression(value, count))
                    continue
                expressions_short.append(value)

        # Return clean results
        if len(expressions_short) == 0:
            return number
        if number == 1:
            if len(expressions_short) == 1:
                return expressions_short[0]
            return tuple.__new__(self.__class__, expressions_short)
        return tuple.__new__(self.__class__, (number, *expressions_short))

    def _data_extract(self, value, /):
        ''' Extract count and truevalue from data'''
        if type(value) is mathfunc:
            value = value.composition

        if isinstance(value, cas_expression):
            if value.oper == '**':
                if is_constant(value.b):
                    return value.b, value.a
            return 1, value

        if callable(value):
            return 1, value

        if isinstance(value, cas_variable):
            return 1, value

        raise TypeError(f'invalid type recieved: type {type(value)}')

    def _comp_derive(self, var, k, /):
        '''computes kth partial of self with respect to var'''
        a, b = self._extract_num()
        n = math.prod(a)
        if len(b) > 2:
            length = len(b)
            f = mul_expression(b[: length//2])
            g = mul_expression(b[length//2:])
        else:
            if len(b) == 1:
                return mul_expression((n, _comp_derive(b[0], var, k)))
            f = b[0]
            g = b[1]
        terms = [_mul_derive_expansion(f, g, var, k, n) for n in range(k+1)]
        return add_expression(terms)

    def _check_hooks(self):
        for i, n in enumerate(self):
            if isinstance(n, cas_function):
                if hasattr(n.func, '__mulcheckhook__'):
                    return n.func.__mulcheckhook__(self)
        return NotImplemented


mul_exact_expression.cas_inexact = mul_expression


class div_exact_shortcut(cas_exact_non_commutative_expression):
    def __new__(cls, a, b):  # TEMPORARY actual division coming as soon as I can figure out factoring
        a = cas_safe(a)
        b = cas_safe(b)
        return a*(b**-1)


class div_shortcut(non_commutative_expression):
    def __new__(cls, a, b):  # TEMPORARY actual division coming as soon as I can figure out factoring
        return a*(b**-1)


class pow_exact_expression(cas_exact_non_commutative_expression):
    oper = '**'
    hook_intercept = 'pow'
    true_operation = lambda x, y: x**y

    def __new__(cls, a, b):
        if not (is_constant(a) and is_constant(b)):
            return pow_expression(a, b)
        a = cas_safe(a)
        b = cas_safe(b)
        if is_rational(a) and validation.is_integer(b):
            if b.value < 0:
                temp = a.value**(-b.value)
                return cas_exact(Fraction(1, temp))
            return cas_exact(a.value**b.value)
        self = super(cas_exact_non_commutative_expression, cls).__new__(cls)
        self.a = a
        self.b = b
        self.value = self.a.value**self.b.value
        return self._simplify()

    def LaTeX(self):
        return '{'+getLaTeX(self.a)+'}^{'+getLaTeX(self.b)+'}'

    def __str__(self):
        return str(self.a)+'**'+str(self.b)

    def evalstr(self):
        return evaluateable_string(self.a)+'**'+evaluateable_string(self.b)

    def _simplify(self, /):
        '''Simplifies power expression '''
        # special cases
        if self.b == 0:
            return 1
        if self.b == 1:
            return self.a
        if self.a == 0:
            return 0
        if self.a == 1:
            return 1
        if type(self.a) in (mul_expression, mul_exact_expression):
            return mul_expression(map(lambda n: pow_expression(n, self.b),
                                  self.a))
        if type(self.a) in (pow_expression, pow_exact_expression):
            return pow_expression(self.a.a,
                                  mul_expression((self.a.b, self.b)))
        return self

    def _comp_derive(self, var, k, /):
        return 0


class pow_expression(non_commutative_expression):
    oper = '**'
    hook_intercept = 'pow'
    cas_exact = remove_duplicates

    def __new__(cls, a, b):
        '''__new__ for non-communative expressions'''
        self = super(non_commutative_expression, cls).__new__(cls)
        if is_constant(a) and is_constant(b):
            return pow_exact_expression(a, b)
        if type(a) is mathfunc:
            a = a.composition
        if type(b) is mathfunc:
            b = b.composition
        # Check for constant exact types
        self.a = a
        self.b = b
        self = self._simplify()
        if type(self) is not cls:
            return self
        check = self._check_hooks()
        if check is not NotImplemented:
            return check
        var = []
        for n in (self.a, self.b):
            if type(n) == cas_variable:
                var.append(n)
            elif isinstance(n, (cas_expression, cas_function)):
                var.extend(n.var)
        self.var = remove_duplicates(var)
        fn = []
        for n in (self.a, self.b):
            if isinstance(n, cas_expression) or callable(n):
                fn.extend(n.fn)
        self.fn = remove_duplicates(fn)
        return self

    def __eq__(self, other, /):
        '''Return self==other'''
        if isinstance(other, cas_expression):
            if self.oper == other.oper:
                return(self.a, self.b) == (other.a, other.b)
        return False

    def __hash__(self, /):
        '''hash for non-communative expression'''
        return hash((self.a, self.b))

    def _evaluate(self):
        '''evaluate self at values of variables'''
        return self.__class__(_get(self.a), _get(self.b))

    def LaTeX(self):
        if isinstance(self.a, (cas_expression, cas_exact_expression)):
            return '\\left('+getLaTeX(self.a)+'\\right)^{'+getLaTeX(self.b)+'}'
        return '{'+getLaTeX(self.a)+'}^{'+getLaTeX(self.b)+'}'

    def __str__(self):
        return str(self.a)+'**'+str(self.b)

    def evalstr(self):
        return evaluateable_string(self.a)+'**'+evaluateable_string(self.b)

    def _simplify(self, /):
        '''Simplifies power expression '''
        # special cases
        if self.b == 0:
            return 1
        if self.b == 1:
            return self.a
        if self.a == 0:
            return 0
        if self.a == 1:
            return 1
        if type(self.a) in (mul_expression, mul_exact_expression):
            return mul_expression(map(lambda n: pow_expression(n, self.b),
                                  self.a))
        if type(self.a) in (pow_expression, pow_exact_expression):
            return pow_expression(self.a.a,
                                  mul_expression((self.a.b, self.b)))
        return self

    def _comp_derive(self, var, k, /):
        '''computes kth partial of self with respect to var'''
        if is_constant(self.b):
            if self.a == var:
                if k > self.b:
                    return 0
                coef = math.prod(range(self.b-k+1, self.b+1))
                return mul_expression((coef, pow_expression(var, self.b-k)))
            if isinstance(self.a, cas_variable):
                return 0
            a = self.a
            b = self.b
            first_derivative = mul_expression((b, pow_expression(a, b-1),
                                               _comp_derive(self.a, var, 1)))
            return _comp_derive(first_derivative, var, k-1)
        if is_constant(self.a):
            return _comp_derive(mul_expression((ln(self.a), self)), var, k-1)
        pross = mul_expression((ln(self.a).composition, self.b))
        internal = _comp_derive(pross, var, 1)
        return _comp_derive(mul_expression((self, internal)), var, k-1)

    def _check_hooks(self):
        if hasattr(self.a, '__powahook__'):
            return self.a.__powahook__(self)
        if hasattr(self.b, '__powbhook__'):
            return self.b.__powbhook__(self)
        return NotImplemented


class cas_exact_nest(cas_exact_expression):
    oper = '()'

    def __new__(cls, func, args):
        if hasattr(func, 'exact_hook'):
            with suppress(Exception):
                rval = func.exact_hook(args)
                if rval is not NotImplemented:
                    return rval
        self = super(cas_exact_nest, cls).__new__(cls)
        argvalues = map(getValue, args)
        self.value = func.original(*argvalues)
        self.func = func
        self.args = args
        if func.format:
            string = func.format
            for n, arg in enumerate(args):
                string = string.replace(f'<{n}>', f'{arg}')
        else:
            string = func.__name__+'('
            string += ', '.join(map(str, args))
            string += ')'
        if hasattr(func, 'custom_latex'):
            latex = func.custom_latex
            for n, arg in enumerate(args):
                latex = latex.replace(f'<{n}>', f'{arg}')
            self.LaTeX = latex
        elif hasattr(func, 'LaTeX'):
            self.LaTeX = func.LaTeX
        else:
            if hasattr(func, 'latexname'):
                latex = func.latexname+'\\left('
            elif hasattr(func, 'latexfunc') and func.latexfunc:
                latex = '\\'+func.__name__+'\\left('
            else:
                latex = func.__name__+'\\left('
            LaTeX_end = ', '.join(map(getLaTeX, args))
            self.LaTeX = f'{latex}{LaTeX_end}\\right)'
        self.string = string
        return self

    def __str__(self):
        return self.string

    def evalstr(self):
        return str(self.value)

    def _comp_derive(n, var, k):
        return 0


class cas_function:
    func: types.FunctionType
    string: str

    def __new__(cls, func, args):
        self = super(cas_function, cls).__new__(cls)
        self.func = func
        self.args = args
        self.prime = self.func.prime
        self.prime_cycle = self.func.prime_cycle
        if hasattr(func, 'custom_composition'):
            self.custom_composition = func.custom_composition
        var = []
        fn = [func]
        for arg in args:
            if is_constant(arg):
                continue
            if isinstance(arg, cas_variable):
                var.append(arg)
                continue
            if isinstance(arg, cas_expression):
                var.extend(arg.var)
                fn.extend(arg.fn)
                continue
            if isinstance(arg, cas_function):
                var.extend(arg.var)
                fn.extend(arg.fn)
                continue
        self.raw_vars = tuple(var)
        self.var = remove_duplicates(var)
        self.fn = remove_duplicates(fn)
        var_names = ', '.join(map(lambda x: x.name, self.var))
        tmd = {}
        if func.__doc__:
            exec(f'def {func.__name__}({var_names}): \
                  \t\n    """{func.__doc__}"""\n    pass ', tmd)
        else:
            exec(f'def {func.__name__}({var_names}): pass', tmd)
        self.__call__ = tmd[func.__name__]
        if func.format:
            string = func.format
            evalstr = func.format
            for n, arg in enumerate(args):
                string = string.replace(f'<{n}>', f'{arg}')
                evalstr = evalstr.replace(f'<{n}>', f'{evaluateable_string(arg)}')
        else:
            string = func.__name__+'('
            string += ', '.join(map(str, args))
            string += ')'
            evalstr = func.__name__+'('
            evalstr += ', '.join(map(evaluateable_string, args))
            evalstr += ')'
        if hasattr(func, 'custom_latex'):
            latex = func.custom_latex
            for n, arg in enumerate(args):
                latex = latex.replace(f'<{n}>', f'{arg}')
            self.LaTeX = latex
        elif hasattr(func, 'LaTeX'):
            self.LaTeX = func.LaTeX
        else:
            if hasattr(func, 'latexname'):
                latex = func.latexname+'\\left('
            elif hasattr(func, 'latexfunc') and func.latexfunc:
                latex = '\\'+func.__name__+'\\left('
            else:
                latex = func.__name__+'\\left('
            latex += ', '.join(map(getLaTeX, args))
            latex += '\\right)'
            self.LaTeX = latex
        self.string = string
        self.evalstr = evalstr
        self.arg_data_func_wrap = tmd[func.__name__]
        return self

    def __str__(self):
        return self.string

    def _comp_derive(self, v, k):
        if k == 0:
            return self
        if v not in self.var:
            return 0

        if self.args.count(v) == 1:
            i = self.args.index(v)
            if i in self.prime_cycle:
                cycle = self.prime_cycle[i]
                if cycle <= k:
                    return self._comp_derive(v, k % cycle)

        run = []
        for n, a in enumerate(self.args):
            if is_constant(a):
                continue
            if isinstance(a, cas_variable):
                if a != v:
                    continue
                ap = 1
            else:
                ap = _comp_derive(a, v, 1)
            if ap:
                if len(self.prime[n]) == 2:
                    prime_func = self.prime[n][0]
                    prime_args = self.prime[n][1]
                    fp = prime_func(*get_args(self.args, prime_args))
                    fp = fp.composition
                else:
                    fp = self.prime[n]

                run.append(mul_expression((fp, ap)))
        return _comp_derive(add_expression(run), v, k-1)

    def __call__(self, *args):
        if len(args) != len(self.var):
            raise ValueError('Length of args != length of var')
        for v, a in zip(self.var, args):
            v._set(a)
        return_val = self.func(*map(_get, self.args))
        for v in self.var:
            v._reset()
        return return_val
    evaluate = __call__


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
    _data: dict

    def __new__(cls, func):
        if type(func) is mathfunc:
            return func
        if callable(func):
            assert isinstance(func, cas_function)
        elif isinstance(func, cas_expression):
            pass
        else:
            raise TypeError(f'Invalid type recieved, type({type(func)})')
        self = super(mathfunc, cls).__new__(cls)
        if hasattr(func, 'custom_composition') and hasattr(func, 'args'):
            self.composition = func.custom_composition.evaluate(*func.args)
        else:
            self.composition = func
        if isinstance(func, cas_function):
            self.__name__ = func.func.__name__
        else:
            self.__name__ = None
        self.arguments_comp = func.var
        self.arguments_call = func.var
        self.var = func.var
        self.fn = func.fn
        self.function = evaluateable_string(func)
        self.__doc__ = 'Return '+str(func)
        var_list_str = ', '.join(map(str, self.var))
        space = {fn.__name__: fn for fn in func.fn}
        _short = eval(f'lambda {var_list_str}: {self.function}', None, space)
        self.shortcut_function = _short
        _get = eval(f'lambda self, {var_list_str}: {self.function}', None, space)
        self.__call__ = _get.__get__(self)

        self._data = {'composition': func, 'oper': {}, 'custom_data': {}}
        return self

    @math_return_dec
    def __call__(self, *args):
        if all(map(is_constant, args)) and not any(map(is_constant, args)):
            return self.shortcut_function(*args)
        return self.composition.evaluate(*args)

    def __repr__(self):
        '''repr for mathfunc'''
        return f'<mathfunc {self} at {hex(id(self))}>'

    def __str__(self):
        '''str for mathfunc'''
        return str(self.composition)

    def __hash__(self, /):
        '''hash for mathfunc'''
        return hash(self.composition)

    def LaTeX(self):
        return getLaTeX(self.composition)

    @math_return_dec
    def differentiate(self, var, k):
        if var not in self.var:
            return 0
        return _comp_derive(self.composition, var, k)

    def partial(self, var):
        return self.differentiate(var, 1)


pi = cas_constant('π', math.pi, '\\pi')
e = cas_constant('e', math.e)
tau = cas_constant('τ', math.tau, '\\tau')

x, y, z, t = create_variables('x', 'y', 'z', 't')

mathfunction = cas_func_wrap


@mathfunction
def exp(x, /):
    '''Return e to the power of x'''
    try:
        return math.exp(x)
    except Exception:
        pass
    try:
        return cmath.exp(x)
    except Exception:
        pass
    try:
        return x.exp()
    except Exception:
        pass
    try:
        return math.e**x
    except Exception:
        pass
    raise TypeError(f'invalid type, type {type(x).__name__}')


exp.prime[0] = exp, (0, )
exp.prime_cycle[0] = 1
exp.custom_composition = (e**x).composition


@mathfunction
def floor(x, /):
    '''Return the floor of x'''
    try:
        return math.floor(x)  # math's floor already allows for custom types
    except Exception:
        pass
    # I feel that imaginary types should still work
    # They bring it to the closest gaussian number
    if type(x) is complex:
        return math.floor(x.real) + math.floor(x.imag)*1j
    raise TypeError(f'invalid type, type {type(x).__name__}')


floor.prime[0] = 0


@mathfunction
def ceil(x, /):
    '''Return the ceil of x'''
    try:
        return math.ceil(x)  # math's ceil already allows for custom types
    except Exception:
        pass
    # imaginary type is not built in.
    if type(x) is complex:
        return ceil(x.real) + ceil(x.imag)*1j

    raise TypeError(f'invalid type, type {type(x).__name__}')


ceil.prime[0] = 0


@mathfunction
def S(x, /):
    '''Sigmoid function'''
    epow = exp(-x)
    return 1/(1+epow)


sigmoid = S
sigmoid.prime[0] = exp(-x)/((1+exp(-x))**2), (0, )
sigmoid.custom_composition = (1/(1+exp(-x))).composition


@mathfunction
def expm1(x, /):
    '''Return exp(x)-1'''
    try:
        return math.expm1(x)
    except Exception:
        return exp(x)-1


expm1.prime[0] = exp, (0, )


@mathfunction
def sqrt(x, /):
    '''Return the square root of x'''
    try:
        return math.sqrt(x)
    except Exception:
        pass
    try:
        return cmath.sqrt(x)
    except Exception:
        pass
    try:
        return x**(1/2)
    except Exception:
        pass
    raise ValueError('math domain error')


sqrt.custom_composition = (x**(0.5)).composition
sqrt.prime[0] = (0.5)*x**(-1/2), (0, )


@mathfunction
def isqrt(x, /):
    '''Return the floored square root of x'''
    try:
        return math.isqrt(x)
    except Exception:
        return floor(sqrt(x))


isqrt.custom_composition = floor(sqrt(x)).composition
isqrt.prime[0] = 0


@mathfunction
def cbrt(x, /):
    '''Return the cube root of x'''
    try:
        return x**(1/3)
    except Exception:
        pass
    raise ValueError('math domain error')


cbrt.custom_composition = (x**cas_exact('1/3')).composition
cbrt.prime[0] = (cas_exact('1/3'))*x**(cas_exact('-2/3')), (0, )


@mathfunction
def icbrt(x, /):
    '''Return the floored cube root of x'''
    try:
        return floor(x**(1/3))
    except Exception:
        pass
    raise ValueError('math domain error')


icbrt.custom_composition = (floor(cbrt(x))).composition
icbrt.prime[0] = (0, )


@mathfunction
def square(x, /):
    '''Return x**2'''
    return x*x


square.custom_composition = (x**2).composition
square.prime[0] = 2*x, (0, )


@mathfunction
def cube(x, /):
    '''Return x**3'''
    return x*x*x


cube.custom_composition = (x**3).composition
cube.prime[0] = 3*x**2, (0, )


@mathfunction
def tesser(x, /):
    '''Return x**4'''
    return x*x*x*x


tesser.custom_composition = (x**4).composition
tesser.prime[0] = 4*x**3, (0, )


@mathfunction
def ln(x, /):
    '''Return the natural logarithm of x
recources to x.ln() or x.log(e) if ln cannot be found'''
    if x == 0:
        raise ValueError('math domain error')
    try:
        return math.log(x)
    except Exception:
        pass
    try:
        return cmath.log(x)
    except Exception:
        pass
    try:
        return x.ln()
    except Exception:
        pass
    try:
        return x.log(math.e)
    except Exception:
        pass
    raise TypeError('ln cannot be found of % s.' % type(x).__name__)


ln.prime[0] = x**-1, (0, )
# TODO: Interaction between logs.


@mathfunction
def log(base, x):
    ''' log([base=10], x)
    Return the log base 'base' of x
    recources to x.log(base) and base.rlog(x) if log cannot be found'''
    if x == base:
        return 1
    if 0 in (x, base):
        raise ValueError('math domain error')
    if base == 1:
        raise ValueError('math domain error')
    try:
        return math.log(x, base)
    except Exception:
        pass
    try:
        return cmath.log(x, base)
    except Exception:
        pass
    try:
        return x.log(base)
    except Exception:
        pass
    try:
        return base.rlog(x)
    except Exception:
        pass
    raise TypeError('Logarithm cannot be found of a type % s.' % type(x))


def logcallhook(a, b):
    if a == 1 or (0 in (a, b)):
        raise ValueError('math domain error')
    if a == b:
        return cas_exact(1)
    if b == 1:
        return cas_exact(0)
    return NotImplemented


def logpassxpowhook(a, b):
    return mul_expression((b.b, log(a, b.a)))


def logpassbasepowhook(a, b):
    return mul_expression((a.b**-1, log(a.a, b)))


def logpassxmulhook(a, b):
    return add_expression(map(lambda x: log(a, x), b))


log.prime[0] = (-ln(x))*((ln(y))**-2)*(y**-1), (0, 1)
log.prime[1] = (x*ln(y))**-1, (0, 1)
log.__passxpowhook__ = logpassxpowhook
log.__passbasepowhook__ = logpassbasepowhook
log.__passxmulhook__ = logpassxmulhook
log.__callhook__ = logcallhook
log.custom_latex = '\\log_{<0>}\\left({<1>}\\right)'

true_log = log
log = decorators.shift_args({2: (0, 1), 1: ((10, ), 0)})(log)


@mathfunction
def log2(x, /):
    '''Return the log base 2 of x'''
    if x == 0:
        raise ValueError('math domain error')
    try:
        return math.log2(x)
    except Exception:
        pass
    try:
        return log(2, x)
    except Exception:
        pass
    raise TypeError('Log base 2 cannot be found of a type % s.' % type(x))


log2.prime[0] = 1/ln(2)*(x**-1), (0, )


@mathfunction
def log1p(x, /):
    '''Return the natural logarithm of x+1'''
    try:
        return math.log1p(x)
    except Exception:
        pass
    try:
        return ln(x+1)
    except Exception:
        pass
    raise TypeError('log1p cannot be found of a type % s.' % type(x))


log1p.prime[0] = 1/(x+1), (0, )


# Trig functions
@mathfunction
def acos(x):
    '''Return the arc cosine of x,
recources to x.acos if cos cannot be found'''
    if validation.is_float(x) and (x <= 1 and x >= -1):
        return math.acos(x)
    elif validation.is_complex(x):
        return cmath.acos(x)
    else:
        try:
            return x.acos()
        except Exception:
            pass
    raise TypeError('acos cannot be found of a type % s' % (type(x)))


acos.latexname = '\\arccos'


@mathfunction
def acosh(x):
    '''Return the inverse hyperbolic cosine of x
recources to x.acosh if cosh cannot be found'''
    if validation.is_float(x):
        return math.acosh(x)
    elif validation.is_complex(x):
        return cmath.acosh(x)
    else:
        try:
            return x.acosh()
        except Exception:
            pass
    raise TypeError('acos cannot be found of a type % s' % (type(x)))


acosh.latexname = '\\arccosh'


@mathfunction
def asin(x):
    '''Return the arc sine of x,
recources to x.asin if sin cannot be found'''
    if validation.is_float(x) and (x <= 1 and x >= -1):
        return math.asin(x)
    elif validation.is_complex(x):
        return cmath.asin(x)
    else:
        try:
            return x.asin()
        except Exception:
            pass
    raise TypeError('asin cannot be found of a type % s' % (type(x)))


asin.latexname = '\\arcsin'


@mathfunction
def asinh(x):
    '''Return the inverse hyperbolic sine of x
recources to x.asinh if sinh cannot be found'''
    if validation.is_float(x):
        return math.asinh(x)
    elif validation.is_complex(x):
        return cmath.asinh(x)
    else:
        try:
            return x.asinh()
        except Exception:
            pass
    raise TypeError('asin cannot be found of a type % s' % (type(x)))


asinh.latexname = '\\arcsinh'


@mathfunction
def atan(x):
    '''Return the arc tangent of x,
recources to x.atan if tan cannot be found'''
    if validation.is_float(x):
        return math.atan(x)
    elif validation.is_complex(x):
        return cmath.atan(x)
    else:
        try:
            return x.atan()
        except Exception:
            pass
    raise TypeError('atan cannot be found of a type % s' % (type(x)))


atan.latexname = '\\arctan'


@mathfunction
def atan2(y, x):
    '''Return the arc tangent(measured in radians) of y/x'''
    return math.atan2(validation.trynumber(y), validation.trynumber(x))


atan2.latexname = '\\arctan2'
atan2.prime[0] = (y+y*(x/y)**2)**-1, (0, 1)
atan2.prime[1] = -(y+y*(x/y)**2)**-1, (0, 1)


@mathfunction
def atanh(x):
    '''Return the inverse hyperbolic tangent of x
recources to x.atanh if tanh cannot be found'''
    if validation.is_float(x):
        return math.atanh(x)
    elif validation.is_complex(x):
        return cmath.atanh(x)
    else:
        try:
            return x.atanh()
        except Exception:
            pass
    raise TypeError('atan cannot be found of a type % s' % (type(x)))


atanh.latexname = '\\arctanh'


@mathfunction
def asec(x):
    '''Return the arc secant of x
recources to x.asec if sec cannot be found'''
    zde = False
    if validation.is_float(x):
        try:
            return(math.acos(1/x))
        except ZeroDivisionError:
            zde = True
    elif validation.is_complex(x):
        try:
            return(cmath.acos(1/x))
        except ZeroDivisionError:
            zde = True
    else:
        try:
            try:
                return x.asec()
            except ZeroDivisionError:
                zde = True
        except Exception:
            pass
    if zde:
        raise ValueError('math domain error')
    raise TypeError('asec cannot be found of a type % s' % (type(x)))


asec.latexname = '\\arcsec'


@mathfunction
def asech(x):
    '''Return the inverse hyperbolic secant of x
recources to x.asech if sech cannot be found'''
    zde = False
    if validation.is_float(x):
        try:
            return(math.acosh(1/x))
        except ZeroDivisionError:
            zde = True
    elif validation.is_complex(x):
        try:
            return(cmath.acosh(1/x))
        except ZeroDivisionError:
            zde = True
    else:
        try:
            try:
                return x.asech()
            except ZeroDivisionError:
                zde = True
        except Exception:
            pass
    if zde:
        raise ValueError('math domain error')
    raise TypeError('asech cannot be found of a type % s' % (type(x)))


asech.latexname = '\\arcsech'


@mathfunction
def acsc(x):
    '''Return the arc cosecant of x
recources to x.acsc if csc cannot be found'''
    zde = False
    if validation.is_float(x):
        try:
            return(math.asin(1/x))
        except ZeroDivisionError:
            zde = True
    elif validation.is_complex(x):
        try:
            return(cmath.asin(1/x))
        except ZeroDivisionError:
            zde = True
    else:
        try:
            try:
                return x.acsc()
            except ZeroDivisionError:
                zde = True
        except Exception:
            pass
    if zde:
        raise ValueError('math domain error')
    raise TypeError('acsc cannot be found of a type % s' % (type(x)))


acsc.latexname = '\\arccsc'


@mathfunction
def acsch(x, /):
    '''Return the inverse hyperbolic cosecant of x
recources to x.acsch if csch cannot be found'''
    zde = False
    if validation.is_float(x):
        try:
            return(math.asinh(1/x))
        except ZeroDivisionError:
            zde = True
    elif validation.is_complex(x):
        try:
            return(cmath.asinh(1/x))
        except ZeroDivisionError:
            zde = True
    else:
        try:
            try:
                return x.acsch()
            except ZeroDivisionError:
                zde = True
        except Exception:
            pass
    if zde:
        raise ValueError('math domain error')
    raise TypeError('acsch cannot be found of a type % s' % (type(x)))


acsch.latexname = '\\arccsch'


@mathfunction
def acot(x, /):
    '''Return the arc cotangent of x
recources to x.acot if cot cannot be found'''
    zde = False
    if validation.is_float(x):
        try:
            return(math.atan(1/x))
        except ZeroDivisionError:
            zde = True
    elif validation.is_complex(x):
        try:
            return (cmath.atan(1/x))
        except ZeroDivisionError:
            zde = True
    else:
        try:
            try:
                return x.acot()
            except ZeroDivisionError:
                zde = True
        except Exception:
            pass
    if zde:
        raise ValueError('math domain error')
    raise TypeError('acot cannot be found of a type % s' % (type(x)))


acot.latexname = '\\arccot'


@mathfunction
def acoth(x, /):
    '''Return the inverse hyperbolic cotangent of x
recources to x.acoth if coth cannot be found'''
    zde = False
    if validation.is_float(x):
        try:
            return(math.atanh(1/x))
        except ZeroDivisionError:
            zde = True
    elif validation.is_complex(x):
        try:
            return(cmath.atanh(1/x))
        except ZeroDivisionError:
            zde = True
    else:
        try:
            try:
                return x.acoth()
            except ZeroDivisionError:
                zde = True
        except Exception:
            pass
    if zde:
        raise ValueError('math domain error')
    raise TypeError('acoth cannot be found of a type % s' % (type(x)))


acot.latexname = '\\arccot'


@mathfunction
def cos(θ):
    '''Return the cosine of θ,
recources to θ.cos if cos cannot be found'''
    if validation.is_float(θ):
        return math.cos(θ)
    elif validation.is_complex(θ):
        return cmath.cos(θ)
    else:
        try:
            return θ.cos()
        except Exception:
            pass
    raise TypeError('cos cannot be found of a type % s' % (type(θ)))


def cospowahook(powexp):
    if powexp.b == 2:
        powexp.__mulcheckhook__ = cos2mulhook
        powexp.__addcheckhook__ = cos2addhook
        return powexp
    return NotImplemented


def cos2addhook(addexp):
    return NotImplemented


def cos2mulhook(mulexp):
    return NotImplemented


cos.latexfunc = True


@mathfunction
def cosh(θ):
    '''Return the hyperbolic cosine of θ,
recources to θ.cosh if cosh cannot be found'''
    if validation.is_float(θ):
        return math.cosh(θ)
    elif validation.is_complex(θ):
        return cmath.cosh(θ)
    else:
        try:
            return θ.cosh()
        except Exception:
            pass
    raise TypeError('cosh cannot be found of a type % s' % (type(θ)))


cosh.latexfunc = True


@mathfunction
def sin(θ):
    '''Return the sine of θ,
recources to θ.sin if sin cannot be found'''
    if validation.is_float(θ):
        return math.sin(θ)
    elif validation.is_complex(θ):
        return cmath.sin(θ)
    else:
        try:
            return θ.sin()
        except Exception:
            pass
    raise TypeError('sin cannot be found of a type % s' % (type(θ)))


sin.latexfunc = True


@mathfunction
def sinh(θ):
    '''Return the hyperbolic sine of θ,
recources to θ.sinh if sinh cannot be found'''
    if validation.is_float(θ):
        return math.sinh(θ)
    elif validation.is_complex(θ):
        return cmath.sinh(θ)
    else:
        try:
            return θ.sinh()
        except Exception:
            pass
    raise TypeError('sinh cannot be found of a type % s' % (type(θ)))


sinh.latexfunc = True


@mathfunction
def tan(θ):
    '''Return the tangent of θ,
recources to θ.tan if tan cannot be found'''
    if validation.is_float(θ):
        return math.tan(θ)
    elif validation.is_complex(θ):
        return cmath.tan(θ)
    else:
        try:
            return θ.tan()
        except Exception:
            pass
    raise TypeError('tan cannot be found of a type % s' % (type(θ)))


tan.latexfunc = True


@mathfunction
def tanh(θ):
    '''Return the hyperbolic tangent of θ,
recources to θ.tanh if tanh cannot be found'''
    if validation.is_float(θ):
        return math.tanh(θ)
    elif validation.is_complex(θ):
        return cmath.tanh(θ)
    else:
        try:
            return θ.tanh()
        except Exception:
            pass
    raise TypeError('tanh cannot be found of a type % s' % (type(θ)))


tanh.latexfunc = True


@mathfunction
def sec(θ):
    '''Return the secant of θ,
recources to θ.sec if sec cannot be found'''
    if validation.is_float(θ):
        try:
            return 1/math.cos(θ)
        except ZeroDivisionError:
            pass
        raise ValueError('math domain error')
    elif validation.is_complex(θ):
        try:
            return 1/cmath.cos(θ)
        except ZeroDivisionError:
            pass

    else:
        zde = False
        try:
            try:
                return θ.sec()
            except ZeroDivisionError:
                zde = True
        except Exception:
            pass
        if zde:
            raise ValueError('math domain error')
    raise TypeError('sec cannot be found of a type % s' % (type(θ)))


sec.latexfunc = True


@mathfunction
def sech(θ):
    '''Return the hyperbolic secant of θ
recources to θ.sech if sech cannot be found'''
    if validation.is_float(θ):
        try:
            return 1/math.cosh(θ)
        except ZeroDivisionError:
            pass
        raise ValueError('math domain error')
    elif validation.is_complex(θ):
        try:
            return 1/cmath.cosh(θ)
        except ZeroDivisionError:
            pass

    else:
        zde = False
        try:
            try:
                return θ.sech()
            except ZeroDivisionError:
                zde = True
        except Exception:
            pass
        if zde:
            raise ValueError('math domain error')
    raise TypeError('sech cannot be found of a type % s' % (type(θ)))


sech.latexfunc = True


@mathfunction
def csc(θ):
    '''Return the cosecant of θ,
recources to θ.csc if csc cannot be found'''
    if validation.is_float(θ):
        try:
            return 1/math.sin(θ)
        except ZeroDivisionError:
            pass
        raise ValueError('math domain error')
    elif validation.is_complex(θ):
        try:
            return 1/cmath.sin(θ)
        except ZeroDivisionError:
            pass
    else:
        zde = False
        try:
            try:
                return θ.csc()
            except ZeroDivisionError:
                zde = True
        except Exception:
            pass
        if zde:
            raise ValueError('math domain error')
    raise TypeError('csc cannot be found of a type % s' % (type(θ)))


csc.latexfunc = True


@mathfunction
def csch(θ):
    '''Return the hyperbolic cosecant of θ
recources to θ.csch if csch cannot be found'''
    if validation.is_float(θ):
        try:
            return 1/math.sinh(θ)
        except ZeroDivisionError:
            pass
        raise ValueError('math domain error')
    elif validation.is_complex(θ):
        try:
            return 1/cmath.sinh(θ)
        except ZeroDivisionError:
            pass

    else:
        zde = False
        try:
            try:
                return θ.csch()
            except ZeroDivisionError:
                zde = True
        except Exception:
            pass
        if zde:
            raise ValueError('math domain error')
    raise TypeError('csch cannot be found of a type % s' % (type(θ)))


csch.latexfunc = True


@mathfunction
def cot(θ):
    '''Return the cotangent of θ,
recources to θ.cot if cot cannot be found'''
    if validation.is_float(θ):
        try:
            return 1/math.tan(θ)
        except ZeroDivisionError:
            pass
        raise ValueError('math domain error')
    elif validation.is_complex(θ):
        try:
            return 1/cmath.tan(θ)
        except ZeroDivisionError:
            pass

    else:
        zde = False
        try:
            try:
                return θ.cot()
            except ZeroDivisionError:
                zde = True
        except Exception:
            pass
        if zde:
            raise ValueError('math domain error')
    raise TypeError('cot cannot be found of a type % s' % (type(θ)))


cot.latexfunc = True


@mathfunction
def coth(θ):
    '''Return the hyperbolic cotangent of θ
recources to θ.coth if coth cannot be found'''

    if validation.is_float(θ):
        try:
            return 1/math.tanh(θ)
        except ZeroDivisionError:
            pass
        raise ValueError('math domain error')
    elif validation.is_complex(θ):
        try:
            return 1/cmath.tanh(θ)
        except ZeroDivisionError:
            pass

    else:
        zde = False
        try:
            try:
                return θ.coth()
            except ZeroDivisionError:
                zde = True
        except Exception:
            pass
        if zde:
            raise ValueError('math domain error')
    raise TypeError('coth cannot be found of a type % s' % (type(θ)))


coth.latexfunc = True

acos.prime[0] = -(1-x**2)**-(1/2), (0, )
asin.prime[0] = (1-x**2)**-(1/2), (0, )
atan.prime[0] = 1/(1+x**2), (0, )
asec.prime[0] = (x**4-x**2)**(-1/2), (0, )
acot.prime[0] = -1/(1+x**2), (0, )
acsc.prime[0] = -(x**4-x**2)**(-1/2), (0, )

cos.prime[0] = -sin(x), (0, )
sin.prime[0] = cos, (0, )
cos.prime_cycle[0] = 4
sin.prime_cycle[0] = 4
tan.prime[0] = sec(x)**2, (0, )
sec.prime[0] = sec(x)*tan(x), (0, )
cot.prime[0] = -(csc(x)**2), (0, )
csc.prime[0] = -csc(x)*cot(x), (0, )

acosh.prime[0] = (x**2-1)**(-1/2), (0, )
asinh.prime[0] = (x**2+1)**(-1/2), (0, ), (0, )
atanh.prime[0] = 1/(1-x**2), (0, )
asech.prime[0] = -1/(x*(1-x**2)**(1/2)), (0, )
acoth.prime[0] = 1/(1-x**2), (0, )
acsch.prime[0] = -(x**4+x**2)**(-1/2), (0, )

cosh.prime[0] = sinh, (0, )
sinh.prime[0] = cosh, (0, )
cosh.prime_cycle[0] = 2
sinh.prime_cycle[0] = 2
tanh.prime[0] = sech(x)**2, (0, )
sech.prime[0] = -sech(x)*tanh(x), (0, )
coth.prime[0] = -(csch(x)**2), (0, )
csch.prime[0] = -csch(x)*coth(x), (0, )


@mathfunction
def cis(θ, n=1j):
    '''Return cos(θ) + nsin(θ)'''
    if abs(abs(n)-1) > 1e-10:
        raise ValueError('math domain error')
    if n.real != 0:
        raise ValueError('math domain error')
    return cos(θ)+(n*sin(θ))


cis.prime[0] = -sin(x)+y*cos(x), (0, 1)
cis.prime[1] = sin(x), (0, )

variable = cas_variable


def polynomial(*terms):
    runfunc = 0
    for power, coefficient in enumerate(terms):
        runfunc += coefficient*x**power
    return runfunc

# For those of you brave enough to read to the end. That was nearly three thousand lines of cobbled nonsense I call a CAS.
# I plan to make it less nonsensical later

# eof
