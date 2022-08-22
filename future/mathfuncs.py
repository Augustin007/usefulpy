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
   variables using the CASvariable class.
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
from functools import cache, wraps, reduce
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
        return bool(n.is_constant)
    except AttributeError:
        return False


def is_rational(n):
    if isinstance(n, (int, Fraction, *constants)):
        return True
    try:
        return bool(n.is_rational())
    except AttributeError:
        return False


def is_exact(n):
    if isinstance(n, constants):
        return True
    try:
        return n.exact
    except AttributeError:
        return False


# DATA HANDLING #

def create_variables(*names):
    if not all(map(lambda x: type(x) is str, names)):
        raise TypeError('All names must be strings')
    return tuple(map(CASvariable, names))


def remove_duplicates(tup):
    return tuple(OrderedDict.fromkeys(tup).keys())


def get_args(args, selector):
    '''get args according to selector'''
    return [args[select] for select in selector]

# TYPE VALIDATION AND CONVERSION TOOLS #


def cas_safe(n):
    if type(n) is mathfunc:
        n = n.composition
    if isinstance(n, CASvariable):
        if n.value is not None:
            n = n.value
    if is_constant(n):
        if not isinstance(n, CASobject):
            logging.debug(f'converting {n} to cas_exact')
            try:
                return CASnumber(n)
            except Exception as error:
                logging.warn(f'{error.__class__.__name__}: {error.args[0]}')
        return n
    if not isinstance(n, CASobject):
        raise TypeError(f'Invalid CAS types, {type(n)}')
    if callable(n):
        return n(*map(cas_safe, n.args))
    return n

# ALTERNATE STRING TOOLS #


def getTex(value):
    if hasattr(value, 'LaTeX'):
        LaTeX = value.LaTeX
        if callable(LaTeX):
            return LaTeX()
        return LaTeX
    return str(value)


def print_raw_LaTeX(value):
    print(getTex(value))


def evaluateable_string(value):
    if hasattr(value, 'evalstr'):
        evalstr = value.evalstr
        if callable(evalstr):
            return evalstr()
        return evalstr
    return str(value)

# MATH TOOLS #


def _compDerive(n, var, k):
    '''Computes the kth partial derivative of n with respect to var'''
    # Making sure k is valid
    assert k >= 0  # Send to integral.
    if type(k) is not int:
        return NotImplemented  # decimal derivatives not implemented

    # 0th derivative means nothing
    if k == 0:
        return n

    # logging computation
    log = f'Computing {k} partial of {str(n)} with respect to {var.name}'
    logging.info(log)

    # catch trivial and identity derivatives
    if k == 1 and var == n:
        return 1

    elif is_constant(n) or isinstance(n, CASvariable):
        return 0

    # Call attributes
    if isinstance(n, (CASobject)):
        return n._compDerive(var, k)

    raise TypeError(f'Invalid type, type {type(n)}')


def _prodDeriveExpansion(f, g, v, k, n):
    f_p = _compDerive(f, v, n)
    g_p = _compDerive(g, v, k-n)
    c_p = binomialCoeficient(n, k)
    return CASprod((c_p, f_p, g_p))


def binomialCoeficient(k, n):
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
            return CASobject._math_return(return_val)
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


class _getitemtype(type):
    def __getitem__(self, *args):
        self._getitem(self, *args)


class CAS(type, metaclass=_getitemtype):
    def _getitem(self, *args):
        print(args)


class CASobject(metaclass=CAS):
    exact: bool
    value: int
    var: set
    fn: set

    def __repr__(self, /):
        return f'CAS[{repr(str(self))}]'

    @abstractmethod
    def tex(self, /):
        pass

    @abstractmethod
    def _checkHooks(self, /):
        return NotImplemented

    @abstractmethod
    def _compDerive(self, var, k, /):
        '''kth partial of self with respect to var'''
        return NotImplemented


class _arithmetic:
    pass


class CASfunction(CASobject, _arithmetic):
    pass


class CASvariable(CASobject, _arithmetic):
    '''variable for cas engine'''
    name: str
    names: dict = {}
    value = typing.Any = None
    exact = False
    var: set

    def __new__(cls, name):
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

        # create and log the variable
        logging.info(f'Variable created: {name!r}')
        self = super(CASvariable, cls).__new__(cls)

        self.name = name
        self.names[name] = self
        self.var = {self}

        return self

    def _set(self, value):
        self.value = value

    def _reset(self):
        self.value = None

    def __str__(self, /):
        return self.name


class CASconstant(CASobject, _arithmetic):
    pass


class CASnumber(CASobject, _arithmetic):
    def __init__(self, number):
        self.value = number
        self.exact = True

    def __str__(self, /):
        return str(self.value)

    def __eq__(self, other, /):
        return self.value == other


bitor = lambda a, b: a|b


def get_var(n):
    return reduce(bitor, (i.var for i in n if hasattr(i, 'var')), set())


def get_fn(n):
    return reduce(bitor, (i.fn for i in n if hasattr(i, 'fn')), set())


