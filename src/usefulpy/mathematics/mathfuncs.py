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
  Version 0.1.0
   Improved useability, ability to calculate derivatives.
   Recursiveness battled
   more versatility
   trig func and inverse trig func decorators
   functions moved here

'''

### DUNDERS ###
__author__ = 'Augustin Garcia'
__version__='0.1.0'


### IMPORTS ###
from .constants import *
from .. import validation as _validation
from .. import decorators as _decorators
from functools import cache, wraps as _wraps
from .expression_check import *


import cmath as _cmath
import math as _math

from . import expression_check as _expression_check


_simplify = _expression_check._simplify
_flatten= _expression_check._flatten

def convert(value, frm, to):
    '''Convert value from 'frm' units to 'to' units.'''
    if frm == to: return value
    assert conversions[frm]['type'] == conversions[to]['type']
    valuefrm, valueto = eval(conversions[frm]['value']), eval(conversions[to]['value'])
    return (value/valuefrm)*valueto

def _mathfunc_oper(function):
    name = function.__name__
    @_wraps(function)
    def _call(self, *args, **kwargs):
        if name in self.__data__['oper']:
            return self.__data__['oper'][name](self, *args, **kwargs)
        return function(self, *args, **kwargs)
    return _call

@cache
def _simplified_tup_to_mfunc(comp):
    if not isinstance(comp, (int, float)):
        callables = {n.__name__:n for n in set(_flatten(comp)) if callable(n)}
        function = mathfunc(eval('lambda x : '+view_string(comp), callables))
        strcomp = function_string(comp)
    else:
        function = mathfunc(eval('lambda x: '+str(comp)))
        strcomp = str(comp)
    function.composition = comp
    function.function = strcomp
    function.__name__ = '<mathfunc>'
    return function

def _tup_to_mfunc(comp):
    comp = _simplify(comp)
    if callable(comp):
        return mathfunc(comp)
    return _simplified_tup_to_mfunc(comp)

class mathfunc:
    '''This class works as a wrapper for functions to support function
