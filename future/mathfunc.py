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

# IMPORTS #
# Relative imports
from .. import decorators
from .. import validation
# Utilities
from abc import abstractmethod
import types
import typing
from functools import cache, wraps
import logging
from contextlib import suppress
# Maths
import math
import cmath
from decimal import Decimal
from fractions import Fraction
from numbers import Number

if __name__ == '__main__':
    level = validation.intinput('enter logging level: ')
    fmt = '[ % (levelname)s] % (name)s - % (message)s'
    logging.basicConfig(level=level, format=fmt)
    logging.root.setLevel(level)


constants = (int, float, complex, Decimal, Fraction, Number)


def is_constant(n) -> bool:
    '''Checks whether n is constant for cas engine'''
    if isinstance(n, constants):
        return True
    try:
        return bool(n.is_constant())
    except Exception:
        return False


def is_rational(n):
    return isinstance(n, (cas_exact, *constants))


def remove_duplicates(tup):  # TEMPORARY:
    return tuple(set(tup))


def get_args(args, selector):
    '''get args according to selector'''
    return [args[select] for select in selector]


def comp_extract(obj):
    if isinstance(obj, mathfunc):
        return obj.composition
    if is_constant(obj):
        if not isinstance(obj, cas_exact_object):
            return cas_exact(obj)
        return obj
    if isinstance(obj, cas_function):
        return obj
    assert isinstance(obj, cas_object)
    return obj


def cas_safe(n):
    if is_constant(n):
        if not isinstance(n, cas_exact_object):
            try:
                return cas_exact(n)
            except Exception as error:
                logging.debug(f'{error.__class__.__name__}: {error.args[0]}')
        return n
    if type(n) is mathfunc:
        return n.composition
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


def _comp_derive(n, var, k):
    return NotImplemented


def getLaTeX(value):
    if hasattr(value, 'LaTeX'):
        LaTeX = value.LaTeX
        if callable(LaTeX):
            return LaTeX()
        return LaTeX
    return str(value)


def _mul_derive_expansion(f, g, v, k, n):
    f_p = _comp_derive(f, v, n)
    g_p = _comp_derive(g, v, k-n)
    c_p = binomial_coeficient(n, k)
    return mul_expression((c_p, f_p, g_p))


def binomial_coeficient(k, n):
    return math.factorial(n)/(math.factorial(n-k)*math.factorial(k))


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
    fhook = f'__{preface}{"r" if r else None}{name}hook__'
    bhook = f'__{preface}{"r" if not r else None}{name}hook__'

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
            logging.debug(f'{error.__class__.__name__}: {error.args[0]}')
            return NotImplemented
    return wrapper


class cas_object:
    safe: typing.Any

    @staticmethod
    def _math_return(return_val):
        if is_constant(return_val):
            return return_val
        if isinstance(return_val, cas_variable):
            return return_val
        try:
            return mathfunc(return_val)
        except Exception as error:
            logging.debug(f'{error.__class__.__name__}: {error.args[0]}')
            return return_val

    def __pos__(self):
        '''Return +self'''
        return self

    @math_return_dec
    def __neg__(self):
        '''Return -self'''
        return mul_expression((-1, self))

    @math_return_dec
    @hook('add', 2, False, (1,))
    def __add__(self, other):
        '''Return self+other'''
        return add_expression((self, other))

    @math_return_dec
    @hook('add', 2, True, (1,))
    def __radd__(self, other):
        '''Return other+self'''
        return self+other

    @math_return_dec
    @hook('sub', 2, False, (1,))
    def __sub__(self, other):
        '''Return self-other'''
        return self+(-other)

    @math_return_dec
    @hook('sub', 2, True, (1,))
    def __rsub__(self, other):
        '''Return other-self'''
        return other+(-self)

    @math_return_dec
    @hook('mul', 2, False, (1,))
    def __mul__(self, other):
        '''Return self*other'''
        return mul_expression((self, other))

    @math_return_dec
    @hook('mul', 2, True, (1,))
    def __rmul__(self, other):
        '''Return other*self'''
        return self*other

    @math_return_dec
    def reciprocal(self):
        '''Return 1/self'''
        return pow_expression(self, -1)

    @math_return_dec
    @hook('truediv', 2, False, (1,))
    def __truediv__(self, other):
        '''Return self/other'''
        if type(other) is mathfunc:
            return self*other.reciprocal()
        return div_shortcut(self, other)

    @math_return_dec
    @hook('truediv', 2, True, (1,))
    def __rtruediv__(self, other):
        '''Return other/self'''
        return self.reciprocal()*other

    @math_return_dec
    @hook('pow', 2, False, (1,))
    def __pow__(self, other):
        '''Return self**other'''
        return pow_expression(self, other)

    @math_return_dec
    @hook('pow', 2, True, (1,))
    def __rpow__(self, other):
        '''Return other**self'''
        return pow_expression(other, self)