def get_simplify(n):
    return n.simplify() if hasattr(n, 'simplify') else n


class CASexpression(CASobject, _arithmetic):
    pass


class CAScommutative(CASexpression, tuple):
    operation: types.FunctionType
    next: CASobject
    empty: int

    def __new__(cls, iterable=()):
        '''__new__ for any communative expressions'''
        if iterable == ():
            iterable = (cls.empty,)
        iterable = tuple(map(cas_safe, iterable))
        var, fn, exact, iterable = cls.gatherData(iterable)
        if len(iterable) < 1:
            if len(iterable) == 0:
                return cls.empty
            return iterable[0]
        self = tuple.__new__(cls, iterable)
        self.exact, self.var, self.fn = exact, var, fn
        return self

    @classmethod
    def gatherData(cls, iterable: iter, /) -> tuple[set, set, bool, iter]:
        var = get_var(iterable)
        fn = get_fn(iterable)
        exact = not var
        iterable = cls.expandInternal(iterable, exact)
        return var, fn, exact, tuple(iterable)

    @classmethod
    def expandInternal(cls, iterable, exact):
        if exact:
            for i in iterable:
                if i == cls.empty:
                    continue
                if type(i) is cls:
                    yield from i
                    continue
                yield i
            return
        exactOnes = []
        for i in iterable:  # FLAG
            if i.exact:
                if i == cls.empty:
                    continue
                exactOnes.append(i)
                continue
            elif type(i) is cls:
                yield from i
                continue
            yield i
        yield cls(exactOnes)

    def mapSimple(self, /):
        return self.__class__(map(get_simplify, self))

    def simplify(self):
        self = self.mapSimple()
        # Fast cases
        if len(self) == 1:
            return self[0]
        if len(self) == 0:
            return self.empty

        # Hooks
        check = self._checkHooks()
        if check is not NotImplemented:
            return check

        # Separate rationals/irrationals, or constant/variable expressions.
        num, exp = self._extractNum()  # FLAG
        expExtract = list(map(self._dataExtract, exp))
        expShort = []
        while expExtract:
            count, value = expExtract.pop(0)
            runCount = 0
            for newCount, newValue in tuple(expExtract):
                if newValue == value:
                    count += newCount
                    expExtract.pop(runCount)
                    continue
                runCount += 1
                continue
            if count != 0:
                if count != 1:
                    expShort.append(self.next((count, value)).simplify())
                    continue
                expShort.append(value)
        if len(expShort) == 0:
            return num  # FLAG
        if num == 0:
            if len(expShort) == 1:
                return expShort[0]
            return self.__class__(expShort)
        return self.__class__((num, *expShort))

    def _extractNum(self, /):
        check = is_rational if self.exact else is_constant
        numbers = []
        expressions = []
        for n in self:
            if check(n):
                numbers.append(n)
                continue
            expressions.append(n)
        return self.operation(numbers), expressions

    def _dataExtract(self, value, /):
        if isinstance(value, self.next):
            count, value = value._extractNum()
            return count, self.next(value).simplify()
        return 1, value

    def __str__(self, /):
        return self.oper.join(map(str, self))

    def tex(self, /):
        return '{'+(f'}}{self.oper}{{').join(map(getTex, self))+'}'


class d:  # Not entirely sure what to do here
    pass
# Something like this
# (d/d(x)) = CASdifferential(x)
# (d/d(x))[f(x)] = f'(x)
# d(x) = Partial(x)
# d[f(x)] = CASdifferentiator(f(x))
# d[f(x)]/d(x) = f'(x)
# etc.


class CASdifferentiator(CASexpression):
    pass


class CASdifferential(CASobject, _arithmetic):
    pass


class CASlimit(CASexpression):
    pass


class CASintegrator(CASobject, _arithmetic):
    pass


class CASsum(CAScommutative):
    def _compDerive(self, var, k, /):
        if var not in self.var:
            return 0
        return CASsum(tuple(map(lambda x: _compDerive(x, var, k), self))).simplify()


class CASprod(CAScommutative):
    pass


class CASpow(CASexpression):
    pass


CASsum.operation = sum
CASsum.next = CASprod
CASsum.oper = '+'
CASsum.empty = CASnumber(0)
CASprod.operation = math.prod
CASprod.next = CASpow
CASprod.oper = '*'
CASprod.empty = CASnumber(1)

#"""


class function:
    pass


def cas_func_wrap(func):
    '''Wraps a function to make it work in the cas engine.'''

    @wraps(func)
    def wrap(*args):
        if all(map(is_constant, args)):
            if any(map(is_exact, args)):
                return CASnest(wrap, args)
            return func(*args)
        return mathfunc(CASfunction(wrap, args))

    wrap.original = func
    wrap = function(wrap)
    wrap.original = func
    wrap.prime = {}
    wrap.format = None
    wrap.prime_cycle = {}
    return wrap


class mathfunc(_arithmetic):
    pass
# """