differentiation'''
    
    ### ANNOTATIONS ###
    __data__:dict
    __doc__:str
    func:callable
    composition:tuple
    function:str
    __name__:str
    inverse:callable
    interval = None
    __is_frozen:bool = False

    @cache
    def __new__(cls, func:callable):
        '''__new__ for mathfunc class, wraps function 'func'.'''
        assert callable(func)
        if type(func) == mathfunc: return mathfunc
        self = super(mathfunc, cls).__new__(cls)
        self.func = func
        self.__doc__ = func.__doc__
        self.function = func.__name__ + '(<x>)'
        self.__name__ = func.__name__
        self.composition = func
        self.__data__ = {'prime':{'available':[]}, 'oper':{}, 'custom_data':{}}
        return self

    def __setattr__(self, name:str, value)->None:
        '''Intercepts attribute setting, for customized storage'''
        
        if self.__is_frozen:
            raise AttributeError(f'attributes of {self!r} are no longer writeable')
        if name in self.__annotations__:
            super.__setattr__(self, name, value)
            if name == 'function':
                try: self.func.function = value
                except: pass
            return
        if name == 'prime_cycle':
            self.__data__['prime']['cycle'] = value
            return
        if name.startswith('prime'):
            prime_name = name[5:]
            try:
                prime = int(prime_name)
                self.__data__['prime'][prime] = value
                self.__data__['prime']['available'].append(prime)
                return
            except: pass
        if name.endswith('override'):
            method = name[:-8]
            if method in dir(self):
                if callable(value) or value == None:
                    self.__data__['oper'][method] = value
                    return
                raise TypeError(f'{name} attribute must be callable')
                
        self.__data__['custom_data'][name]=value


    def __getattr__(self, name):
        '''Customized attribute storage also necesitates custom attribute lookup'''
        if name == 'prime_cycle':
            try: return self.__data__['prime']['cycle']
            except: pass
        elif name.startswith('prime'):
            try: return self.__data__['prime'][int(name[5:])]
            except: pass
        elif name.endswith('overide') and name[:-8] in dir(self):
            try: return self.__data__['oper'][name]
            except: pass
        try: return self.__data__['custom_data'][name]
        except: pass
        raise AttributeError(f'\'{self.__class__.__name__}\' object has no attribute \'{name}\'')

    
    def __hash__(self):
        '''hash for mathfunc'''
        return hash(self.func)

    def __repr__(self):
        '''repr for mathfunc'''
        return f'<mathfunc {self} at {hex(id(self))}>'

    def __str__(self):
        '''return string representing the funtion'''
        return self.function.replace('<x>', 'x')

    ### CALLING ###
    
    def __call__(self, x):
        '''calls function, if you call it with another function, nests function'''
        if callable(x): return self.__nest__(x)
        if self.interval != None:
            if x not in self.interval:
                raise ValueError('math domain error')
        return self.func(x)

    ### ARITHMETIC ###
    @_mathfunc_oper
    def __pos__(self):
        return self

    @_mathfunc_oper
    def __neg__(self):
        return _tup_to_mfunc(('mul', (-1, self.composition)))

    @cache
    @_mathfunc_oper
    def __add__(self, other):
        if callable(other) or isinstance(other, (int, float)):
            f, g = self, other
            if callable(other):
                if not isinstance(other, mathfunc):
                    g = mathfunc(g)
                return _tup_to_mfunc(('add', (f.composition, g.composition)))
            return _tup_to_mfunc(('add', (f.composition, g)))
        return NotImplemented

    @_mathfunc_oper
    def __radd__(self, other):
        '''return other+self'''
        if callable(other):
            return mathfunc(other)+self
        return self+other

    @_mathfunc_oper
    def __sub__(self, other):
        return self + -other

    @_mathfunc_oper
    def __rsub__(self, other):
        return other + -self

    @_mathfunc_oper
    def __mul__(self, other):
        if callable(other) or isinstance(other, (int, float)):
            f, g = self, other
            if callable(other):
                if not isinstance(other, mathfunc):
                    g = mathfunc(g)
                return _tup_to_mfunc(('mul', (f.composition, g.composition)))
            return _tup_to_mfunc(('mul', (f.composition, g)))
        return NotImplemented

    @_mathfunc_oper
    def __rmul__(self, other):
        '''return other*self'''
        if callable(other):
            return mathfunc(other)*self
        return self*other

    @_mathfunc_oper
    def reciprocal(self):
        return _tup_to_mfunc(('pow', (self.composition,-1)))

    @_mathfunc_oper
    def __truediv__(self, other):
        if callable(other):
            if not isinstance(other, mathfunc):
                other = mathfunc(other)
            return self * other.reciprocal()
        if isinstance(other, (int, float)):
            return self * 1/other
        return NotImplemented

    @_mathfunc_oper
    def __rtruediv__(self, other):
        return other*self.reciprocal()

    @_mathfunc_oper
    def __pow__(self, other):
        if callable(other) or isinstance(other, (int, float)):
            f, g = self, other
            if callable(other):
                if not isinstance(other, mathfunc):
                    g = mathfunc(g)
                return _tup_to_mfunc(('pow', (f.composition, g.composition)))
            return _tup_to_mfunc(('pow', (f.composition, g)))
        return NotImplemented

    @_mathfunc_oper
    def __rpow__(self, other):
        if callable(other):
            return mathfunc(other)**self
        if isinstance(other, (int, float)):
            return _tup_to_mfunc(('pow', (other, self.composition)))
        return NotImplemented

    @_mathfunc_oper
    def __nest__(self, other):
        if other is x:
            return self
        if type(other) != mathfunc:
            other = mathfunc(other)
        return _tup_to_mfunc(('nest', (self.composition, other.composition)))

    @_mathfunc_oper
    def derivative(self, k=1):
        if type(k) is not int:
            raise TypeError(f'only ints allowed, not {type(k).__name__}')
        if not (k >= 0):
            return NotImplemented
        
        if 'cycle' in self.__data__['prime']:
            k = k%self.prime_cycle
        if k == 0:return self
        available = sorted(self.__data__['prime']['available'], reverse = True)
        for nk in available:
            if nk == k:
                return self.__data__['prime'][nk]
            if nk < k:
                return (self.__data__['prime'][nk]).derivative(k-nk)
        if isinstance(self.composition, (tuple, int, float)):
            return _tup_to_mfunc(_comp_derive(self.composition, k))
        return NotImplemented

def _comp_derive(c, k=1):
    if k == 0: return c
    if callable(c):
        return mathfunc(c).derivative(k).composition
    if type(c) in (int, float):
        return 0
    if type(c) is not tuple:
        raise TypeError('Error')
    if c[0] == 'add':
        return _simplify(('add', tuple([_comp_derive(n, k) for n in c[1]])))
    if c[0] == 'nest':
        return _comp_derive(_simplify(('mul', ('nest', (_comp_derive(c[1][0]), c[1][1])), _comp_derive(c[1][1]))), k-1)
    if c[0] == 'mul':
        if len(c[1]) > 2:
            l = len(c[1])
            f = ('mul', (c[1][:l//2]))
            g = ('mul', (c[1][1//2:]))
        else:
            f= c[1][0]
            g = c[1][1]
        return _comp_derive(_simplify(('add', (('mul', (_comp_derive(f), g)), ('mul', (_comp_derive(g), f))))), k-1)
    if c[0] == 'pow':
        if isinstance(c[1][0], (int, float)):
            return _comp_derive(_simplify(('mul', (c, ln(c[1][0]), _comp_derive(c[1][0])))), k-1)
        if isinstance(c[1][1], (int, float)):
            return _comp_derive(_simplify(('mul', (c[1][1], ('pow', (c[1][0], c[1][1]-1)), (_comp_derive(c[1][0]))))), k-1)
        return _comp_derive(('mul', (c, ('add', (('mul', (ln(c[1][0]), _comp_derive(c[1][1]))),('mul', (_comp_derive(c[1][0]), ('pow', (c[1][0], -1)), c[1][1])))))), k-1)

@mathfunc
def trivial(x): return 0

trivial.composition = 0
trivial.function = '0'
trivial.prime1 = trivial
trivial.prime_cycle = 1

@mathfunc
def identity(x):return x

identity.function = '<x>'
identity.prime1 = trivial+1
identity.prime2 = trivial

x=identity

@mathfunc
def floor(x, /):
    '''Return the floor of x'''
    try: return _math.floor(x)
    except: pass
    try: return _math.floor(x.real) + _math.floor(x.imag)*1j if type(x) is complex else x.__floor__()
    except: pass
    raise TypeError(f'invalid type, type {type(x).__name__}')

@mathfunc
def ceil(x, /):
    '''Return the ceil of x'''
    try: return _math.ceil(x)
    except: pass
    try: return ceil(x.real) + ceil(x.imag)*1j if type(x) is complex else x.__ceil__()
    except: pass
    raise TypeError(f'invalid type, type {type(x).__name__}')

@mathfunc
def sigmoid(x, /):
    '''Sigmoid function'''
    epow = exp(-x)
    return 1/(1+epow)

@mathfunc
def exp(x, /):
    '''Return e to the power of x'''
    try: return _math.exp(x)
    except: pass
    try: return _cmath.exp(x)
    except: pass
    try: return x.__exp__()
    except: return e**x
    # this final section may cause a recursive loop if 
    # the method __pow__ or __rpow__ calls exp, but if it doesn't then this
    # handles it.

exp.prime1=exp
exp.prime_cycle=1

@mathfunc
def expm1(x, /):
    '''Return exp(x)-1'''
    try: return _math.expm1(x)
    except: return exp(x)-1

expm1.prime1 = exp
expm1.composition = ('add', (exp, -1))


@mathfunc
def sqrt(x, /):
    '''Return the square root of x'''
    try: return _math.sqrt(x)
    except: pass
    try: return _cmath.sqrt(x)
    except: pass
    try: return x**(1/2)
    except: pass
    raise ValueError('math domain error')

@mathfunc
def isqrt(x, /):
    '''Return the floored square root of x'''
    try: return _math.isqrt(x)
    except: return floor(sqrt(x))

@mathfunc
def cbrt(x, /):
    '''Return the cube root of x'''
    try: return x**(1/3)
    except: pass
    raise ValueError('math domain error')

@mathfunc
def icbrt(x, /):
    '''Return the floored cube root of x'''
    try: return int(x**(1/3))
    except: pass
    raise ValueError('math domain error')

@mathfunc
def square(x, /):
    '''Return x**2'''
    return x*x

@mathfunc
def cube(x, /):
    '''Return x**3'''
    return x*x*x

@mathfunc
def tesser(x, /):
    '''Return x**4'''
    return x*x*x*x

@mathfunc
def ln(x, /):
    '''Return the natural logarithm of x
    recources to x.__ln__() or x.__log__(e) if log cannot be found'''
    if x == 0:
        raise ValueError('math domain error')
    try: return _math.log(x)
    except: pass
    try: return _cmath.log(x)
    except: pass    
    try: return x.ln()
    except: pass
    try: return x.__log__(e)
    except: pass
    raise TypeError('Natural logarithm cannot be found of a type %s.' % type(x))
ln.prime1 = 1/x


@_decorators.shift_args({2:(0, 1), 1:((10,), 0)})
def log(base, x):
    ''' log([base=10], x)
    Return the log base 'base' of x
    recources to x.__log__(base) if log cannot be found'''
    if x == base: return 1
    if 0 in (x, base):
        raise ValueError('math domain error')
    if base == 1:
        raise ValueError('math domain error')
    try: return _math.log(x, base)
    except: pass
    try: return _cmath.log(x, base)
    except: pass
    try: return x.__log__(base)
    except: pass
    raise TypeError('Logarithm cannot be found of a type %s.' % type(x))

@_decorators.default_with_decorator(mathfunc)
def log_base(a, b):
    '''Log base \\FIRSTARG of x'''
    return log(a, b)

@mathfunc
def log2(x, /):
    '''Return the log base 2 of x'''
    if x == 0:
        raise ValueError('math domain error')
    try: return _math.log2(x)
    except: pass
    try: return log(2, x)
    except: pass
    raise TypeError('Logarithm base 2 cannot be found of a type %s.' % type(x))

@mathfunc
def log1p(x, /):
    '''Return the natural logarithm of x+1'''
    try: return _math.log1p(x)
    except:pass
    try: return ln(x+1)
    except: pass
    raise TypeError('log1p cannot be found of a type %s.' % type(x))

_circles = {
    'rad': tau,
    'deg': 360,
    'grad':400
    }
_angle = 'rad'
_circle = tau

def _changeto(to):
    global _angle, _circle
    _angle, _circle = to, _circles[to]

def radians():
    '''Change setting to radians'''
    _changeto('rad')

def degrees():
    '''Change setting to degrees'''
    _changeto('deg')

def grad():
    '''Change setting to grad'''
    _changeto('grad')

def get_angle():
    return _angle

def trig_func(function):
    @mathfunc
    @_wraps(function)
    def _trig_wrap(θ):
        θ = convert(θ, _angle, 'rad')
        return function(θ)
    return _trig_wrap

def inverse_trig_func(function):
    @mathfunc
    @_wraps(function)
    def _inverse_trig_wrap(x):
        θ = function(x)
        return convert(θ, 'rad', _angle)

@inverse_trig_func
def acos(x):
    '''Return the arc cosine of x,
