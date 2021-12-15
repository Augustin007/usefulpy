'''
mathfunc

DESCRIPTION
This file contains function with wrappers that allow for pretty cool stuff

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
   Reimplemented CAS system, removed expression_check, now supports multiple variables
   using the cas_variable class.
   __all__ added.
'''

### DUNDERS ###
__author__ = 'Austin Garcia'
__version__ = '1.0.0'
if __name__ == '__main__': #To account for relative imports when directly run
    __package__ = 'usefulpy.mathematics'
__all__ = ('S', 'acos', 'acosh', 'acot', 'acoth', 'acsc', 'acsch', 'asec',
           'asech', 'asin', 'asinh', 'atan', 'atan2', 'atanh',
           'binomial_coeficient', 'cas_variable', 'cbrt', 'ceil', 'cis',
           'cos', 'cosh', 'cot', 'coth', 'csc', 'csch', 'cube', 'exp',
           'expm1', 'floor', 'from_str', 'icbrt', 'is_constant', 'isqrt',
           'ln', 'log', 'log1p', 'log2', 'mathfunc', 'mathfunction', 'polynomial', 
           'sec', 'sech', 'sigmoid', 'sin', 'sinh', 'sqrt', 'square', 'tan', 
           'tanh', 'tesser', 'x', 'y', 'z')

### IMPORTS ###
# Utilities
from collections import Counter, abc
from abc import abstractmethod
import types
from functools import cache, wraps
# Maths
import math
import cmath
from decimal import Decimal
from fractions import Fraction
# Relative imports
from .. import decorators
from .. import validation
import logging

if __name__ == '__main__':
    level = validation.intinput('enter logging level: ')
    fmt = '[%(levelname)s] %(name)s - %(message)s'
    logging.basicConfig(level=level, format=fmt)
    logging.root.setLevel(level)

constants = (int, float, complex, Decimal, Fraction)
def is_constant(n):
    '''Checks whether n is constant for cas engine'''
    if type(n) in constants:
        return True
    try: return n.is_constant()
    except: return False

def _comp_derive(n, var, k):
    '''Computes the kth partial derivative of n with respect to var'''
    # Making sure k is valid
    assert k >= 0 
    assert type(k) is int 

    # 0th derivative means nothing
    if k == 0:
        return n

    #logging computation
    logging.info(f'Computing {k} partial of {safe_str(n)} with respect to {var.name}')

    #catch trivial and identity derivatives
    if k == 1 and var == n:
        return 1
    elif is_constant(n) or isinstance(n, cas_variable):
        return 0

    # Call attributes
    if isinstance(n, cas_expression):
        return n._comp_derive(var, k)
    if callable(n):
        return n.derive(var, k)
    
    raise TypeError(f'Invalid type, type {type(n)}')

class cas_variable:
    '''variable class for cas engine'''
    
    name:str
    names:dict = {} #stores all created variables
    value = None

    ### INITIALIZATION ###
    
    def __new__(cls, name):
        '''__new__ for cas_variable'''
        if name in cls.names: return cls.names[name]
        
        # Check name validity
        e = False
        try:
            assert type(name) == str
            assert len(name) in range(1, 4)
            assert '.' not in name
            exec(f'{name}=0')
        except: e = True
        if e:
            raise ValueError(f'Invalid name recieved for cas_variable: {name!r}')

        # create and log the variable
        logging.info(f'Variable created: {name!r}')
        self = super(cas_variable, cls).__new__(cls)

        self.name = name
        self.names[name] = self
        
        return self

    ### SET/RESET ###
    # set and reset for internal capabilities

    def _set(self, value):
        self.value = value

    def _reset(self):
        self.value = None

    ### CONVERSIONS ###
    def __repr__(self):
        ''' representation string for cas_variable '''
        return f'<{self.__class__.__name__} {self} at {hex(id(self))}>'

    def __str__(self):
        ''' str for cas_variable '''
        return '<'+self.name+'>'

    ### ARITHMETIC ###
    def _math_return(self, return_val):
        if is_constant(return_val):
            return return_val
        if isinstance(return_val, cas_variable):
            return return_val
        try: return mathfunc(return_val)
        except Exception as error:
            logging.debug(f'{error.__class__.__name__}: {error.args[0]}')
            return return_val
        

    def __pos__(self):
        '''Return +self'''
        return self
    
    def __neg__(self):
        '''Return -self'''
        try: return self._math_return(mul_expression((-1, self)))
        except Exception as error:
            logging.debug(f'{error.__class__.__name__}: {error.args[0]}')
            return NotImplemented

    def __add__(self, other):
        '''Return self+other'''
        try: return self._math_return(add_expression((self, other)))
        except Exception as error:
            logging.debug(f'{error.__class__.__name__}: {error.args[0]}')
            return NotImplemented

    def __radd__(self, other):
        '''Return other+self'''
        try: return self+other
        except Exception as error:
            logging.debug(f'{error.__class__.__name__}: {error.args[0]}')
            return NotImplemented

    def __sub__(self, other):
        '''Return self-other'''
        try: return self+ (-other)
        except Exception as error:
            logging.debug(f'{error.__class__.__name__}: {error.args[0]}')
            return NotImplemented

    def __rsub__(self, other):
        '''Return other-self'''
        try: return other+ (-self)
        except Exception as error:
            logging.debug(f'{error.__class__.__name__}: {error.args[0]}')
            return NotImplemented

    def __mul__(self, other):
        '''Return self*other'''
        try: return self._math_return(mul_expression((self, other)))
        except Exception as error:
            logging.debug(f'{error.__class__.__name__}: {error.args[0]}')
            return NotImplemented

    def __rmul__(self, other):
        '''Return other*self'''
        try: return self*other
        except Exception as error:
            logging.debug(f'{error.__class__.__name__}: {error.args[0]}')
            return NotImplemented

    def reciprocal(self):
        '''Return 1/self'''
        try: return self._math_return(pow_expression(self, -1))
        except Exception as error:
            logging.debug(f'{error.__class__.__name__}: {error.args[0]}')
            return NotImplemented

    def __truediv__(self, other):
        '''Return self/other'''
        try:
            if type(other) is mathfunc:
                return self*other.reciprocal()
            return self*(1/other)
        except Exception as error:
            logging.debug(f'{error.__class__.__name__}: {error.args[0]}')
            return NotImplemented

    def __rtruediv__(self, other):
        '''Return other/self'''
        try: return self.reciprocal()*other
        except Exception as error:
            logging.debug(f'{error.__class__.__name__}: {error.args[0]}')
            return NotImplemented

    def __pow__(self, other):
        '''Return self**other'''
        try: return self._math_return(pow_expression(self, other))
        except Exception as error:
            logging.debug(f'{error.__class__.__name__}: {error.args[0]}')
            return NotImplemented

    def __rpow__(self, other):
        '''Return other**self'''
        try: return self._math_return(pow_expression(other, self))
        except Exception as error:
            logging.debug(f'{error.__class__.__name__}: {error.args[0]}')
            return NotImplemented

