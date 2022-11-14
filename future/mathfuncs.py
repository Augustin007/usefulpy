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
   Version 1.1.1:
    Bugfixes and more thorough documentation.
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

autoSimplify = True

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
from collections import OrderedDict, Counter
# Maths
import math
import cmath
from decimal import Decimal
from fractions import Fraction
from numbers import Number
from operator import add, or_

# CHECKS #

# DECORATORS #


def hook(name: str, varnum: int=None, r: bool=False, riter: tuple[int]=(), preface: str='', ignore: tuple[int]=(), custom: dict[int: str]={}) -> types.FunctionType:
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


    Returns
    -------
    types.FunctionType
        Wrapped function
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


def logCall(function: types.FunctionType) -> types.FunctionType:
    '''logCall

    Log all calls of wrapped function

    Parameters
    ----------
    function : types.FunctionType
        Function to wrap

    Returns
    -------
    types.FunctionType
        wrapped function
    '''
    @wraps(function)
    def wrapper(*args, **kwargs):
        logging.debug(f'{function.__name__} called with args {args} and kwargs {kwargs}')
        return function(*args, **kwargs)
    wrapper.logged = True
    return wrapper


def mathReturn(function: types.FunctionType) -> types.FunctionType:
    '''mathReturnDec

    Make sure returns are cas_safe

    Parameters
    ----------
    function : types.FunctionType
        Function to wrap

    Returns
    -------
    types.FunctionType
        wrapped function
    '''
    @wraps(function)
    @logCall
    def wrapper(*args, **kwargs):
        returnVal = function(*args, **kwargs)

        if not autoSimplify:
            return returnVal
        try:
            return getSimplify(casSafe(returnVal))
        except Exception as error:
            logging.error(f'{error.__class__.__name__}: {error.args[0]}')
            return NotImplemented
    return wrapper


class CAS(type):
    def __new__(cls, *args, **kwargs):
        namespace = args[2]
        for key, val in namespace.items():
            if callable(val) and not hasattr(val, 'logged') and (val.__name__ not in ('__repr__', '__str__')):
                namespace[key]=logCall(val)
        return type.__new__(type, *args, **kwargs)

    def __class_getitem__(self, *args):
        print(args)


class CASobject(metaclass=CAS):
    exact: bool
    value: int
    var: tuple
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

    def evalstr(self):
        if self.exact:
            return str(self.value)
        return str(self)
    
    def derive(self, var, k):
        return _compDerive(self, var, k)
    
    def partial(self, var):
        return _compDerive(self, var, 1)


class _arithmetic:
    @mathReturn
    def __neg__(self):
        return CASprod(self, -1)

    @logCall
    def __pos__(self):
        return self

    @mathReturn
    def __add__(self, other, /):
        other = casSafe(other)
        if isRational(other) and isRational(self):
            return CASnumber(self.value + other.value)
        return CASsum(self, other)

    @mathReturn
    def __radd__(self, other):
        return self+other

    @mathReturn
    def __sub__(self, other):
        return self + -other

    @mathReturn
    def __rsub__(self, other):
        return -self + other

    @mathReturn
    def __mul__(self, other):
        other = casSafe(other)
        if isRational(other) and isRational(self):
            return CASnumber(self.value * other.value)
        return CASprod(self, other)

    @mathReturn
    def __rmul__(self, other):
        return self*other

    @mathReturn
    def __truediv__(self, other):
        if isRational(other):
            other = Fraction(1, other)
        else:
            other = other**-1
        return self*other

    @mathReturn
    def __rtruediv__(self, other):
        return (self**-1)*other

    @mathReturn
    def __pow__(self, other):
        other = casSafe(other)
        if isRational(self) and (type(other.value) is int):
            return CASnumber(self.value ** other.value)
        return CASpow(self, other)

    @mathReturn
    def __rpow__(self, other):
        other = casSafe(other)
        if isRational(other) and (type(self.value) is int):
            return CASnumber(other.value ** self.value)
        return CASpow(other, self)