recources to x.__acos__ if cos cannot be found'''
    if _validation.is_float(x) and (x<=1 and x>=-1):
        return _math.acos(x)
    elif _validation.is_complex(x):
        return _cmath.acos(x)
    else:
        try: return x.__acos__()
        except: pass
    raise TypeError('acos cannot be found of a type %s' % (type(x)))

@inverse_trig_func
def acosh(x):
    '''Return the inverse hyperbolic cosine of x
recources to x.__acos__ if cosh cannot be found'''
    if _validation.is_float(x):
        return _math.acosh(x)
    elif _validation.is_complex(x):
        return _cmath.acosh(x)
    else:
        try: return x.__acosh__()
        except: pass
    raise TypeError('acos cannot be found of a type %s' % (type(x)))

@inverse_trig_func
def asin(x):
    '''Return the arc sine of x,
recources to x.__asin__ if sin cannot be found'''
    if _validation.is_float(x)  and (x<=1 and x>=-1):
        return _math.asin(x)
    elif _validation.is_complex(x):
        return _cmath.asin(x)
    else:
        try: return x.__asin__()
        except: pass
    raise TypeError('asin cannot be found of a type %s' % (type(x)))

@inverse_trig_func
def asinh(x):
    '''Return the inverse hyperbolic sine of x