class cas_callable:
    fn: tuple
    var: tuple
    _data: dict
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
    exact_return: bool = False

    def check_domain(self, *args):
        pass

    def __call__(self, *args):
        self.check_domain(args)
        get_key = lambda x: (self.arguments_comp.index(self.arguments_call[x[0]]))
        sorter = sorted(enumerate(args), key=get_key)
        args = tuple((i[1] for i in sorter))
        if hasattr(self, '__callhook__'):
            return_val = self.__callhook__(*args)
            if return_val is not NotImplemented:
                return return_val
        if all(map(is_constant, args)) and not self.exact_return:
            return self.shortcut_function(*args)

        for varname, a in zip(self.arguments_comp, args):
            if hasattr(a, 'hook_intercept'):
                idict = self._data['inputs'][varname]
                if a.hook_intercept in idict:
                    return_val = idict[a.hook_intercept](*args)
                    if return_val is not NotImplemented:
                        return return_val
        return self.truecall(*args)

    def _get_data_copy(self):
        return self._data.copy()

    def _set_args_comp(self, value):
        for n in value:
            self._data['inputs'][n] = {}

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
                        self._data['inputs'][var][vmethod[len(var):]] = value
                        return
                raise ValueError('Invalid name')
            if name.startswith('__'):
                self._data['oper'][name[2:-6]] = value
                return
        self._data['custom_data'][name] = value

    def __getattr__(self, name):
        '''Customized attribute storage also necesitates custom attribute lookup'''
        if name.endswith('hook__'):
            if name.startswith('__pass'):
                vmethod = name[6:-6]
                for var in self.arguments_comp:
                    with suppress(KeyError):
                        if vmethod.startswith(var):
                            return self._data['inputs'][var][vmethod[len(var):]]
            if name.startswith('__'):
                with suppress(KeyError):
                    return self._data['oper'][name[2:-6]]
        with suppress(KeyError):
            return self._data['custom_data'][name]
        raise AttributeError(f'{self.__class__.__name__!r} object has no attribute {name!r}')
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
    def __repr__(self):
        ''' representation string for cas_variable '''
        return f'<{self.__class__.__name__} <{self}> at {hex(id(self))}>'

    def __str__(self):
        ''' str for cas_variable '''
        return self.name