class CASvariable(CASobject, _arithmetic):
    '''variable for cas engine'''
    name: str
    tex: str
    names: dict = {}
    value = typing.Any = None
    exact = False
    var: tuple
    fn = set()

    def __new__(cls, name, tex=None):
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
        self.var = (self,)
        self.tex = name if tex is None else tex

        return self

    def _set(self, value):
        self.value = value

    def _reset(self):
        self.value = None

    def __str__(self, /):
        return self.name
    
    def evaluate(self, vardict:dict, /):
        return vardict.get(self, self)

class CASconstant(CASobject, _arithmetic):
    var = ()
    fn = set()
    rational = False
    exact = True
    names = CASvariable.names

    def __new__(cls, name, number, tex=None):
        if name in cls.names:
            return cls.names[name]
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
        self = super(CASconstant, cls).__new__(cls)
        self.value = number
        self.name = name
        self.names[name] = self
        self.tex = name if tex is None else tex
        return self

    def __str__(self, /):
        return self.name

    def __eq__(self, other, /):
        return self.value == other

    def __hash__(self, /):
        return hash(self.value)

    def tex(self, /):
        return getTex(self.value)


class CASnumber(CASobject, _arithmetic):
    var = ()
    fn = set()
    rational = True
    exact = True

    def __init__(self, number):
        self.value = number

    def __str__(self, /):
        return str(self.value)

    def __eq__(self, other, /):
        return self.value == other

    def __hash__(self, /):
        return hash(self.value)

    def tex(self, /):
        return getTex(self.value)


class CASexpression(CASobject, _arithmetic):
    pass


class CAScommutative(CASexpression, tuple):
    operation: types.FunctionType
    next: CASobject
    empty: int

    def __new__(cls, *iterable):
        '''__new__ for any communative expressions'''
        if iterable == ():
            iterable = (cls.empty,)
        iterable = tuple(map(casSafe, iterable))
        var, fn, exact, iterable = cls.gatherData(iterable)
        if len(iterable) <= 1:
            if len(iterable) == 0:
                return cls.empty
            return iterable[0]

        self = tuple.__new__(cls, iterable)
        self.exact, self.var, self.fn = exact, var, fn
        self.value = None if not exact else self.operation(map(getValue, iterable))
        return self

    @classmethod
    def gatherData(cls, iterable: iter, /) -> tuple[set, set, bool, iter]:
        var = getVar(iterable)
        fn = getFn(iterable)
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
        if len(exactOnes) == 0:
            return
        if len(exactOnes) == 1:
            yield exactOnes[0]
            return
        yield cls(*exactOnes)

    def mapSimple(self, /):
        return self.__class__(*map(getSimplify, self))

    def simplify(self):
        self = self.mapSimple()
        self = self.preSimplify()
        # Fast cases
        if not isinstance(self, CAScommutative):
            return self
        if len(self) == 1:
            return self[0]
        if len(self) == 0:
            return self.empty

        if hasattr(self, 'collapse') and self.collapse in self:
            return self.collapse

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
                    expShort.append(getSimplify(self.next(value, count)))
                    continue
                expShort.append(value)
        if len(expShort) == 0:
            return CASnumber(num)
        if num == 0:
            if len(expShort) == 1:
                return expShort[0]
            return self.__class__(*expShort)
        return self.__class__(num, *expShort)
    
    def evaluate(self, vardict:dict):
        runcheck = []
        for item in self:
            if hasattr(item, 'evaluate'):
                runcheck.append(item.evaluate(vardict))
                continue
            runcheck.append(item)
        return getSimplify(self.__class__(*runcheck))

    def _extractNum(self, /):
        check = isRational if self.exact else isConstant
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
            if len(value) == 1:
                return count, getSimplify(value[0])
            return count, getSimplify(self.next(*value))
        return 1, value

    def __str__(self, /):
        return '('+(f'){self.oper}(').join(map(str, self))+')'

    def tex(self, /):
        return '{'+(f'}}{self.texoper}{{').join(map(getTex, self))+'}'

    def evalstr(self, /):
        return '('+(f'){self.oper}(').join(map(evalstr, self))+')'

    def __eq__(self, other, /):
        cls = type(self)
        other = casSafe(other)
        self = getSimplify(self)
        other = getSimplify(other)
        if type(self) is not cls:
            return self == other
        if type(self) is not type(other):
            return False
        return Counter(self) == Counter(other)
    
    def __hash__(self, /):
        # Expensive checks
        self = self.simplify().distribute()
        if not isinstance(self, CAScommutative):
            return hash(self)
        return hash(tuple(sorted(self, key = lambda x: hash(x))))