recources to x.__asin__ if sinh cannot be found'''
    if _validation.is_float(x):
        return _math.asinh(x)
    elif _validation.is_complex(x):
        return _cmath.asinh(x)
    else:
        try: return x.__asinh__()
        except: pass
    raise TypeError('asin cannot be found of a type %s' % (type(x)))

@inverse_trig_func
def atan(x):
    '''Return the arc tangent of x,
recources to x.__atan__ if tan cannot be found'''
    if _validation.is_float(x):
        return _math.atan(x)
    elif _validation.is_complex(x):
        return _cmath.atan(x)
    else:
        try: return x.__atan__()
        except: pass
    raise TypeError('atan cannot be found of a type %s' % (type(x)))

def atan2(y, x, setting = None):
    if setting is None: setting = _angle
    θ = _math.atan2(_validation.trynumber(y), _validation.trynumber(x))
    return _validation.trynumber(convert(θ, 'rad', setting))

@inverse_trig_func
def atanh(x):
    '''Return the inverse hyperbolic tangent of x
recources to x.__atan__ if tanh cannot be found'''
    if _validation.is_float(x):
        return _math.atanh(x)
    elif _validation.is_complex(x):
        return _cmath.atanh(x)
    else:
        try: return x.__atanh__()
        except: pass
    raise TypeError('atan cannot be found of a type %s' % (type(x)))

@inverse_trig_func
def asec(x):
    '''Return the arc secant of x
