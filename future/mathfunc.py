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
import functools

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

        @functools.wraps(function)
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
    @functools.wraps(function)
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
    fns: tuple
    vars: tuple
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
    exact_return: bool = False

    def __new__(cls, composition):
        self = super(cas_callable, cls).__new__(cls)
        self.__data = {'inputs': {}, 'pass': {}, 'oper': {}, 'custom_data': {}}
        self.composition = composition
        self.special = {'arguments_comp': self.__set_args_comp}
        self.safe = composition
        self.exact_composition = composition
        self.true_call = composition
        if isinstance(composition, types.FunctionType):
            self.arguments_comp = composition.__code__.co_varnames
            self.arguments_call = composition.__code__.co_varnames
        elif isinstance(composition, cas_object):
            self.arguments_comp = composition.var
            self.arguments_call = composition.var
        return self

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
                idict = self.__data['inputs'][varname]
                if a.hook_intercept in idict:
                    return_val = idict[a.hook_intercept](*args)
                    if return_val is not NotImplemented:
                        return return_val
        return self.truecall(*args)

    def _get_data_copy(self):
        return self.__data.copy()

    def __set_args_comp(self, value):
        for n in value:
            self.__data['inputs'][n] = {}

    def __setattr__(self, name: str, value) -> None:
        '''Intercepts attribute setting, for customized storage'''
        if self.__is_frozen:
            raise AttributeError(f'attributes of {self!r} are no longer writeable')
        if name in self.__annotations__:
            if name in ('arguments_call', 'fn', 'vars') and hasattr(self, name):
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
    special: dict = {'arguments_comp': __set_args_comp}


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


def math_return_dec(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return_val = function(*args, **kwargs)
            return cas_object._math_return(return_val)
        except Exception as error:
            logging.debug(f'{error.__class__.__name__}: {error.args[0]}')
            return NotImplemented
    return wrapper


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

    # INITIALIZATION #

    def __new__(cls, name, value):
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

        self.name = name
        self.names[name] = self
        self.value = value

        return self

    # CONVERSIONS #
    def __repr__(self):
        ''' representation string for cas_variable '''
        return f'<{self.__class__.__name__} <{self}={self.value}> at {hex(id(self))}>'

    def __str__(self):
        ''' str for cas_variable '''
        return self.name


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

    def __repr__(self):
        return f'cas_exact({str(self.value)!r})'


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
        if len(self.vars) != len(args):
            raise ValueError('Incorrect number of arguments entered')
        for arg, var in zip(args, self.vars):
            var._set(arg)
        value = self._evaluate()
        for var in self.vars:
            var._reset()
        return value

    @abstractmethod
    def vars(self):
        '''abstract method: create as a @property
Return variables involved in expression'''
        pass

    @abstractmethod
    def fn(self):
        '''abstract method: create as a @property
Return functions involved in expression'''
        pass

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
    pass


def comp_extract(obj):
    if isinstance(obj, mathfunc):
        return obj.composition
    if is_constant(obj):
        if not isinstance(obj, cas_exact_object):
            return cas_exact(obj)
        return obj
    assert isinstance(obj, cas_object)
    return obj


class commutative_expression(cas_expression, tuple):
    def __new__(cls, iterable=()):
        '''__new__ for any communative expressions'''
        if all(map(is_constant, iterable)):
            return cls.cas_exact(iterable)
        self = tuple.__new__(cls, map(comp_extract, iterable))
        self = self._simplify()
        var = []
        for n in self:
            if type(n) is cas_variable:
                var.append(n)
            elif isinstance(n, cas_expression):
                var.extend(n.vars)
            elif callable(n):
                var.extend(n.info)
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

    def __hash__(self, /):
        '''hash for communative expression '''
        return hash((self.oper, tuple(self)))

    def __str__(self, /):
        '''string for communative expression'''
        return '('+self.oper.join(map(str, self))+')'

    def _evaluate(self):
        '''evaluate self at values of variables'''
        return self.__class__(map(_get, self))


class non_commutative_expression(cas_expression):
    vars: tuple
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
        return current.firstwrap(*map(_get, current.args))
    return current


class cas_exact_commutative_expression(cas_exact_expression, tuple):
    pass


class cas_exact_non_commutative_expression(cas_exact_expression):
    pass


class add_exact_expression(cas_exact_commutative_expression):
    pass


class add_expression(commutative_expression):
    oper = '+'
    hook_intercept = 'add'
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

        if callable(value):
            if not value.expressionable:
                raise ValueError('function must be expressionable')
            return 1, value

        if isinstance(value, cas_variable):
            return 1, value
        raise TypeError(f'invalid type recieved: type {type(value)}')

    def _comp_derive(self, var, k, /):
        '''computes kth partial of self with respect to var'''
        return add_expression(map(lambda x: _comp_derive(x, var, k), self))


def _comp_derive(n, var, k):
    return NotImplemented


class mul_exact_expression(cas_exact_commutative_expression):
    pass


class mul_expression(commutative_expression):
    oper = '+'
    hook_intercept = 'add'
    cas_exact = mul_exact_expression

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


def _mul_derive_expansion(f, g, v, k, n):
    f_p = _comp_derive(f, v, n)
    g_p = _comp_derive(g, v, k-n)
    c_p = binomial_coeficient(n, k)
    return mul_expression((c_p, f_p, g_p))


def binomial_coeficient(k, n):
    return math.factorial(n)/(math.factorial(n-k)*math.factorial(k))


class div_exact_shortcut(cas_exact_non_commutative_expression):
    pass


class div_shortcut(non_commutative_expression):
    def __new__(cls, a, b):  # TEMPORARY
        return a*(b**-1)


class pow_exact_expression(cas_exact_non_commutative_expression):
    pass


def remove_duplicates(tup):  # TEMPORARY:
    return tuple(set(tup))


class pow_expression(non_commutative_expression):
    def __new__(cls, a, b):
        '''__new__ for non-communative expressions'''
        self = super(non_commutative_expression, cls).__new__(cls)
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
            elif isinstance(n, cas_expression):
                var.extend(n.vars)
            elif callable(n):
                var.extend(n.info)
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


def getLaTeX(value):
    if hasattr(value, 'LaTeX'):
        LaTeX = value.LaTeX
        if callable(LaTeX):
            return LaTeX()
        return LaTeX
    return str(value)


class cas_exact_nest(cas_exact_object):
    pass


class cas_function(cas_callable):
    pass


class mathfunc(cas_callable, cas_object):
    pass


def test(a, b):
    return a, b


t = cas_callable(test)

# eof