class d:  # Not entirely sure what to do here
    NotImplemented
# Something like this
# (d/d(x)) = CASdifferential(x)
# (d/d(x))[f(x)] = f'(x)
# d(x) = Partial(x)
# d[f(x)] = CASdifferentiator(f(x))
# d[f(x)]/d(x) = f'(x)
# etc.


class CASdifferentiator(CASexpression):
    NotImplemented


class CASdifferential(CASobject, _arithmetic):
    NotImplemented


class CASlimit(CASexpression):
    NotImplemented


class CASintegrator(CASobject, _arithmetic):
    NotImplemented


class CASsum(CAScommutative):
    def _compDerive(self, var, k, /):
        if var not in self.var:
            return 0
        return getSimplify(CASsum(*map(lambda x: _compDerive(x, var, k), self)))

    def preSimplify(self):
        return self

    def distribute(self):
        return getSimplify(CASsum(*map(distribute, self)))

    def __str__(self, /):
        return (self.oper).join(map(str, self))


class CASprod(CAScommutative):
    def preSimplify(self):
        if self.collapse in self:
            return self.collapse
        return self

    def distribute(self):
        for i, n in enumerate(self):
            if type(n) is CASsum:
                return getSimplify(CASsum(*map(lambda x: CASprod(x, *self[:i], *self[i+1:]), n))).distribute()
        return self

    def _compDerive(self, var, k, /):
        a, b = self._extractNum()
        if len(b) == 1:
            return CASprod(a, _compDerive(b[0], var, k))
        if len(b) == 2:
            f = b[0]
            g = b[1]
        elif len(b) == 3:
            f = b[0]
            g = CASprod(b[1], b[2])
        else:
            length = len(b)
            f = CASprod(b[: length//2])
            g = CASprod(b[length//2:])
        terms = [_prodDeriveExpansion(f, g, var, k, n) for n in range(k+1)]
        return getSimplify(a*sum(terms))


class CASpow(CASexpression):
    def __new__(cls, a, b):
        if b == 0 or a == 1:
            return CASnumber(1)
        if b == 1 or a == 0:
            return casSafe(a)
        self = super(cls, cls).__new__(cls)
        self.a, self.b = map(casSafe, (a, b))
        self.var = add(self.a.var, self.b.var)
        self.fn = self.a.fn | self.b.fn
        self.exact = not self.var
        self.value = None if not self.exact else self.a.value ** self.b.value
        return self

    def simplify(self):
        if isRational(self.a):
            if hasattr(self.b, 'value') and type(self.b.value) is int:
                return CASnumber(self.a.value**self.b.value)
        if type(self.a) is CASprod:
            return getSimplify(CASprod(*map(lambda n: CASpow(n, self.b), self.a)))
        if type(self.a) is CASpow:
            return CASpow(self.a.a, CASprod(self.a.b, self.b))
        return self

    def __hash__(self, /):
        self = getDistribute(getSimplify(self))
        if type(self) is CASpow:
            return hash((self.a, self.b))
        return hash(self)

    def __eq__(self, other, /):
        selftype = type(self)
        other = casSafe(other)
        self = getSimplify(self)
        other = getSimplify(other)
        if type(self) != selftype:
            return self == other
        if type(self) is not type(other):
            return False
        return self.a == other.a and self.b == other.b

    def _extractNum(self, /):
        return self.b, [self.a]

    def __str__(self, /):
        return f'({self.a})**({self.b})'

    def evalstr(self, /):
        return f'({evalstr(self.a)})**({evalstr(self.b)})'

    def tex(self, /):
        return '\\left({'+getTex(self.a)+'}\\right)^{'+getTex(self.b)+'}'

    def distribute(self, /):
        if not hasattr(self.b, 'value'):
            return CASpow(distribute(self.a), distribute(self.b))
        if type(self.b.value) is not int:
            return CASpow(distribute(self.a), distribute(self.b))
        return CASprod(*[self.a for n in range(self.b.value)]).distribute()

    def _compDerive(self, var, k, /):
        if var not in self.var:
            return CASnumber(0)
        if isConstant(self.b):
            if self.a == var:
                if type(self.b.value) is int:
                    b = self.b.value
                    if k > b:
                        return CASnumber(0)
                    coef = math.prod(range(b-k+1, b+1))
                else:
                    coef = math.prod(map(lambda x: (self.b-x+1), range(0, k)))
                return CASprod(coef, CASpow(var, self.b-k))
            partial = CASprod(self.b, CASpow(self.a, self.b-1), _compDerive(self.a, var, 1))
            return _compDerive(partial, var, k-1)
        if isConstant(self.a):
            return _compDerive(CASprod(ln(self.a), self), var, k-1)
        pross = CASprod(ln(self.a), self.b)
        internal = _compDerive(pross, var, 1)
        return getSimplify(_compDerive(CASprod(self, internal), var, k-1))
    
    def evaluate(self, vardict:dict):
        return getSimplify(CASpow(getEvaluate(self.a, vardict), getEvaluate(self.b, vardict)))

class CASfunction:
    def __init__(self, func:types.FunctionType, partials:tuple[CASobject]=(), partialsReferences:tuple[CASvariable]=(), indefiniteInt:tuple[CASobject]=(), indefiniteIntReferences:tuple[CASvariable]=()):
        self.func = func
        self.__name__ = func.__name__
        self.partials = partials
        self.partialsReferences = partialsReferences
        self.indefiniteInt = indefiniteInt
        self.indefiniteIntReferences = indefiniteIntReferences

    def __call__(self, *args):
        if any(map(lambda x: isinstance(x, CASobject), args)):
            args = tuple(map(casSafe, args))
            exact = all(map(lambda x: isExact(x), args))
            value = None
            if exact:
                value = self.func(*map(getValue, args))
            return CASnest(self, args, exact, value) ## TODO: Implement .evaluate
        return self.func(*args)

    def partialReset(self, partials, partialsReferences):
        self.partials = partials
        self.partialsReferences = partialsReferences
    
    def intReset(self, indefiniteInt, indefiniteIntReferences):
        self.indefiniteInt = indefiniteInt
        self.indefiniteIntReferences = indefiniteIntReferences


class CASnest(CASexpression):
    helper: CASfunction
    func: types.FunctionType
    nest: tuple[CASobject]
    __name__:str
    exact:bool
    value:typing.Any

    def __new__(cls, helper:CASfunction, nest:tuple[CASobject], exact:bool, value=None, /):
        self = super(cls, cls).__new__(cls)
        self.func = helper.func
        self.helper = helper
        self.__name__ = helper.__name__
        self.nest = nest
        self.var = getVar(nest)
        self.fn = getFn(nest)
        self.exact = exact
        self.value = value
        return self
    
    @property
    def partials(self):
        partialRefSet = {a:b for a, b in zip(self.helper.partialsReferences, self.nest)}
        return  tuple([fprime.evaluate(partialRefSet) for fprime in self.helper.partials])

    @property
    def indefiniteInt(self):
        indefiniteRefSet = {a:b for a, b in zip(self.helper.indefiniteIntReferences, self.nest)}
        return tuple([faprime.evaluate(indefiniteRefSet) for faprime in self.helper.indefiniteInt])
        

    def _compDerive(self, var, k):
        return _compDerive(getSimplify(CASsum(*tuple(CASprod(a, _compDerive(b, var, 1)) for a, b in zip(self.partials, self.nest) if var in b.var))), var, k-1)
        #TODO: prime_cycle
    
    def __str__(self, /):
        if len(self.nest) == 0:
            return self.__name__+'()'
        if len(self.nest) == 1:
            return f'{self.__name__}({self.nest[0]})'
        return f'{self.__name__}{self.nest}'
    
    def tex(self, /):
        pass
        #self.format?

    def evaluate(self, vardict:dict):
        return self.helper(*[getEvaluate(n, vardict) for n in self.nest])
        ##FLAG


CASsum.operation = sum
CASsum.next = CASprod
CASsum.oper = '+'
CASsum.texoper = '+'
CASsum.empty = CASnumber(0)
CASprod.operation = math.prod
CASprod.next = CASpow
CASprod.oper = '*'
CASprod.texoper = ''
CASprod.empty = CASnumber(1)
CASprod.collapse = CASsum.empty

constants = (int, float, complex, Decimal, Fraction, Number)
Rationals = (int, Fraction)
MathAttributes = ('__add__', '__radd__', '__sub__', '__mul__', '__rsub__', '__rmul__',
                  '__truediv__', '__rtruediv__', '__pow__', '__rpow__')


def isConstant(n: typing.Any) -> bool:
    '''isConstant

    Check whether a number is constant for cas engine

    Parameters
    ----------
    n : typing.Any
        Number to be checked

    Returns
    -------
    bool
    '''
    if isinstance(n, constants):
        return True
    if hasattr(n, 'exact'):
        return bool(n.exact)
    return all(map(lambda x: hasattr(n, x), MathAttributes))


def isRational(n: typing.Any) -> bool:
    '''isRational

    Check whether n is rational for cas engine

    Parameters
    ----------
    n : typing.Any
        Number to be checked

    Returns
    -------
    bool
    '''
    ''''''
    if isinstance(n, (Rationals)):
        return True
    if hasattr(n, 'rational'):
        return bool(n.rational)
    return False


def isExact(n: typing.Any) -> bool:
    '''isExact

    Check whether a number is stored 'exactly' in the engine

    Parameters
    ----------
    n : typing.Any
        Number to be checked

    Returns
    -------
    bool
    '''
    if isRational(n):
        return True
    if hasattr(n, 'exact'):
        return bool(n.exact)


# DATA HANDLING #
def createVariables(*names: tuple[str]) -> tuple[CASvariable]:
    '''createVariables _summary_

    Create CAS variables for a list of names
    x, y, z = create_variables('x', 'y', 'z')

    Returns
    -------
    tuple[CASvariable]
        One variable for each name input

    Raises
    ------
    TypeError
        Names must be strings
    '''
    if not all(map(lambda x: type(x) is str, names)):
        raise TypeError('All names must be strings')
    return tuple(map(CASvariable, names))


def removeDuplicates(tup: tuple) -> tuple:
    '''removeDuplicates

    Remove duplicates

    Parameters
    ----------
    tup : tuple
        Original values of iterable

    Returns
    -------
    tuple
        New tuple with duplicates removed
    '''
    return tuple(OrderedDict.fromkeys(tup).keys())


def getArgs(args, selector):
    '''get args according to selector'''
    return [args[select] for select in selector]


def getValue(n):
    if hasattr(n, 'value') and n.value is not None:
        return n.value
    return n


def distribute(expression):
    '''distribute

    Propogate distribution in CAS

    Parameters
    ----------
    expression : CASobject
        Point in distribution

    Returns
    -------
    CASobject
        New expression re-distributed
    '''
    if hasattr(expression, 'distribute'):
        return expression.distribute()
    return expression


# TYPE VALIDATION AND CONVERSION TOOLS #

def casSafe(n):
    '''casSafe

    Generate CAS safe version of a number

    Parameters
    ----------
    n : Some form of number/expression
        Number to convert to CASobject

    Returns
    -------
    CASobject
        New or original object that is safe within CAS

    Raises
    ------
    TypeError
        Invalid CAS type
    '''
    # if type(n) is mathfunc:
    #    n = n.composition
    if isinstance(n, CASvariable):
        if n.value is not None:
            n = n.value
    if isConstant(n):
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
        return n(*map(casSafe, n.args))
    return n

# ALTERNATE STRING TOOLS #


def getTex(value: CASobject) -> str:
    '''getTex

    Get TeX representation of value

    Parameters
    ----------
    value : CASobject
        Object to be rendered as TeX

    Returns
    -------
    str
        TeX-renderable string
    '''
    if hasattr(value, 'tex'):
        tex = value.tex
        if callable(tex):
            return tex()
        return tex
    return str(value)


def evalstr(n) -> str:
    '''evalstr _summary_

    Parameters
    ----------
    n : _type_
        _description_

    Returns
    -------
    str
        _description_

    Raises
    ------
    TypeError
        _description_
    '''
    if hasattr(n, 'value'):
        return str(n.value)
    return str(n) if not hasattr(n, 'evalstr') else n.evalstr()

def getVar(n: tuple[CASobject]) -> set[CASvariable]:
    '''getVar

    Gather variables for expression construction

    Parameters
    ----------
    n : tuple[CASobject]
        List of things to check before expression construction

    Returns
    -------
    set[CASvariable]
        Set of all CASvariables involved in expression
    '''
    return removeDuplicates(tuple(reduce(add, (i.var for i in n if hasattr(i, 'var')), ())))


def getFn(n: tuple[CASobject]) -> set[types.FunctionType]:
    '''getVar

    Gather functions for expression construction

    Parameters
    ----------
    n : tuple[CASobject]
        List of things to check before expression construction

    Returns
    -------
    set[types.FunctionType]
        Set of all functions involved in expression
    '''
    return reduce(or_, (i.fn for i in n if hasattr(i, 'fn')), set())


def getSimplify(n):
    '''getSimplify

    Attempt to simplify an expression

    Parameters
    ----------
    n
        Attempt to simplify n

    Returns
    -------
    Any
        Attempted simplification
    '''
    return n.simplify() if hasattr(n, 'simplify') else n

def getDistribute(n):
    '''getDistribute

    Attempt to distribute an expression

    Parameters
    ----------
    n
        Attempt to distribute n

    Returns
    -------
    Any
        Attempted distribution
    '''
    return n.distribute() if hasattr(n, 'distribute') else n

def getEvaluate(n, vardict:dict):
    if hasattr(n, 'evaluate'):
        return n.evaluate(vardict)
    return n

def printTex(value: CASobject) -> None:
    '''Utility for easier copy/pasting'''
    print(getTex(value))


def evaluateableStr(value: CASobject) -> str:
    '''evaluateableStr

    Constructs evaluatable string representation of expression

    Parameters
    ----------
    value : CASobject
        Expression to be formulated

    Returns
    -------
    str
        Evaluatable string
    '''
    if hasattr(value, 'evalstr'):
        evalstr = value.evalstr
        if callable(evalstr):
            return evalstr()
        return evalstr
    return str(value)

def symbolic(partials:tuple[CASobject]=(), partialsReferences:tuple[CASvariable]=(), indefiniteInt:tuple[CASobject]=(), indefiniteIntReferences:tuple[CASvariable]=()):
    def symbolicWrapper(func:types.FunctionType):
        return CASfunction(func, partials, partialsReferences, indefiniteInt, indefiniteIntReferences)
    return symbolicWrapper


# MATH TOOLS #


def _compDerive(n: CASobject, var: CASvariable, k: int) -> CASobject:
    '''_compDerive

    Compute partials

    Parameters
    ----------
    n : CASobject
        Expression to compute partial of
    var : CASvariable
        Compute partial with respect to var
    k : int
        Compute kth partial

    Returns
    -------
    CASobject
        kth partial derivative of n with respect to var

    Raises
    ------
    TypeError
        Invalid n recieved
    '''
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
        return CASnumber(1)

    elif isConstant(n) or isinstance(n, CASvariable):
        return CASnumber(0)

    # Call attributes
    if isinstance(n, (CASobject)):
        return getSimplify(n._compDerive(var, k))

    raise TypeError(f'Invalid type, type {type(n)}')

def _antiDerive(n: CASobject, var: CASvariable, k: int):
    return NotImplemented


def _prodDeriveExpansion(f: CASobject, g: CASobject, v: CASvariable, k: int, n: int) -> CASobject:
    '''_prodDeriveExpansion

    Return a term of a partial of a product

    Parameters
    ----------
    f : CASobject
        One of the terms in the product
    g : CASobject
        Other term in the product
    v : CASvariable
        Compute partial with respect to v
    k : int
        Compute kth partial
    n : int
        The term of the resulting sum

    Returns
    -------
    CASobject
        nth term of kth partial of fg with respect to v
    '''
    f_p = _compDerive(f, v, n)
    g_p = _compDerive(g, v, k-n)
    c_p = binomialCoeficient(n, k)
    return CASprod(c_p, f_p, g_p)


def binomialCoeficient(k: int, n: int) -> int:
    '''binomialCoeficient

    k choose n

    Parameters
    ----------
    k : int
        Power of bionomial expansion
    n : int
        Term of polynomial

    Returns
    -------
    int
        Coefficient of nth term of (a+b)**k
    '''
    return math.factorial(n)/(math.factorial(n-k)*math.factorial(k))


t, x, y, z = createVariables('t', 'x', 'y', 'z')
pi = CASconstant('π', math.pi, '\\pi')
e = CASconstant('e', math.e)
tau = CASconstant('τ', math.tau, '\\tau')

@symbolic((0,))
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

@symbolic((0,))
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


ln = symbolic((1/x,), (x,))(decorators.func_zip(math.log, cmath.log, decorators.attribute.ln, lambda x: x.log(math.e), final_exception=TypeError('Invalid Type')))
ln.__name__ = 'ln'
#  decorators.attribute.log(math.e))
ln.intReset((x*ln(x)-x,), (x,))


# exp
##TODO: Reimpliment custom coefficient for elementary functions

# Sigmoid

# exp(x)-1

#sqrt(x)
#isqrt(x)
#cbrt(x)
#icbrt(x)

#log (ln/ln with decorator shift args)

#log_2(x)

#log1p(x)

acos = symbolic()(decorators.func_zip(math.acos, cmath.acos, lambda x: x.acos(), final_exception = TypeError('Invalid Type')))
acosh = symbolic()(decorators.func_zip(math.acosh, cmath.acosh, lambda x: x.acosh(), final_exception = TypeError('Invalid Type')))
asin = symbolic()(decorators.func_zip(math.asin, cmath.asin, lambda x: x.asin(), final_exception = TypeError('Invalid Type')))
asinh = symbolic()(decorators.func_zip(math.asinh, cmath.asinh, lambda x: x.asinh(), final_exception = TypeError('Invalid Type')))
atan = symbolic()(decorators.func_zip(math.atan, cmath.atan, lambda x: x.atan(), final_exception = TypeError('Invalid Type')))
atanh = symbolic()(decorators.func_zip(math.atanh, cmath.atanh, lambda x: x.atanh(), final_exception = TypeError('Invalid Type')))

@symbolic()
def atan2(y, x):
    '''Return the arc tangent(measured in radians) of y/x'''
    return math.atan2(validation.trynumber(y), validation.trynumber(x))

asec = symbolic()(decorators.func_zip(lambda x:1/asec(x), lambda x: x.asec(), final_exception = TypeError('Invalid Type')))
asech = symbolic()(decorators.func_zip(lambda x:1/asec(x), lambda x: x.asech(), final_exception = TypeError('Invalid Type')))
acsc = symbolic()(decorators.func_zip(lambda x:1/acsc(x), lambda x: x.acsc(), final_exception = TypeError('Invalid Type')))
acsch = symbolic()(decorators.func_zip(lambda x:1/acsch(x), lambda x: x.acsch(), final_exception = TypeError('Invalid Type')))
acot = symbolic()(decorators.func_zip(lambda x:1/acot(x), lambda x: x.acot(), final_exception = TypeError('Invalid Type')))
acoth = symbolic()(decorators.func_zip(lambda x:1/acoth(x), lambda x: x.acoth(), final_exception = TypeError('Invalid Type')))

cos = symbolic()(decorators.func_zip(math.cos, cmath.cos, lambda x: x.cos(), final_exception = TypeError('Invalid Type')))
cosh = symbolic()(decorators.func_zip(math.cosh, cmath.cosh, lambda x: x.cosh(), final_exception = TypeError('Invalid Type')))
sin = symbolic()(decorators.func_zip(math.sin, cmath.sin, lambda x: x.sin(), final_exception = TypeError('Invalid Type')))
sinh = symbolic()(decorators.func_zip(math.sinh, cmath.sinh, lambda x: x.sinh(), final_exception = TypeError('Invalid Type')))
tan = symbolic()(decorators.func_zip(math.tan, cmath.tan, lambda x: x.tan(), final_exception = TypeError('Invalid Type')))
tanh = symbolic()(decorators.func_zip(math.tanh, cmath.tanh, lambda x: x.tanh(), final_exception = TypeError('Invalid Type')))

sec = symbolic()(decorators.func_zip(lambda x: 1/cos(x), lambda x: x.sec(), final_exception = TypeError('Invalid Type')))
sech = symbolic()(decorators.func_zip(lambda x: 1/cosh(x), lambda x: x.sech(), final_exception = TypeError('Invalid Type')))
csc = symbolic()(decorators.func_zip(lambda x: 1/sin(x), lambda x: x.csc(), final_exception = TypeError('Invalid Type')))
csch = symbolic()(decorators.func_zip(lambda x: 1/sinh(x), lambda x: x.csch(), final_exception = TypeError('Invalid Type')))
cot = symbolic()(decorators.func_zip(lambda x: 1/tan(x), lambda x: x.cot(), final_exception = TypeError('Invalid Type')))
coth = symbolic()(decorators.func_zip(lambda x: 1/tanh(x), lambda x: x.coth(), final_exception = TypeError('Invalid Type')))

acos.partialReset((-(1-x**2)**-(1/2),), (x,))
asin.partialReset(((1-x**2)**-(1/2),), (x,))
atan.partialReset((1/(1+x**2),), (x,))
asec.partialReset(((x**4-x**2)**(-1/2),), (x,))
acot.partialReset((-1/(1+x**2),), (x,))
acsc.partialReset((-(x**4-x**2)**(-1/2),), (x,))

cos.partialReset((-sin(x),), (x,))
sin.partialReset((cos,), (x,))
# cos.prime_cycle[0] = 4
# sin.prime_cycle[0] = 4
tan.partialReset((sec(x)**2,), (x,))
sec.partialReset((sec(x)*tan(x),), (x,))
cot.partialReset((-(csc(x)**2),), (x,))
csc.partialReset((-csc(x)*cot(x),), (x,))

acosh.partialReset(((x**2-1)**(-1/2),),(x,))
asinh.partialReset(((x**2+1)**(-1/2),), (x,))
atanh.partialReset((1/(1-x**2),), (x,))
asech.partialReset((-1/(x*(1-x**2)**(1/2))), (x,))
acoth.partialReset((1/(1-x**2),), (x,))
acsch.partialReset((-(x**4+x**2)**(-1/2),), (x,))

cosh.partialReset((sinh,), (x,))
sinh.partialReset((cosh,), (x,))
# cosh.prime_cycle[0] = 2
# sinh.prime_cycle[0] = 2
tanh.partialReset((sech(x)**2,), (x,))
sech.partialReset((-sech(x)*tanh(x),), (x,))
coth.partialReset((-(csch(x)**2),), (x,))
csch.partialReset((-csch(x)*coth(x),), (x,))

# TODO: redefine everything in terms of cos/sin?


# eof