recources to x.__asec__ if sec cannot be found'''
    zde = False
    if _validation.is_float(x):
        try: return (1/_math.acos(x))
        except ZeroDivisionError: zde = True
    elif _validation.is_complex(x):
        try: return (1/_cmath.acos(x))
        except ZeroDivisionError: zde = True
    else:
        try:
            try: return x.__asec__()
            except ZeroDivisionError: zde = True
        except:pass
    if zde:
        raise ValueError ('math domain error')
    raise TypeError('asec cannot be found of a type %s' % (type(x)))

@inverse_trig_func
def asech(x):
    '''Return the inverse hyperbolic secant of x
recources to x.__asech__ if sech cannot be found'''
    zde = False
    if _validation.is_float(x):
        try: return (1/_math.acosh(x))
        except ZeroDivisionError: zde = True
    elif _validation.is_complex(x):
        try: return (1/_cmath.acosh(x))
        except ZeroDivisionError: zde = True
    else:
        try:
            try: return x.__asech__()
            except ZeroDivisionError: zde = True
        except:pass
    if zde:
        raise ValueError ('math domain error')
    raise TypeError('asech cannot be found of a type %s' % (type(x)))

@inverse_trig_func
def acsc(x):
    '''Return the arc cosecant of x
recources to x.__acsc__ if csc cannot be found'''
    zde = False
    if _validation.is_float(x):
        try: return (1/_math.asin(x))
        except ZeroDivisionError: zde = True
    elif _validation.is_complex(x):
        try: return (1/_cmath.asin(x))
        except ZeroDivisionError: zde = True
    else:
        try:
            try: return x.__acsc__()
            except ZeroDivisionError: zde = True
        except:pass
    if zde:
        raise ValueError ('math domain error')
    raise TypeError('acsc cannot be found of a type %s' % (type(x)))

@inverse_trig_func
def acsch(x, /):
    '''Return the inverse hyperbolic cosecant of x
recources to x.__acsch__ if csch cannot be found'''
    zde = False
    if _validation.is_float(x):
        try: return (1/_math.asinh(x))
        except ZeroDivisionError: zde = True
    elif _validation.is_complex(x):
        try: return (1/_cmath.asinh(x))
        except ZeroDivisionError: zde = True
    else:
        try:
            try: return x.__acsch__()
            except ZeroDivisionError: zde = True
        except:pass
    if zde:
        raise ValueError ('math domain error')
    raise TypeError('acsch cannot be found of a type %s' % (type(x)))

@inverse_trig_func
def acot(x, /, setting = None):
    '''Return the arc cotangent of x
recources to x.__acot__ if cot cannot be found'''
    zde = False
    if _validation.is_float(x):
        try: return (1/_math.atan(x))
        except ZeroDivisionError: zde = True
    elif _validation.is_complex(x):
        try: return (1/_cmath.atan(x))
        except ZeroDivisionError: zde = True
    else:
        try:
            try: return x.__acot__()
            except ZeroDivisionError: zde = True
        except: pass
    if zde:
        raise ValueError ('math domain error')
    raise TypeError('acot cannot be found of a type %s' % (type(x)))

@inverse_trig_func
def acoth(x, /):
    '''Return the inverse hyperbolic cotangent of x