class cas_expression:
    '''Abstract class for expression in cas'''
    oper = ''

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

    def __call__(self, *args):
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
        return f'<{self.__class__.__name__[:-11]} {self} at {hex(id(self))}>'

def comp_extract(x):
    if type(x) is mathfunc:
        return x.composition
    return x
#removes mathfunc classes in favor of their cas composition

class commutative_expression(cas_expression, tuple):
    '''Abstract class that represents communative expressions'''
    def __new__(cls, iterable=()):
        '''__new__ for any communative expressions'''
        self = tuple.__new__(cls, map(comp_extract, iterable))
        return self._simplify()

    @property
    def vars(self):
        var = []
        for n in self:
            if type(n)==cas_variable:
                var.append(n)
            elif isinstance(n, cas_expression):
                var.extend(n.vars)
            elif callable(n):
                var.extend(n.info)
        return set(var)

    @property
    def fn(self, /):
        fn = []
        for n in self:
            if isinstance(n, cas_expression) or callable(n):
                fn.extend(n.fn)
        return set(fn)

    def _evaluate(self):
        '''evaluate self at values of variables'''
        return self.__class__(map(_get, self))

    def __eq__(self, other, /):
        ''' Return self==other'''
        if isinstance(other, cas_expression):
            if self.oper == other.oper:
                return Counter(self)==Counter(other)
        return False

    def _expand(self, /):
        ''' Expands according to assosiative property'''
        for n in self:
            if type(n)==type(self):
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
        return hash((self.oper, *(Counter(self).items())))

    def __str__(self, /):
        '''string for communative expression'''
        return '('+self.oper.join(map(safe_str, self))+')'

    def view_string(self, /):#might be removed
        '''viewing string'''
        return '('+self.oper.join(map(safe_str, self))+')'

class non_commutative_expression(cas_expression):
    '''Abstract class that represents non-communative expressions'''
    def __new__(cls, a, b):
        '''__new__ for non-communative expressions'''
        self = super(non_commutative_expression, cls).__new__(cls)
        if type(a) is mathfunc:
            a = a.composition
        if type(b) is mathfunc:
            b = b.composition
        self.a = a
        self.b = b
        return self._simplify()

    @property
    def vars(self, /):
        var = []
        for n in (self.a, self.b):
            if type(n)==cas_variable:
                var.append(n)
            elif isinstance(n, cas_expression):
                var.extend(n.vars)
            elif callable(n):
                var.extend(n.info)
        return set(var)

    @property
    def fn(self, /):
        fn = []
        for n in (self.a, self.b):
            if isinstance(n, cas_expression) or callable(n):
                fn.extend(n.fn)
        return set(fn)

    def __eq__(self, other, /):
        '''Return self==other'''
        if isinstance(other, cas_expression):
            if self.oper == other.oper:
                return (self.a, self.b)==(other.a, other.b)
        return False

    def __hash__(self, /):
        '''hash for non-communative expression'''
        return hash((self.a, self.b))

    def _evaluate(self):
        '''evaluate self at values of variables'''
        return self.__class__(_get(self.a), _get(self.b))

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

class add_expression(commutative_expression):
    oper = '+'
    def _simplify(self, /):
        '''Simplifies addition expression'''
        # Fast cases
        if len(self) == 1: return self[0]
        if len(self) == 0: return 0

        # Seperates constants out
        numbers, expressions = self._extract_num()
        # adds constants
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
                runcount +=1
                continue
            if count != 0:
                if count != 1:
                    expressions_short.append(mul_expression((count, value)))
                    continue
                expressions_short.append(value)

        # Return clean results
        if len(expressions_short)==0:
            return number
        if number==0:
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
            #pow value count not implemented
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
        return add_expression(map(lambda x:_comp_derive(x, var, k), self))