class cas_exact_object:
    value: typing.Any

    @classmethod
    def _math_return(return_val):
        if is_constant(return_val):
            return return_val
        if isinstance(return_val, cas_variable):
            return return_val
        try:
            return mathfunc(return_val)
        except Exception as error:
            logging.debug(f'{error.__class__.__name__}: {error.args[0]}')
            return return_val

    def __pos__(self):
        '''Return +self'''
        return self

    def __neg__(self):
        '''Return -self'''
        try:
            return cas_exact(-self.value)
        except Exception:
            return mul_exact_expression((-1, self.value))

    @hook('add', 2, False, (1,), 'exact')
    def __add__(self, other):
        '''Return self+other'''
        if is_rational(other) and is_rational(self):
            if type(other) is not cas_exact:
                other = cas_exact(other)
            return self.value + other.value
        return add_exact_expression((self, other))

    @hook('add', 2, True, (1,), 'exact')
    def __radd__(self, other):
        '''Return other+self'''
        return self+other

    @hook('sub', 2, False, (1,), 'exact')
    def __sub__(self, other):
        '''Return self-other'''
        return self+(-other)

    @hook('sub', 2, True, (1,), 'exact')
    def __rsub__(self, other):
        '''Return other-self'''
        return other+(-self)

    @hook('mul', 2, False, (1,), 'exact')
    def __mul__(self, other):
        '''Return self*other'''
        if is_rational(other) and is_rational(self):
            if type(other) is not cas_exact:
                other = cas_exact(other)
            return self.value * other.value
        return mul_exact_expression((self, other))

    @hook('mul', 2, True, (1,), 'exact')
    def __rmul__(self, other):
        '''Return other*self'''
        return self*other

    def reciprocal(self):
        '''Return 1/self'''
        return pow_exact_expression(self, -1)

    @hook('truediv', 2, False, (1,), 'exact')
    def __truediv__(self, other):
        '''Return self/other'''
        if type(other) is mathfunc:
            return self*other.reciprocal()
        return div_exact_shortcut(self, other)

    @hook('truediv', 2, True, (1,), 'exact')
    def __rtruediv__(self, other):
        '''Return other/self'''
        return self.reciprocal()*other

    @hook('pow', 2, False, (1,), 'exact')
    def __pow__(self, other):
        '''Return self**other'''
        return pow_exact_expression(self, other)

    @hook('pow', 2, True, (1,), 'exact')
    def __rpow__(self, other):
        '''Return other**self'''
        return pow(other, self)

    def is_constant(self):
        return True


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
    def __repr__(self):
        ''' representation string for cas_variable '''
        return f'<{self.__class__.__name__} <{self.name}={self.value}> at {hex(id(self))}>'

    def __str__(self):
        ''' str for cas_variable '''
        return str(self.value)


class cas_exact(cas_exact_object):
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

    def __repr__(self):
        return f'cas_exact({str(self.value)!r})'

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

    def __repr__(self, /):
        '''Return ide representation of self'''
        return f'<{self.__class__.__name__[: -11]} {self} at {hex(id(self))}>'


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

    def __repr__(self, /):
        '''Return ide representation of self'''
        return f'<{self.__class__.__name__[: -11]} {self} at {hex(id(self))}>'


class commutative_expression(cas_expression, tuple):
    LaTeXoper: str

    def __new__(cls, iterable=()):
        '''__new__ for any communative expressions'''
        iterable = tuple(map(cas_safe, iterable))
        if all(map(is_constant, iterable)):
            return cls.cas_exact(iterable)
        self = tuple.__new__(cls, map(comp_extract, iterable))
        self = self._simplify()
        if not isinstance(self, cls):
            return self
        var = []
        for n in self:
            if type(n) is cas_variable:
                var.append(n)
            elif isinstance(n, cas_expression):
                var.extend(n.var)
            elif callable(n):
                var.extend(n.var)
        self.var = remove_duplicates(var)
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
    """
    @abstractmethod
    def var(self):
        '''abstract method: create as a @property
Return variables involved in expression'''
        pass

    @abstractmethod
    def fn(self):
        '''abstract method: create as a @property
Return functions involved in expression'''
        pass
"""
    def __hash__(self, /):
        '''hash for communative expression '''
        return hash((self.oper, tuple(self)))

    def __str__(self, /):
        '''string for communative expression'''
        return '('+self.oper.join(map(str, self))+')'

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
        self = tuple.__new__(cls, map(comp_extract, iterable))
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
        '''string for communative expression'''
        return '('+str(self.value)+')'

    def _extract_num(self, /):
        ''' seperates rationals from non-rational expressions'''
        logging.debug('seperating rationals from non-rational expressions')
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

        # extracts constants
        numbers, expressions = self._extract_num()
        # product of constants
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
            if value.oper == '^':
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
        if type(value) is mathfunc:
            value = value.composition

        if isinstance(value, cas_expression):
            if value.oper == '^':
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