recources to x.__acoth__ if coth cannot be found'''
    zde = False
    if _validation.is_float(x):
        try: return (1/_math.atanh(x))
        except ZeroDivisionError: zde = True
    elif _validation.is_complex(x):
        try: return (1/_cmath.atanh(x))
        except ZeroDivisionError: zde = True
    else:
        try:
            try: return x.__acoth__()
            except ZeroDivisionError: zde = True
        except:pass
    if zde:
        raise ValueError ('math domain error')
    raise TypeError('acoth cannot be found of a type %s' % (type(x)))

@trig_func
def cos(θ):
    '''Return the cosine of θ,
recources to θ.__cos__ if cos cannot be found'''
    if _validation.is_float(θ):
        return _math.cos(θ)
    elif _validation.is_complex(θ):
        return _cmath.cos(θ)
    else:
        try: return θ.__cos__()
        except: pass
    raise TypeError('cos cannot be found of a type %s' % (type(θ)))

@trig_func
def cosh(θ):
    '''Return the hyperbolic cosine of θ,
recources to θ.__cosh__ if cosh cannot be found'''
    if _validation.is_float(θ):
        return _math.cosh(θ)
    elif _validation.is_complex(θ):
        return _cmath.cosh(θ)
    else:
        try: return θ.__cosh__()
        except: pass
    raise TypeError('cosh cannot be found of a type %s' % (type(θ)))

@trig_func
def sin(θ):
    '''Return the sine of θ,
recources to θ.__sin__ if sin cannot be found'''
    if _validation.is_float(θ):
        return _math.sin(θ)
    elif _validation.is_complex(θ):
        return _cmath.sin(θ)
    else:
        try: return θ.__sin__()
        except: pass
    raise TypeError('sin cannot be found of a type %s' % (type(θ)))

@trig_func
def sinh(θ):
    '''Return the hyperbolic sine of θ,
recources to θ.__sinh__ if sinh cannot be found'''
    if _validation.is_float(θ):
        return _math.sinh(θ)
    elif _validation.is_complex(θ):
        return _cmath.sinh(θ)
    else:
        try: return θ.__sinh__()
        except: pass
    raise TypeError('sinh cannot be found of a type %s' % (type(θ)))

@trig_func
def tan(θ):
    '''Return the tangent of θ,
recources to θ.__tan__ if tan cannot be found'''
    if _validation.is_float(θ):
        return _math.tan(θ)
    elif _validation.is_complex(θ):
        return _cmath.tan(θ)
    else:
        try: return θ.__tan__()
        except: pass
    raise TypeError('tan cannot be found of a type %s' % (type(θ)))

@trig_func
def tanh(θ):
    '''Return the hyperbolic tangent of θ,
recources to θ.__tanh__ if tanh cannot be found'''
    if _validation.is_float(θ):
        return _math.tanh(θ)
    elif _validation.is_complex(θ):
        return _cmath.tanh(θ)
    else:
        try: return θ.__tanh__()
        except: pass
    raise TypeError('tanh cannot be found of a type %s' % (type(θ)))

@trig_func
def sec(θ):
    '''Return the secant of θ,
recources to θ.__sec__ if sec cannot be found'''
    if _validation.is_float(θ):
        try: return _math.cos(1/θ)
        except ZeroDivisionError: pass
        raise ValueError ('math domain error')
    elif _validation.is_complex(θ):
        try: return _cmath.cos(1/θ)
        except ZeroDivisionError: pass
        
    else:
        zde = False
        try:
            try: return θ.__sec__()
            except ZeroDivisionError: zde = True
        except: pass
        if zde: raise ValueError ('math domain error')
    raise TypeError('sec cannot be found of a type %s' % (type(θ)))

@trig_func
def sech(θ):
    '''Return the hyperbolic secant of θ