class mul_expression(commutative_expression):
    oper = '*'
    
    def _simplify(self, /):
        '''Simplifies multiplication expression'''
        # fast return
        if len(self) == 1: return self[0]
        if len(self) == 0: return 1
        if 0 in self: return 0

        # expands accross addition expressions within it
        for count, value in enumerate(self):
            if type(value) == add_expression:
                distributor = lambda x: mul_expression((x, *self[:count], *self[count+1:]))
                run = map(distributor, value)
                return add_expression(run)

        # extracts constants
        numbers, expressions = self._extract_num()
        #product of constants
        number = math.prod(numbers)
        #extracts count value information from expressions
        expressions_extract = list(map(self._data_extract, expressions))

        #Loop through creating a list of simplified data
        expressions_short = []
        while expressions_extract:
            count, value = expressions_extract.pop(0)
            runcount = 0
            for new_count, new_value in tuple(expressions_extract):
                if new_value == value:
                    count += new_count
                    expressions_extract.pop(runcount)
                    continue
                runcount +=1
                continue
            if count != 0:
                if count != 1:
                    expressions_short.append(pow_expression(value, count))
                    continue
                expressions_short.append(value)

        # Return clean results
        if len(expressions_short)==0:
            return number
        if number==1:
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
            f = mul_expression(b[:length//2])
            g = mul_expression(b[length//2:])
        else:
            if len(b)==1:
                return mul_expression((n, _comp_derive(b[0], var, k)))
            f = b[0]
            g = b[1]
        summation = [_mul_comp_expansion_derive(f, g, var, k, n) for n in range(k+1)]
        return add_expression(summation)

def _mul_comp_expansion_derive(f, g, v, k, n):
    f_p = _comp_derive(f, v, n)
    g_p = _comp_derive(g, v, k-n)
    c_p = binomial_coeficient(n, k)
    return mul_expression((c_p, f_p, g_p))

class pow_expression(non_commutative_expression):
    oper = '^'
    def _simplify(self, /):
        '''Simplifies power expression '''
        # special cases
        if self.b == 0:
            return 1
        if self.b == 1:
            return self.a
        if self.a == 0:
            return 0
        if self.a ==1:
            return 1
        if is_constant(self.a) and is_constant(self.b):
            return self.a**self.b
        if type(self.a) is mul_expression:
            return mul_expression(map(lambda n:pow_expression(n, self.b), self.a))
        if type(self.a) is pow_expression:
            return pow_expression(self.a.a, mul_expression((self.a.b, self.b)))
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
            first_derivative = mul_expression((self.b, pow_expression(self.a, self.b-1), _comp_derive(self.a, var, 1)))
            return _comp_derive(first_derivative, var, k-1)
        if is_constant(self.a):
            return _comp_derive(mul_expression((ln(self.a), self)), var, k-1)
        pross = mul_expression((ln(self.a).composition, self.b))
        internal = _comp_derive(pross, var, 1)
        return _comp_derive(mul_expression((self, internal)), var, k-1)

    def __str__(self, /):
        '''String for power expression'''
        return f'({safe_str(self.a)}**{safe_str(self.b)})'

    def view_string(self, /):
        '''Viewing string'''
        return '('+safe_str(self.a)+'**'+safe_str(self.b)+')'

def expression_function(func):
    '''Wraps a function to make it work in the cas engine.'''
    @wraps(func)
    def exchange(*args):
        return wrap(*map(mathfunc_process, args))
    
    @cache
    def wrap(*args):
        if all(map(is_constant, args)):
            return func(*args)
        args = tuple(map(mathfunc_process, args))
        var = []
        fn = [func]
        for arg in args:
            if is_constant(arg): continue
            if isinstance(arg, cas_variable):
                var.append(arg)
                continue
            if isinstance(arg, cas_expression):
                var.extend(arg.vars)
                fn.extend(arg.fn)
                continue
            if callable(arg):
                if arg.expressionable:
                    var.extend(arg.info)
                    fn.extend(arg.fn)
                    continue
            
        var = set(var)
        var_names = ', '.join(map(lambda x: x.name, var))
        if func.__doc__:
            exec(f'def {func.__name__}({var_names}):\t\n    """{func.__doc__}"""\n    pass ')
        else:
            exec(f'def {func.__name__}({var_names}):pass')
        
        @wraps(eval(func.__name__))
        def _internal_exchange(*args2):
            return _internal_wrap(*args2)
        
        @cache
        def _internal_wrap(*args2):
            if len(args2) != len(var):
                raise ValueError('Length of args != length of var')
            for v, a in zip(var, args2):
                v._set(a)
            return_val = wrap(*map(_get, args))
            for v in var:
                v._reset()
            return return_val

        def derive(v, k):
            if k == 0: return _internal_exchange
            if not v in var: return 0

            if args.count(v) == 1:
                i = args.index(v)
                if i in exchange.prime_cycle:
                    cycle = exchange.prime_cycle[i]
                    if cycle <= k:
                        return derive(v, k%cycle)

            run = []
            for n, a in enumerate(args):
                if is_constant(a):
                    continue
                if isinstance(a, cas_variable):
                    if a != v:
                        continue
                    ap = 1
                else:
                    ap = _comp_derive(a, v, 1)
                if ap:
                    if len(exchange.prime[n]) == 2:
                        fp = exchange.prime[n][0](*get_args(args, exchange.prime[n][1]))
                        fp = fp.composition
                    else:
                        fp = exchange.prime[n]
                    
                    run.append(mul_expression((fp, ap)))
            return _comp_derive(add_expression(run), v, k-1)
        
        if exchange.format:
            view_string = exchange.format
            for n, arg in enumerate(args):
                view_string = view_string.replace(f'<{n}>', '('+safe_str(arg)+')')
            
        else:
            view_string = func.__name__+'('
            view_string += ', '.join(map(safe_str, args))
            view_string += ')'
        
        fn = set(fn)
        _internal_exchange.func = func
        _internal_exchange.firstwrap=wrap
        _internal_exchange.expressionable = True
        _internal_exchange.info = var
        _internal_exchange.args = args
        _internal_exchange.view_str = view_string
        _internal_exchange.derive = derive
        _internal_exchange.old_exchange = exchange
        _internal_exchange.fn = fn
        
        return mathfunc(_internal_exchange)
    exchange.prime = {}
    exchange.format = None
    exchange.prime_cycle = {}
    return exchange

def get_args(args, selector):
    '''get args according to selector'''
    return [args[select] for select in selector]

def safe_str(expression):
    '''Return a 'safe' string for evaluation'''
    if isinstance(expression, cas_expression):
        return expression.view_string()
    if isinstance(expression, cas_variable):
        return expression.name
    if callable(expression):
        return expression.view_str
    return str(expression)

def from_str(string):
    '''NotImplemented: Will return mathfunc from string'''
    return NotImplemented

def binomial_coeficient(k, n):
    return math.factorial(n)/(math.factorial(n-k)*math.factorial(k))
class mathfunc:
    '''This class works as a wrapper for functions to support function
differentiation'''
    ### ANNOTATIONS ###
    __data:dict
    __doc__:str
    shortcut_function:types.FunctionType
    variables:set
    function:str
    __name__:str
    inverse:types.FunctionType
    interval = None
    __is_frozen:bool = False
    __slots__:tuple = ('composition',)

    ### INITIALIZATION ###
    def __new__(cls, func):
        '''__new__ for mathfunc class, wraps function 'func'.'''
        if type(func) == mathfunc: return func
        assert callable(func)
        if isinstance(func, cas_expression):pass
        elif not func.expressionable:
            raise ValueError('function is not expressionable')
        self = super(mathfunc, cls).__new__(cls)
        self.composition = func
        if isinstance(func, cas_expression):
            self.variables = func.vars
            self.__doc__ = None
            self.function = func.view_string()
            self.__name__ = None
        else:
            self.variables = func.info
            self.__doc__ = func.__doc__
            self.function = func.view_str
            self.__name__ = func.__name__
        var_list_str = ', '.join(map(safe_str, self.variables))
        space = {fn.__name__:fn for fn in func.fn}
        self.shortcut_function = eval(f'lambda {var_list_str}: {self.function}', None, space)
        
        self.__data = {'composition':func, 'prime':{'available':[]}, 'oper':{}, 'custom_data':{}}
        return self

    # def __getattr__
    # def __setattr__

    ### UTILITIES ###

    def __eq__(self, other, /):
        '''return self == other'''
        try: return self-other ==0
        except AttributeError: return False

    def __hash__(self, /):
        '''hash for mathfunc'''
        return hash(self.composition)

    def __repr__(self):
        '''repr for mathfunc'''
        return f'<mathfunc {self} at {hex(id(self))}>'

    def __str__(self):
        '''str for mathfunc'''
        return self.function

    def __call__(self, *args):
        '''calls mathfunc'''
        if all(map(is_constant, args)):
            return self.shortcut_function(*args)
        return mathfunc(self.composition(*map(mathfunc_process, args)))

    ### ARITHMETIC ###

    def _math_return(self, return_val):
        if is_constant(return_val):
            return return_val
        if isinstance(return_val, cas_variable):
            return return_val
        try: return mathfunc(return_val)
        except Exception as error:
            logging.debug(f'{error.__class__.__name__}: {error.args[0]}')
            return return_val

    def __pos__(self):
        '''Return +self'''
        return self
    
    def __neg__(self):
        '''Return -self'''
        try: return self._math_return(mul_expression((-1, self)))
        except Exception as error:
            logging.debug(f'{error.__class__.__name__}: {error.args[0]}')
            return NotImplemented

    def __add__(self, other):
        '''Return self+other'''
        try: return self._math_return(add_expression((self, other)))
        except Exception as error:
            logging.debug(f'{error.__class__.__name__}: {error.args[0]}')
            return NotImplemented

    def __radd__(self, other):
        '''Return other+self'''
        try: return self+other
        except Exception as error:
            logging.debug(f'{error.__class__.__name__}: {error.args[0]}')
            return NotImplemented

    def __sub__(self, other):
        '''Return self-other'''
        try: return self+ (-other)
        except Exception as error:
            logging.debug(f'{error.__class__.__name__}: {error.args[0]}')
            return NotImplemented

    def __rsub__(self, other):
        '''Return other-self'''
        try: return other+ (-self)
        except Exception as error:
            logging.debug(f'{error.__class__.__name__}: {error.args[0]}')
            return NotImplemented

    def __mul__(self, other):
        '''Return self*other'''
        try: return self._math_return(mul_expression((self, other)))
        except Exception as error:
            logging.debug(f'{error.__class__.__name__}: {error.args[0]}')
            return NotImplemented

    def __rmul__(self, other):
        '''Return other*self'''
        try: return self*other
        except Exception as error:
            logging.debug(f'{error.__class__.__name__}: {error.args[0]}')
            return NotImplemented

    def reciprocal(self):
        '''Return 1/self'''
        try: return self._math_return(pow_expression(self, -1))
        except Exception as error:
            logging.debug(f'{error.__class__.__name__}: {error.args[0]}')
            return NotImplemented

    def __truediv__(self, other):
        '''Return self/other'''
        try:
            if type(other) is mathfunc:
                return self*other.reciprocal()
            return self*(1/other)
        except Exception as error:
            logging.debug(f'{error.__class__.__name__}: {error.args[0]}')
            return NotImplemented

    def __rtruediv__(self, other):
        '''Return other/self'''
        try: return self.reciprocal()*other
        except Exception as error:
            logging.debug(f'{error.__class__.__name__}: {error.args[0]}')
            return NotImplemented

    def __pow__(self, other):
        '''Return self**other'''
        try: return self._math_return(pow_expression(self, other))
        except Exception as error:
            logging.debug(f'{error.__class__.__name__}: {error.args[0]}')
            return NotImplemented

    def __rpow__(self, other):
        '''Return other**self'''
        try: return self._math_return(pow_expression(other, self))
        except Exception as error:
            logging.debug(f'{error.__class__.__name__}: {error.args[0]}')
            return NotImplemented

    def differentiate(self, var, k):
        if var not in self.variables:
            return 0
        return self._math_return(_comp_derive(self.composition, var, k))

    def partial(self, var):
        return self.differentiate(var, 1)

def mathfunc_process(arg):
        if type(arg) is mathfunc:
            return arg.composition
        return arg
mathfunction = expression_function

@mathfunction
def exp(x, /):
    '''Return e to the power of x'''
    try: return math.exp(x)
    except Exception: pass
    try: return cmath.exp(x)
    except Exception: pass
    try: return x.exp()
    except Exception: pass
    try: return math.e**x
    except Exception: pass
    raise TypeError(f'invalid type, type {type(x).__name__}')
exp.prime[0] = exp, (0, )
exp.prime_cycle[0] = 1

@mathfunction
def floor(x, /):
    '''Return the floor of x'''
    try: return math.floor(x) # math's floor already allows for custom types
    except Exception: pass
    # I feel that imaginary types should still work
    # They bring it to the closest gaussian number
    try: return math.floor(x.real) + math.floor(x.imag)*1j if type(x) is complex else x.__floor__()
    except Exception: pass
    raise TypeError(f'invalid type, type {type(x).__name__}')
floor.prime[0] = 0

@mathfunction
def ceil(x, /):
    '''Return the ceil of x'''
    try: return math.ceil(x)# math's ceil already allows for custom types
    except Exception: pass
    # imaginary type is not built in.
    try: return ceil(x.real) + ceil(x.imag)*1j if type(x) is complex else x.__ceil__()
    except Exception: pass
    raise TypeError(f'invalid type, type {type(x).__name__}')
ceil.prime[0] = 0

x = cas_variable('x')
y = cas_variable('y')
z = cas_variable('z')

@mathfunction
def S(x, /):
    '''Sigmoid function'''
    epow = exp(-x)
    return 1/(1+epow)
sigmoid = S
sigmoid.prime[0] = exp(-x)/((1+exp(-x))**2), (0,)

@mathfunction
def expm1(x, /):
    '''Return exp(x)-1'''
    try: return math.expm1(x)
    except: return exp(x)-1

expm1.prime[0] = exp, (0,)

@mathfunction
def sqrt(x, /):
    '''Return the square root of x'''
    try: return math.sqrt(x)
    except Exception: pass
    try: return cmath.sqrt(x)
    except Exception: pass
    try: return x**(1/2)
    except Exception: pass
    raise ValueError('math domain error')
sqrt.prime[0] = (0.5)*x**(-1/2), (0,)

@mathfunction
def isqrt(x, /):
    '''Return the floored square root of x'''
    try: return math.isqrt(x)
    except: return floor(sqrt(x))
isqrt.prime[0] = 0

@mathfunction
def cbrt(x, /):
    '''Return the cube root of x'''
    try: return x**(1/3)
    except Exception: pass
    raise ValueError('math domain error')
cbrt.prime[0] = (1/3)*x**(-2/3), (0,)

@mathfunction
def icbrt(x, /):
    '''Return the floored cube root of x'''
    try: return int(x**(1/3))
    except Exception: pass
    raise ValueError('math domain error')
icbrt.prime[0] = (0,)

@mathfunction
def square(x, /):
    '''Return x**2'''
    return x*x
square.prime[0] = 2*x, (0,)

@mathfunction
def cube(x, /):
    '''Return x**3'''
    return x*x*x
cube.prime[0] = 3*x**2, (0,)

@mathfunction
def tesser(x, /):
    '''Return x**4'''
    return x*x*x*x
cube.prime[0] = 4*x**3, (0,)

@mathfunction
def ln(x, /):
    '''Return the natural logarithm of x
    recources to x.ln() or x.log(e) if ln cannot be found'''
    if x == 0:
        raise ValueError('math domain error')
    try: return math.log(x)
    except Exception: pass
    try: return cmath.log(x)
    except Exception: pass    
    try: return x.ln()
    except Exception: pass
    try: return x.log(math.e)
    except Exception: pass
    raise TypeError('Natural logarithm cannot be found of a type %s.' % type(x).__name__)
ln.prime[0] = x**-1, (0,)

@mathfunction
def log(base, x):
    ''' log([base=10], x)
    Return the log base 'base' of x
    recources to x.log(base) and base.rlog(x) if log cannot be found'''
    if x == base: return 1
    if 0 in (x, base):
        raise ValueError('math domain error')
    if base == 1:
        raise ValueError('math domain error')
    try: return math.log(x, base)
    except Exception: pass
    try: return cmath.log(x, base)
    except Exception: pass
    try: return x.log(base)
    except Exception: pass
    try: return base.rlog(x)
    except Exception: pass
    raise TypeError('Logarithm cannot be found of a type %s.' % type(x))
log.prime[0] = (-ln(x))*((ln(y))**-2)*(y**-1), (0, 1)
log.prime[1] = (x*ln(y))**-1, (0, 1)
log = decorators.shift_args({2:(0, 1), 1:((10,), 0)})(log)


@mathfunction
def log2(x, /):
    '''Return the log base 2 of x'''
    if x == 0:
        raise ValueError('math domain error')
    try: return math.log2(x)
    except Exception: pass
    try: return log(2, x)
    except Exception: pass
    raise TypeError('Logarithm base 2 cannot be found of a type %s.' % type(x))
log2.prime[0] = 1/ln(2)*(x**-1), (0,)


@mathfunction
def log1p(x, /):
    '''Return the natural logarithm of x+1'''
    try: return math.log1p(x)
    except Exception: pass
    try: return ln(x+1)
    except Exception: pass
    raise TypeError('log1p cannot be found of a type %s.' % type(x))
log1p.prime[0] = 1/(x+1), (0,)

@mathfunction
def acos(x):
    '''Return the arc cosine of x,
recources to x.acos if cos cannot be found'''
    if validation.is_float(x) and (x<=1 and x>=-1):
        return math.acos(x)
    elif validation.is_complex(x):
        return cmath.acos(x)
    else:
        try: return x.acos()
        except Exception: pass
    raise TypeError('acos cannot be found of a type %s' % (type(x)))

@mathfunction
def acosh(x):
    '''Return the inverse hyperbolic cosine of x
recources to x.acosh if cosh cannot be found'''
    if validation.is_float(x):
        return math.acosh(x)
    elif validation.is_complex(x):
        return cmath.acosh(x)
    else:
        try: return x.acosh()
        except Exception: pass
    raise TypeError('acos cannot be found of a type %s' % (type(x)))

@mathfunction
def asin(x):
    '''Return the arc sine of x,
recources to x.asin if sin cannot be found'''
    if validation.is_float(x)  and (x<=1 and x>=-1):
        return math.asin(x)
    elif validation.is_complex(x):
        return cmath.asin(x)
    else:
        try: return x.asin()
        except Exception: pass
    raise TypeError('asin cannot be found of a type %s' % (type(x)))

@mathfunction
def asinh(x):
    '''Return the inverse hyperbolic sine of x
recources to x.asinh if sinh cannot be found'''
    if validation.is_float(x):
        return math.asinh(x)
    elif validation.is_complex(x):
        return cmath.asinh(x)
    else:
        try: return x.asinh()
        except Exception: pass
    raise TypeError('asin cannot be found of a type %s' % (type(x)))

@mathfunction
def atan(x):
    '''Return the arc tangent of x,
recources to x.atan if tan cannot be found'''
    if validation.is_float(x):
        return math.atan(x)
    elif validation.is_complex(x):
        return cmath.atan(x)
    else:
        try: return x.atan()
        except Exception: pass
    raise TypeError('atan cannot be found of a type %s' % (type(x)))

@mathfunction
def atan2(y, x):
    '''Return the arc tangent (measured in radians) of y/x'''
    return math.atan2(validation.trynumber(y), validation.trynumber(x))
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
        try: return x.atanh()
        except Exception: pass
    raise TypeError('atan cannot be found of a type %s' % (type(x)))

@mathfunction
def asec(x):
    '''Return the arc secant of x
recources to x.asec if sec cannot be found'''
    zde = False
    if validation.is_float(x):
        try: return (1/math.acos(x))
        except ZeroDivisionError: zde = True
    elif validation.is_complex(x):
        try: return (1/cmath.acos(x))
        except ZeroDivisionError: zde = True
    else:
        try:
            try: return x.asec()
            except ZeroDivisionError: zde = True
        except Exception: pass
    if zde:
        raise ValueError ('math domain error')
    raise TypeError('asec cannot be found of a type %s' % (type(x)))

@mathfunction
def asech(x):
    '''Return the inverse hyperbolic secant of x
recources to x.asech if sech cannot be found'''
    zde = False
    if validation.is_float(x):
        try: return (1/math.acosh(x))
        except ZeroDivisionError: zde = True
    elif validation.is_complex(x):
        try: return (1/cmath.acosh(x))
        except ZeroDivisionError: zde = True
    else:
        try:
            try: return x.asech()
            except ZeroDivisionError: zde = True
        except Exception: pass
    if zde:
        raise ValueError ('math domain error')
    raise TypeError('asech cannot be found of a type %s' % (type(x)))

@mathfunction
def acsc(x):
    '''Return the arc cosecant of x
recources to x.acsc if csc cannot be found'''
    zde = False
    if validation.is_float(x):
        try: return (1/math.asin(x))
        except ZeroDivisionError: zde = True
    elif validation.is_complex(x):
        try: return (1/cmath.asin(x))
        except ZeroDivisionError: zde = True
    else:
        try:
            try: return x.acsc()
            except ZeroDivisionError: zde = True
        except Exception: pass
    if zde:
        raise ValueError ('math domain error')
    raise TypeError('acsc cannot be found of a type %s' % (type(x)))

@mathfunction
def acsch(x, /):
    '''Return the inverse hyperbolic cosecant of x
recources to x.acsch if csch cannot be found'''
    zde = False
    if validation.is_float(x):
        try: return (1/math.asinh(x))
        except ZeroDivisionError: zde = True
    elif validation.is_complex(x):
        try: return (1/cmath.asinh(x))
        except ZeroDivisionError: zde = True
    else:
        try:
            try: return x.acsch()
            except ZeroDivisionError: zde = True
        except Exception: pass
    if zde:
        raise ValueError ('math domain error')
    raise TypeError('acsch cannot be found of a type %s' % (type(x)))

@mathfunction
def acot(x, /):
    '''Return the arc cotangent of x
recources to x.acot if cot cannot be found'''
    zde = False
    if validation.is_float(x):
        try: return (1/math.atan(x))
        except ZeroDivisionError: zde = True
    elif validation.is_complex(x):
        try: return (1/cmath.atan(x))
        except ZeroDivisionError: zde = True
    else:
        try:
            try: return x.acot()
            except ZeroDivisionError: zde = True
        except Exception: pass
    if zde:
        raise ValueError ('math domain error')
    raise TypeError('acot cannot be found of a type %s' % (type(x)))

@mathfunction
def acoth(x, /):
    '''Return the inverse hyperbolic cotangent of x
recources to x.acoth if coth cannot be found'''
    zde = False
    if validation.is_float(x):
        try: return (1/math.atanh(x))
        except ZeroDivisionError: zde = True
    elif validation.is_complex(x):
        try: return (1/cmath.atanh(x))
        except ZeroDivisionError: zde = True
    else:
        try:
            try: return x.acoth()
            except ZeroDivisionError: zde = True
        except Exception: pass
    if zde:
        raise ValueError ('math domain error')
    raise TypeError('acoth cannot be found of a type %s' % (type(x)))

@mathfunction
def cos(θ):
    '''Return the cosine of θ,
recources to θ.cos if cos cannot be found'''
    if validation.is_float(θ):
        return math.cos(θ)
    elif validation.is_complex(θ):
        return cmath.cos(θ)
    else:
        try: return θ.cos()
        except Exception: pass
    raise TypeError('cos cannot be found of a type %s' % (type(θ)))

@mathfunction
def cosh(θ):
    '''Return the hyperbolic cosine of θ,
recources to θ.cosh if cosh cannot be found'''
    if validation.is_float(θ):
        return math.cosh(θ)
    elif validation.is_complex(θ):
        return cmath.cosh(θ)
    else:
        try: return θ.cosh()
        except Exception: pass
    raise TypeError('cosh cannot be found of a type %s' % (type(θ)))

@mathfunction
def sin(θ):
    '''Return the sine of θ,
recources to θ.sin if sin cannot be found'''
    if validation.is_float(θ):
        return math.sin(θ)
    elif validation.is_complex(θ):
        return cmath.sin(θ)
    else:
        try: return θ.sin()
        except Exception: pass
    raise TypeError('sin cannot be found of a type %s' % (type(θ)))

@mathfunction
def sinh(θ):
    '''Return the hyperbolic sine of θ,
recources to θ.sinh if sinh cannot be found'''
    if validation.is_float(θ):
        return math.sinh(θ)
    elif validation.is_complex(θ):
        return cmath.sinh(θ)
    else:
        try: return θ.sinh()
        except Exception: pass
    raise TypeError('sinh cannot be found of a type %s' % (type(θ)))

@mathfunction
def tan(θ):
    '''Return the tangent of θ,
recources to θ.tan if tan cannot be found'''
    if validation.is_float(θ):
        return math.tan(θ)
    elif validation.is_complex(θ):
        return cmath.tan(θ)
    else:
        try: return θ.tan()
        except Exception: pass
    raise TypeError('tan cannot be found of a type %s' % (type(θ)))

@mathfunction
def tanh(θ):
    '''Return the hyperbolic tangent of θ,
recources to θ.tanh if tanh cannot be found'''
    if validation.is_float(θ):
        return math.tanh(θ)
    elif validation.is_complex(θ):
        return cmath.tanh(θ)
    else:
        try: return θ.tanh()
        except Exception: pass
    raise TypeError('tanh cannot be found of a type %s' % (type(θ)))

@mathfunction
def sec(θ):
    '''Return the secant of θ,
recources to θ.sec if sec cannot be found'''
    if validation.is_float(θ):
        try: return math.cos(1/θ)
        except ZeroDivisionError: pass
        raise ValueError ('math domain error')
    elif validation.is_complex(θ):
        try: return cmath.cos(1/θ)
        except ZeroDivisionError: pass
        
    else:
        zde = False
        try:
            try: return θ.sec()
            except ZeroDivisionError: zde = True
        except Exception: pass
        if zde: raise ValueError ('math domain error')
    raise TypeError('sec cannot be found of a type %s' % (type(θ)))

@mathfunction
def sech(θ):
    '''Return the hyperbolic secant of θ
recources to θ.sech if sech cannot be found'''
    if validation.is_float(θ):
        try: return math.cosh(1/θ)
        except ZeroDivisionError: pass
        raise ValueError ('math domain error')
    elif validation.is_complex(θ):
        try: return cmath.cosh(1/θ)
        except ZeroDivisionError: pass
        
    else:
        zde = False
        try:
            try: return θ.sech()
            except ZeroDivisionError: zde = True
        except Exception: pass
        if zde: raise ValueError ('math domain error')
    raise TypeError('sech cannot be found of a type %s' % (type(θ)))

@mathfunction
def csc(θ):
    '''Return the cosecant of θ,
recources to θ.csc if csc cannot be found'''
    if validation.is_float(θ):
        try: return math.sin(1/θ)
        except ZeroDivisionError: pass
        raise ValueError ('math domain error')
    elif validation.is_complex(θ):
        try: return cmath.sin(1/θ)
        except ZeroDivisionError: pass
    else:
        zde = False
        try:
            try: return θ.csc()
            except ZeroDivisionError: zde = True
        except Exception: pass
        if zde: raise ValueError ('math domain error')
    raise TypeError('csc cannot be found of a type %s' % (type(θ)))

@mathfunction
def csch(θ):
    '''Return the hyperbolic cosecant of θ
recources to θ.csch if csch cannot be found'''
    if validation.is_float(θ):
        try: return math.sinh(1/θ)
        except ZeroDivisionError: pass
        raise ValueError ('math domain error')
    elif validation.is_complex(θ):
        try: return cmath.sinh(1/θ)
        except ZeroDivisionError: pass
        
    else:
        zde = False
        try:
            try: return θ.csch()
            except ZeroDivisionError: zde = True
        except Exception: pass
        if zde: raise ValueError ('math domain error')
    raise TypeError('csch cannot be found of a type %s' % (type(θ)))

@mathfunction
def cot(θ):
    '''Return the cotangent of θ,
recources to θ.cot if cot cannot be found'''
    if validation.is_float(θ):
        try: return math.tan(1/θ)
        except ZeroDivisionError: pass
        raise ValueError ('math domain error')
    elif validation.is_complex(θ):
        try: return cmath.tan(1/θ)
        except ZeroDivisionError: pass
        
    else:
        zde = False
        try:
            try: return θ.cot()
            except ZeroDivisionError: zde = True
        except Exception: pass
        if zde: raise ValueError ('math domain error')
    raise TypeError('cot cannot be found of a type %s' % (type(θ)))

@mathfunction
def coth(θ):
    '''Return the hyperbolic cotangent of θ
recources to θ.coth if coth cannot be found'''
    
    if validation.is_float(θ):
        try: return math.tanh(1/θ)
        except ZeroDivisionError: pass
        raise ValueError ('math domain error')
    elif validation.is_complex(θ):
        try: return cmath.tanh(1/θ)
        except ZeroDivisionError: pass
        
    else:
        zde = False
        try:
            try: return θ.coth()
            except ZeroDivisionError: zde = True
        except Exception: pass
        if zde: raise ValueError ('math domain error')
    raise TypeError('coth cannot be found of a type %s' % (type(θ)))

acos.prime[0] = -(1-x**2)**-(1/2), (0,)
asin.prime[0] = (1-x**2)**-(1/2), (0,)
atan.prime[0] = 1/(1+x**2), (0,)
asec.prime[0] = (x**4-x**2)**(-1/2), (0,)
acot.prime[0] = -1/(1+x**2), (0,)
acsc.prime[0] = -(x**4-x**2)**(-1/2), (0,)

cos.prime[0] = -sin(x), (0,)
sin.prime[0] = cos, (0,)
cos.prime_cycle[0] = 4
sin.prime_cycle[0] = 4
tan.prime[0] = sec(x)**2, (0,)
sec.prime[0] = sec(x)*tan(x), (0,)
cot.prime[0] = -(csc(x)**2), (0,)
csc.prime[0] = -csc(x)*cot(x), (0,)

acosh.prime[0] = (x**2-1)**(-1/2), (0,)
asinh.prime[0] = (x**2+1)**(-1/2), (0,), (0,)
atanh.prime[0] = 1/(1-x**2), (0,)
asech.prime[0] = -1/(x*(1-x**2)**(1/2)), (0,)
acoth.prime[0] = 1/(1-x**2), (0,)
acsch.prime[0] = -(x**4+x**2)**(-1/2), (0,)

cosh.prime[0] = sinh, (0,)
sinh.prime[0] = cosh, (0,)
cosh.prime_cycle[0] = 2
sinh.prime_cycle[0] = 2
tanh.prime[0] = sech(x)**2, (0,)
sech.prime[0] = -sech(x)*tanh(x), (0,)
coth.prime[0] = -(csch(x)**2), (0,)
csch.prime[0] = -csch(x)*coth(x), (0,)

@mathfunction
def cis(θ, n=1j):
    '''Return cos(θ) + nsin(θ)'''
    if abs(abs(n)-1) > 1e-10:
        raise ValueError ('math domain error')
    if n.real != 0:
        raise ValueError ('math domain error')
    return cos(θ)+(n*sin(θ))
cis.prime[0] = -sin(x)+y*cos(x), (0, 1)
cis.prime[1] = sin(x), (0,)

variable = cas_variable

def polynomial(*terms):
    runfunc = 0
    for power, coefficient in enumerate(terms):
        runfunc += coefficient*x**power
    return runfunc

#eof