mul_exact_expression.cas_inexact = mul_expression


class div_exact_shortcut(cas_exact_non_commutative_expression):
    def __new__(cls, a, b):  # TEMPORARY
        return a*(b**-1)


class div_shortcut(non_commutative_expression):
    def __new__(cls, a, b):  # TEMPORARY
        return a*(b**-1)


class pow_exact_expression(cas_exact_non_commutative_expression):
    oper = '^'
    hook_intercept = 'pow'
    true_operation = lambda x, y: x**y

    def __new__(cls, a, b):
        if is_rational(a) and validation.is_integer(b):
            return a**b
        self = super(cas_exact_non_commutative_expression, cls).__new__(cls)
        self.a = a
        self.b = b
        self.value = a.value**b.value
        return self._simplify()

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
        return self._simplify()

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
        return '{'+getLaTeX(self.a)+'}^{'+getLaTeX(self.b)+'}'

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


class cas_exact_nest(cas_exact_object):
    pass


class cas_function:
    func: types.FunctionType
    string: str

    def __new__(cls, func, args):
        self = super(cas_function, cls).__new__(cls)
        self.func = func
        self.args = args
        self.prime = self.func.prime
        self.prime_cycle = self.func.prime_cycle
        var = []
        fn = [func]
        for arg in args:
            if is_constant(arg):
                continue
            if isinstance(arg, cas_variable):
                var.append(arg)
                continue
            if isinstance(arg, cas_expression):
                var.extend(arg.vars)
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
            for n, arg in enumerate(args):
                string = string.replace(f'<{n}>', f'({arg})')
        else:
            string = func.__name__+'('
            string += ', '.join(map(str, args))
            string += ')'
        self.string = string
        self.arg_data_func_wrap = tmd[func.__name__]
        if hasattr(func, 'LaTeX'):
            self.LaTeX = func.LaTeX
        return self

    def __str__(self):
        return self.string

    def _comp_derive(self, v, k):
        if k == 0:
            return self
        if v not in self.var:
            return 0

        if self.raw_vars.count(v) == 1:
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
            return func(*args)
        args = tuple(map(cas_safe, args))
        return mathfunc(cas_function(wrap, args))

    wrap.prime = {}
    wrap.format = None
    wrap.prime_cycle = {}
    return wrap


class mathfunc(cas_callable, cas_object):
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
        self._data = {'inputs': {}, 'pass': {}, 'oper': {}, 'custom_data': {}}
        self.special = {'arguments_comp': self._set_args_comp}
        self.composition = func
        self.safe = self.composition
        self.exact_composition = self.composition
        self.true_call = self.composition
        if isinstance(func, cas_function):
            self.__name__ = func.func.__name__
        else:
            self.__name__ = None
        self.arguments_comp = func.var
        self.arguments_call = func.var
        self.var = func.var
        self.fn = func.fn
        self.function = str(func)
        self.__doc__ = 'Return '+self.function
        var_list_str = ', '.join(map(str, self.var))
        space = {fn.__name__: fn for fn in func.fn}
        _short = eval(f'lambda {var_list_str}: {self.function}', None, space)
        self.shortcut_function = _short
        _get = eval(f'lambda self, {var_list_str}: {self.function}', None, space)
        self.__call__ = _get.__get__(self)

        self._data = {'composition': func, 'oper': {}, 'custom_data': {}}
        return self

    @ math_return_dec
    def truecall(self, *args):
        return self.composition.evaluate(*args)

    def __repr__(self):
        '''repr for mathfunc'''
        return f'<mathfunc {self} at {hex(id(self))}>'

    def __str__(self):
        '''str for mathfunc'''
        return self.function

    def __hash__(self, /):
        '''hash for mathfunc'''
        return hash(self.composition)

    def LaTeX(self):
        return getLaTeX(self.composition)

@cas_func_wrap
def f(a, b):
    return a+b

pi = cas_constant('pi', math.pi, '\\pi')

x = cas_variable('x')

# eof