recources to θ.__sech__ if sech cannot be found'''
    if _validation.is_float(θ):
        try: return _math.cosh(1/θ)
        except ZeroDivisionError: pass
        raise ValueError ('math domain error')
    elif _validation.is_complex(θ):
        try: return _cmath.cosh(1/θ)
        except ZeroDivisionError: pass
        
    else:
        zde = False
        try:
            try: return θ.__sech__()
            except ZeroDivisionError: zde = True
        except: pass
        if zde: raise ValueError ('math domain error')
    raise TypeError('sech cannot be found of a type %s' % (type(θ)))

@trig_func
def csc(θ):
    '''Return the cosecant of θ,
recources to θ.__csc__ if csc cannot be found'''
    if _validation.is_float(θ):
        try: return _math.sin(1/θ)
        except ZeroDivisionError: pass
        raise ValueError ('math domain error')
    elif _validation.is_complex(θ):
        try: return _cmath.sin(1/θ)
        except ZeroDivisionError: pass
    else:
        zde = False
        try:
            try: return θ.__csc__()
            except ZeroDivisionError: zde = True
        except: pass
        if zde: raise ValueError ('math domain error')
    raise TypeError('csc cannot be found of a type %s' % (type(θ)))

@trig_func
def csch(θ):
    '''Return the hyperbolic cosecant of θ
recources to θ.__csch__ if csch cannot be found'''
    if _validation.is_float(θ):
        try: return _math.sinh(1/θ)
        except ZeroDivisionError: pass
        raise ValueError ('math domain error')
    elif _validation.is_complex(θ):
        try: return _cmath.sinh(1/θ)
        except ZeroDivisionError: pass
        
    else:
        zde = False
        try:
            try: return θ.__csch__()
            except ZeroDivisionError: zde = True
        except: pass
        if zde: raise ValueError ('math domain error')
    raise TypeError('csch cannot be found of a type %s' % (type(θ)))

@trig_func
def cot(θ):
    '''Return the cotangent of θ,
recources to θ.__cot__ if cot cannot be found'''
    if _validation.is_float(θ):
        try: return _math.tan(1/θ)
        except ZeroDivisionError: pass
        raise ValueError ('math domain error')
    elif _validation.is_complex(θ):
        try: return _cmath.tan(1/θ)
        except ZeroDivisionError: pass
        
    else:
        zde = False
        try:
            try: return θ.__cot__()
            except ZeroDivisionError: zde = True
        except: pass
        if zde: raise ValueError ('math domain error')
    raise TypeError('cot cannot be found of a type %s' % (type(θ)))

@trig_func
def coth(θ):
    '''Return the hyperbolic cotangent of θ
recources to θ.__coth__ if coth cannot be found'''
    
    if _validation.is_float(θ):
        try: return _math.tanh(1/θ)
        except ZeroDivisionError: pass
        raise ValueError ('math domain error')
    elif _validation.is_complex(θ):
        try: return _cmath.tanh(1/θ)
        except ZeroDivisionError: pass
        
    else:
        zde = False
        try:
            try: return θ.__coth__()
            except ZeroDivisionError: zde = True
        except: pass
        if zde: raise ValueError ('math domain error')
    raise TypeError('coth cannot be found of a type %s' % (type(θ)))

def cis(θ, n=1j):
    '''Return cos(θ) + nsin(θ)'''
    if abs(abs(n)-1) > 1e-10:
        raise ValueError ('math domain error')
    if n.real != 0:
        raise ValueError ('math domain error')
    return cos(θ)+(n*sin(θ))

@_decorators.default_with_decorator(trig_func)
def cns(n, θ):
    '''Return cos(θ)+\\FIRSTARG sin(θ)'''
    return cis(θ, n)

cos.prime1=-sin
cos.prime2=-cos
cos.prime3=sin
cos.prime4 = cos
cos.prime_cycle = 4

sin.prime1=cos
sin.prime2=-sin
sin.prime3=-cos
sin.prime4 = sin
sin.prime_cycle = 4

(-sin).prime1=-cos
(-sin).prime2=sin
(-sin).prime3=cos
(-sin).primet=-sin
(-sin).prime_cycle = 4

(-cos).prime1=sin
(-cos).prime2=cos
(-cos).prime3=-sin
(-cos).prime4 = -cos
(-cos).prime_cycle = 4


tan.prime1 = ('pow', (sec, 2))
sec.prime1 = ('mul', (sec, tan))
cot.prime1 = 'mul', (('pow', (csc, 2)), -1)
csc.prime1 = 'mul', (('mul', (csc, cot)), -1)

#eof
