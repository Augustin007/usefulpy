'''
new math

This file is essentially the importation of the math module, but a few small
functions are added or changed.

LICENSE PLATAFORMS and INSTALLATION:
This is a section of usefulpy. See usefulpy.__init__ and usefulpy license
file

RELEASE NOTES:
0
 0.0
  Version 0.0.0
   Simple math importations with some changes and additions
  Version 0.0.1
   Changed some variable names and importations. More comments.
1
 1.0
  Version 1.0.0
   Reworked a lot of little details to allow for use with complex numbers
   throughout.
  Version 1.0.1
   Several new functions.
  Version 1.0.2
   Bug fixes
 1.1
  Version 1.1.0
   Some new functions and changing some internal workings
  Version 1.1.1
   Bug fixes (again)
2
 2.0
  Version 2.0.0
     ——Wednesday, the thirteenth day of the firstmonth Janurary, 2021——
   Rewrote on another document, cleaning up, improving, and adding functions
   throughout
  Version 2.0.1
   Small bugfixes
 2.1
  Version 2.1.0
   Mathfunc improvements/ trigfunc stuff, decorators
  Version 2.1.1
   Mathfunc bugfixes
  Version 2.1.2
   More mathfunc and such bugfixes
  Version 2.1.3
   Clean up of code
'''

### DUNDERS ###
__version__='2.1.3'
__author__ = 'Austin Garcia'
__package__='usefulpy.mathematics'

### IMPORTS ###
from .constants import *
from .. import validation as _validation
from .. import decorators as _decorators

from decimal import Decimal as number
from fractions import Fraction as fraction

import operator as _op # Is not being used currently?
import cmath as _cmath
import math as _math
import json as _json
import os as _os
from functools import reduce as _reduce

from math import comb, copysign, erf, erfc, fabs, factorial, fmod, fsum, gamma
from math import lgamma, modf, nextafter, perm, prod, remainder, trunc, ulp

### CONVERSIONS ###
##TODO: Add more values to conversions
conversions = {'rad':
  {'type': 'angle',
   'value': 'tau'
  },
 'deg':
  {'type': 'angle',
   'value': '360'
  },
 'grad':
  {'type': 'angle',
   'value': '400'
  },
 'meter':
  {'type': 'length',
   'value': 1
  },
 'decameter':
  {'type': 'length',
   'value': 1/10
  },
 'hectometer':
  {'type': 'length',
   'value': 1/100
  },
 'kilometer':
  {'type': 'length',
   'value': 1/1000
  },
 'megameter':
  {'type': 'length',
   'value': 1/1000000
  },
 'gigameter':
  {'type': 'length',
   'value': 1/1000000000
  },
 'terrameter':
  {'type': 'length',
   'value': 1/1000000000
  },
 'petameter':
  {'type': 'length',
   'value': 1/1000000000000000
  },
 'exameter':
  {'type': 'length',
   'value': 1/1000000000000000000
  },
 'zettameter':
  {'type': 'length',
   'value': 1/1000000000000000000000
  },
 'yottameter':
  {'type': 'length',
   'value': 1/1000000000000000000000000
  },
 'decimeter':
  {'type': 'length',
   'value': 10
  },
 'centimeter':
  {'type': 'length',
   'value': 100
  },
 'millimeter':
  {'type': 'length',
   'value': 1000
  },
 'micrometer':
  {'type': 'length',
   'value': 1000000
  },
 'nanometer':
  {'type': 'length',
   'value': 1000000000
  },
 'picometer':
  {'type': 'length',
   'value': 1000000000000
  },
 'femtometer':
  {'type': 'length',
   'value': 1000000000000000
  },
 'attometer':
  {'type': 'length',
   'value': 1000000000000000000
  },
 'zeptometer':
  {'type': 'length',
   'value': 1000000000000000000000
  },
 'yoctometer':
  {'type': 'length',
   'value': 1000000000000000000000000
  },
 'foot':
  {'type': 'length',
   'value': 3.2808398949899997
  },
 'inches':
  {'type': 'length',
   'value': 39.37007873988
  },
 'yard':
  {'type': 'length',
   'value': 1.09361329833
  },
 'mile':
  {'type': 'length',
   'value': 0.0006213711922329545
  },
 'nautical_mile':
  {'type': 'length',
   'value': 0.0005399670663248847
  }
}


### checks ###
def odd(num, /):
    '''Return True if num is odd'''
    return num%2 != 0

def even(num, /):
    '''Return True if num is even'''
    return num%2 == 0

def isclose(a, b, *, rel_tol=1e-09, abs_tol=0.0):
    '''Return True if a is close to b'''
    try: return _math.isclose(a, b) # Always try optimized c methods first
    except: pass
    try: return _cmath.isclose(a, b)
    except: pass
    if isnan(a) or isnan(b): return False
    if isinf(a) or isinf(b): return a == b
    tol, difference = max((abs(abs(b)*rel_tol)), abs(abs_tol)), abs(a-b)
    return tol >= difference

def isinf(x, /):
    '''Return True if x is inf in any direction'''
    try: return _math.isinf(x)
    except: pass
    try: return _cmath.isinf(x)
    except: pass
    if x in (inf, infj, neg_inf, neg_infj): return True
    try:
        if x.real in (inf, neg_inf): return True
        else: return x.imag in (inf, neg_inf)
    except: pass
    try:
        if x.real in (inf, neg_inf): return True
        if x.i in (inf, neg_inf): return True
        if x.j in (inf, neg_inf): return True
        return x.k in (inf, neg_inf)
    except: pass
    return x.__isinf__()

def isnan(x, /):
    '''Return True if x is nan in any way'''
    try: return _math.isnan(x)
    except: pass
    try: return _cmath.isnan(x)
    except: pass
    if x in (nan, nanj): return True
    try:
        if x.real == nan: return True
        else: return x.imag == nan
    except:pass
    try:
        if x.i == nan: return True
        if x.j == nan: return True
        return x.k == nan
    except: pass
    return x.__isnan__()

def isfinite(x, /):
    '''Return True if x is finite'''
    try: return _math.isfinite(x)
    except: pass
    try: return _cmath.isfinite(x)
    except: pass
    if _validation.is_numeric(x):
        return not (isnan(x) or isinf(x))
    return False

_old_tuple = tuple
class tuple(_old_tuple):
    '''A tuple modified for math work'''
    def __add__(self, other):
        '''Return self+other'''
        return tuple([n+other for n in self])
    def __radd__(self, other):
        '''Return other+self'''
        return tuple([other+n for n in self])
    def __sub__(self, other):
        '''Return self-other'''
        return tuple([n-other for n in self])
    def __rsub__(self, other):
        '''Return other-self'''
        return tuple([other-n for n in self])
    def __mul__(self, other):
        '''Return self*other'''
        return tuple([n*other for n in self])
    def __rmul__(self, other):
        '''Return other*self'''
        return tuple([other*n for n in self])
    def __truediv__(self, other):
        '''Return self/other'''
        return tuple([n/other for n in self])
    def __rtruediv__(self, other):
        '''Return other/self'''
        return tuple([other/n for n in self])
    def __pow__(self, other):
        '''Return self**other'''
        return tuple([n**other for n in self])
    def __rpow__(self, other):
        '''Return other**self'''
        return tuple([other**n for n in self])
    def __floor__(self):
        '''Return floor(self)'''
        return tuple([floor(n) for n in self])
    def __ceil__(self):
        '''Return ceil(self)'''
        return tuple([ceil(n) for n in self])
    def __cos__(self):
        return tuple([cos(n) for n in self])
    def __sin__(self):
        return tuple([sin(n) for n in self])
    def __tan__(self):
        return tuple([tan(n) for n in self])
    def __sec__(self):
        return tuple([sec(n) for n in self])
    def __csc__(self):
        return tuple([csc(n) for n in self])
    def __cot__(self):
        return tuple([cot(n) for n in self])
    def __cosh__(self):
        return tuple([cosh(n) for n in self])
    def __sinh__(self):
        return tuple([sinh(n) for n in self])
    def __tanh__(self):
        return tuple([tanh(n) for n in self])
    def __sech__(self):
        return tuple([sech(n) for n in self])
    def __csch__(self):
        return tuple([csch(n) for n in self])
    def __coth__(self):
        return tuple([coth(n) for n in self])
    def __acos__(self):
        return tuple([acos(n) for n in self])
    def __asin__(self):
        return tuple([asin(n) for n in self])
    def __atan__(self):
        return tuple([atan(n) for n in self])
    def __asec__(self):
        return tuple([asec(n) for n in self])
    def __acsc__(self):
        return tuple([acsc(n) for n in self])
    def __acot__(self):
        return tuple([acot(n) for n in self])
    def __acosh__(self):
        return tuple([acosh(n) for n in self])
    def __asinh__(self):
        return tuple([asinh(n) for n in self])
    def __atanh__(self):
        return tuple([atanh(n) for n in self])
    def __asech__(self):
        return tuple([asech(n) for n in self])
    def __acsch__(self):
        return tuple([acsch(n) for n in self])
    def __acoth__(self):
        return tuple([acoth(n) for n in self])
    def __ln__(self):
        return tuple([ln(n) for n in self])
    def __abs__(self):
        return tuple([abs(n) for n in self])
    def __exp__(self):
        return tuple([exp(n) for n in self])
    def __phase__(self):
        return tuple([phase(n) for n in self])
    def __polar__(self):
        return tuple([polar(n) for n in self])
    def __log__(self, base):
        return tuple([log(base, n) for n in self])
    def flatten(self):
        '''flatten into 1 dimension'''
        return _validation.flatten(self)

def pm(a, b):
    '''Return a ± b'''
    return tuple((a+b, a-b))

dx = 1e-14 

add = lambda x, y: x+y
#(add, ((),()))
radd = lambda x, y: y+x
#(radd, ((),()))
sub = lambda x, y: x-y
#(sub, ((),()))
rsub = lambda x, y: y-x
#(rsub, ((),()))
mul = lambda x, y: x*y
#(mul, ((),()))
rmul = lambda x, y: y*x
#(rmul, ((),()))
div = lambda x, y: x/y
#(div, ((),()))
rdiv = lambda x, y: y/x
#(rdiv, ((),()))
rpow = lambda x, y: y**x
#(pow, ((),()))
#(rpow, ((),()))
nest = lambda x, y: x(y)
#(nest, ((),()))
neg = lambda x, y: -x

def pascal(depth):
    values = (1,)
    for layer in range(depth-1):
        value_list = [1]
        for num, value in enumerate(values):
            try: value_list.append(value + values[num+1])
            except IndexError: value_list.append(value)
        values = tuple(value_list)
    return tuple(values)

def binomial_coeficient(k, n):
    return factorial(n)/(factorial(n-k)*factorial(k))

def _derivative_mul_tuple(f, g, kth):
    binomial_numbers = pascal(kth+1)
    sum_ = []
    for m, n in enumerate(binomial_numbers):
        if m == 0:
            sum_.append((mul, (n, (mul, (f, g.__dict__[f'prime{kth}'])))))
            continue
        if kth-m == 0:
            sum_.append((mul, (n, (mul, (f.__dict__[f'prime{m}'], g)))))
            continue
        sum_.append((mul, (n, (mul, (f.__dict__[f'prime{m}'], g.__dict__[f'prime{k-m}'])))))
    return _tuple_sum(_old_tuple(sum_))

def _mul_derive_method(f, g):
    def wrapper(kth):
        return _derivative_mul_tuple(f, g, kth)
    return wrapper

def _tuple_sum(long_tuple):
    if len(long_tuple)==2: return ('add', long_tuple)
    long_list = list(long_tuple)
    first = long_list.pop(0)
    return ('add', (first, _tuple_sum(_old_tuple(long_list))))

class mathfunc:
    def __init__(f, func, **extras):
        f.__dict__ = extras
        f.func = func
        f.__doc__ = f.func.__doc__
        f.composition = f.func.__name__ + '(x)'

    def __repr__(f):
        return f'<nmath.mathfunc {f.composition} at {hex(id(f))}>'

    def __call__(f, x):
        if callable(x): return f.__nest__(x)
        return f.func(x)

    def __nest__(f, g):
        if callable(g):
            h = mathfunc(lambda x: f.func(g.func(x)))
            # use .func to avoid extra calls
            h.composition = f.composition.replace('(x)', '('+g.composition+')')
            h.composition_tuple = (nest, (f, g))
            for key, value_pair in mathfunc.merge_items(f, g):
                fv, gv = value_pair
                if key == 'prime1':
                    h.prime1 = (mul, ((nest, (fv, g)), gv))
                    continue
                if key == 'prime2':
                    try: h.prime2 = (add, ((mul, (pow, (g, 2),(nest, (f.prime2, g)))),(mul, (((nest, (f.prime1,g))),g.prime2))))
                    except NameError: pass
                    continue
            return h

    @staticmethod
    def merge_items(f, g): return _validation.merge_dicts(f.__dict__, g.__dict__).items()

    @staticmethod
    def inverses(f, g): f.inverse, g.inverse = g, f

    @_decorators.arg_modifier(_validation.trynumber)
    def __add__(f, g):
        if f'add{g}' in f.__dict__: return f.solve_key(f'add{g}')
        if g in (0, trivial): return f
        if g == -f: return trivial
        if g == f: return 2*f
        if callable(g):
            h = mathfunc(lambda x: f.func(x) + g.func(x))
            h.composition = '('+f.composition+'+'+g.composition+')'
            h.composition_tuple = (add, (f, g))
            for key, value_pair in mathfunc.merge_items(f, g):
                fv, gv = value_pair
                if key == 'prime_cycle':
                    h.prime_cycle = _math.gcd(fv, gv)
                    continue
                if key.startswith('prime'):
                    h.__dict__[key] = (add, (fv, gv))
                    continue
            return h
        elif _validation.is_numeric(g):
            h = mathfunc(lambda x: f.func(x) + g)
            h.composition = '('+f.composition+'+'+str(g)+')'
            h.composition_tuple = (add, (f, g))
            for key, value in f.__dict__.items():
                if key.startswith('prime'):
                    h.__dict__[key] = value
                    continue
            return h
        raise TypeError('Inappropriate argument type.')

    @_decorators.arg_modifier(_validation.trynumber)
    def __neg__(f):
        if 'negative' in f.__dict__: return f.solve_key('negative')
        h = mathfunc(lambda x: -(f(x)), negative=f)
        h.composition = '-'+f.composition
        for key, value in f.__dict__.items():
            if key == 'prime_cycle':
                h.__dict__[key] = value
                continue
            if key.startswith('prime'):
                h.__dict__[key] = (neg, (value, None)) #TODO: improve ability of solve_key for this
                continue
        return h

    def __eq__(f, g): return f is g

    def inv(f):
        return f.inverse

    @_decorators.arg_modifier(_validation.trynumber)
    def __abs__(f):
        return mathfunc(lambda x: abs(f(x)))

    def __pos__(f): return f

    def __radd__(f, g):
        if callable(g):
            return mathfunc(g) + f
        return f + g

    def __sub__(f, g):
        if g == 0: return f
        if g == f: return trivial
        return f + -g

    def __rsub__(f, g):
        if g == 0: return -f
        if g == f: return trivial
        return g+-f

    @_decorators.arg_modifier(_validation.trynumber)
    def __mul__(f, g):
        if f'mul{g}' in f.__dict__: return f.solve_key(f'mul{g}')
        if g == 1: return f
        if g in (0, trivial): return trivial
        if f == -g: return -(f**2)
        if f == g: return f**2
        if callable(g):
            h = mathfunc(lambda x: f.func(x) * g.func(x))
            for key, value_pair in mathfunc.merge_items(f, g):
                fv, gv = value_pair
                if key == 'prime1':
                    h.__dict__[key] = (add, ((mul, (fv, g)) ,(mul, (gv, f))))
                    continue
            h.derive_method = _mul_derive_method(f, g)
            h.composition = '('+f.composition+'*'+g.composition+')'
            return h
        elif _validation.is_numeric(g):
            h = mathfunc(lambda x: f.func(x) * g)
            for key, value in f.__dict__.items():
                if key == 'prime_cycle':
                    h.__dict__[key] = value
                    continue
                if key.startswith('prime'):
                    h.__dict__[key] = (mul, (value, g))
                    continue
            h.composition = '('+f.composition+'*'+str(g)+')'
            return h
        raise TypeError('Inappropriate argument type.')
    
    @_decorators.arg_modifier(_validation.trynumber)
    def __rmul__(f, g):
        if f'rmul{g}' in f.__dict__: return f.solve_key(f'rmul{g}')
        if g == 1: return f
        if g in (0, trivial): return trivial
        if f == -g: return -(f**2)
        if f == g: return f**2
        
        if callable(g):
            return mathfunc(g)*f
        elif _validation.is_numeric(g):
            h = mathfunc(lambda x: g*f.func(x))
            for key, value in f.__dict__.items():
                if key == 'prime_cycle':
                    h.__dict__[key] = value
                    continue
                if key.startswith('prime'):
                    h.__dict__[key] = (mul, (value, g))
                    continue
            h.composition = '('+f.composition+'*'+str(g)+')'
            return h
        raise TypeError('Inappropriate argument type.')

    def __str__(f):
        return 'mathfunc{('+f.composition+')}'

    @_decorators.arg_modifier(_validation.trynumber)
    def __truediv__(f, g):
        if f'div{g}' in f.__dict__: return f.solve_key(f'div{g}')
        if g == 1: return f
        if g in (0, trivial):
            raise ZeroDivisionError ('Division by 0')
        if f == g: return trivial + 1
        if f == -g: return trivial-1
        if callable(g):
            h = mathfunc(lambda x: f.func(x) / g.func(x))
            h.composition = '('+f.composition+'/'+g.composition+')'
            for key, value_pair in mathfunc.merge_items(f, g):
                fv, gv = value_pair
                if key == 'prime_cycle': continue
                if key == 'prime1':
                    h.__dict__[key] = (div, ((sub, (mul(g, fv), mul(f, gv))), (mul, (g, g))))
                    continue
            return h
        elif _validation.is_numeric(g):
            h = mathfunc(lambda x: f(x) / g)
            for key, value in f.__dict__.items():
                if key == 'prime_cycle':
                    h.__dict__[key] = value
                    continue
                if key.startswith('prime'):
                    h.__dict__[key] = (div, (value, g))
                    continue
            h.composition = '('+f.composition+'/'+str(g)+')'
            return h
        raise TypeError('Inappropriate argument type.')

    @_decorators.arg_modifier(_validation.trynumber)
    def __rtruediv__(f, g):
        if f'rdiv{g}' in f.__dict__: return f.solve_key(f'rdiv{g}')        
        if g in (0, trivial):
            return trivial
        if f == g: return trivial + 1
        if f == -g: return trivial-1
        if callable(g):
            return mathfunc(g)/f
        elif _validation.is_numeric(g):
            h = mathfunc(lambda x: f(x) / g)
            for key, value in f.__dict__.items():
                if key == 'prime1':
                    h.prime1 = (mul, (g, (div, (value, -(f**2)))))
                    continue
            h.composition = '('+str(g)+'/'+f.composition+')'
            return h
        raise TypeError('Inappropriate argument type.')
    
    @_decorators.arg_modifier(_validation.trynumber)
    def __pow__(f, g):
        if g == 1: return f
        if f'pow{g}' in f.__dict__: return f.solve_key(f'pow{g}')
        if g in (trivial, 0): return trivial + 1
        if callable(g):
            h = mathfunc(lambda x: f(x) ** g(x))
            h = mathfunc(lambda x: f.func(x) ** g.func(x))
            for key, value_pair in mathfunc.merge_items(f, g):
                fv, gv = value_pair
                if key == 'prime1':
                    h.prime1 = (mul, (h, (add, ((mul, (ln(f), gv)),(mul, ((div, (fv, f)), g))))))
                    continue
            h.composition = '('+f.composition+'**'+g.composition+')'
            return h
        elif _validation.is_numeric(g):
            h = mathfunc(lambda x: f(x) ** g)
            for key, value in f.__dict__.items():
                if key == 'prime1':
                    h.__dict__[key] = (mul, ((mul, (g, pow(f, g-1)), (value))))
                    continue
            h.composition = '('+f.composition+'**'+str(g)+')'
            return h
        raise TypeError('Inappropriate argument type.')

    @_decorators.arg_modifier(_validation.trynumber)
    def __rpow__(f, g):
        if g == 1: return trivial + 1
        if g in (trivial, 0): return trivial
        if callable(g):
            return mathfunc(g)**f
        elif _validation.is_numeric(g):
            h = mathfunc(lambda x: f(x) + g)
            for key, value in f.__dict__.items():
                if key.startswith('prime'):
                    if key == 'prime_cycle': continue
                    h.__dict__[key] = (mul, (mul, (h, ln(g)), value))
                    continue
            h.composition = '('+str(g)+'**'+f.composition+')'
            return h
        raise TypeError('Inappropriate argument type.')
    
    @staticmethod
    def resolve_tuple_key(x):
        if type(x) is _old_tuple:
            y, z = x
            a, b = z
            if type(a) is _old_tuple:
                a = mathfunc.resolve_tuple_key(a)
                z = (a, b)
            if type(b) is _old_tuple:
                b = mathfunc.resolve_tuple_key(b)
                z = (a, b)
            return y(*z)
        return x

    def solve_key(self, key):
        self.__dict__[key] = self.resolve_tuple_key(self.__dict__[key])
        return self.__dict__[key]

    @_decorators.arg_modifier(_validation.trynumber)
    def derivative(f, kth=1):
        '''find the kth derivative of f'''
        if 'prime_cycle' in f.__dict__:
            if kth > f.prime_cycle:
                kth = f.prime_cycle+(kth%f.prime_cycle)
        if f'prime{kth}' in f.__dict__: return f.solve_key(f'prime{kth}')
        
        assert _validation.is_integer(kth) #fractional derivative not implemented yet
        assert kth >= 0 #anti-derivate not implemented yet

        
        
        if kth == 0: return f
        if kth == 1:
            return mathfunc(lambda x: ((f(x+dx)-f(x))/dx))
        return f.derivative(kth-1).derivative()

trivial = mathfunc(lambda x: 0)
trivial.__name__ = 'trivial'
trivial.composition = '0'
trivial.prime1 = trivial
trivial.prime_cycle = 1
trivial.negative = trivial

identity = mathfunc(lambda x: x)
identity.__name__ = 'identity'
identity.prime1 = trivial + 1
identity.composition = '(x)'
mathfunc.inverses(identity, identity)

@_decorators.arg_modifier(_validation.trynumber)
@_decorators.io_opt
def poly_term(a, n):
    if a == 0: return trivial
    if n == 0: return constant(a)
    if a == 1 and n == 1: return identity
    @mathfunc
    def term(x):
        return a*(x**n)
    if a != 1:
        if n != 1:
            term.composition = f'({a}*(x**{n}))'
        else: term.composition = f'({a}*x)'
    else:
        term.composition = f'(x**{n})'
    term.prime1 = (poly_term, (a*n, n-1))
    return term

@_decorators.arg_modifier(_validation.trynumber)
@_decorators.io_opt
def polynomial(*coeficients):
    degree = len(coeficients)
    terms = [poly_term(coeficient, degree-num-1) for num, coeficient in enumerate(coeficients)]
    nomial = sum(terms)
    nomial.composition = '+'.join(map(lambda x: x.composition, terms))
    return nomial

@_decorators.arg_modifier(_validation.trynumber)
@_decorators.io_opt
def constant(x):
    if x == 0: return trivial
    else:
        h = trivial + x
        h.composition = f'({x})'
        return h

@mathfunc
def floor(x, /):
    '''Return the floor of x'''
    try:
        if x > 0: return int(x)
        else:
            return int(x) if _validation.is_integer(x) else int(x) - 1
    except:pass #lower nesting
    return floor(x.real) + floor(x.imag)*1j if type(x) is complex else x.__floor__()

@mathfunc
def ceil(x, /):
    '''Return the ceil of x'''
    try:
        if x > 0:
            return int(x) if _validation.is_integer(x) else int(x) + 1
        else: return int(x)
    except: pass
    return ceil(x.real) + ceil(x.imag)*1j if type(x) is complex else x.__ceil__()

def convert(value, frm, to):
    '''Convert value from 'frm' units to 'to' units.'''
    if frm == to: return value
    assert conversions[frm]['type'] == conversions[to]['type']
    valuefrm, valueto = eval(conversions[frm]['value']), eval(conversions[to]['value'])
    return _validation.trynumber((value/valuefrm)*valueto)

### miscillaneous ###
def summation(start, finish, function = lambda x: x):
    '''Σ'''
    if finish == inf:
        try:
            # This is not true infinite summation, but it does give an
            # approximation, (this does mean that it can be stuck in an infinite
            # loop... not yet sure how to counter this accurately and efficiently.
            # but eventually a number gets to big or to small for python to handle
            prev = 10
            prev1 = 10
            prev2 = 10
            change = function(start)
            sm = 0
            ##print('in')
            while not all(map(lambda x: abs(x)<1e-25, (change, prev, prev1, prev2))):
                start += 1
                try:
                    ##print(sm, '+', change)
                    sm += change
                    prev2 = prev1
                    prev1 = prev
                    prev = change
                    change = function(start)
                except: return sm
            return sm
        except: return sm
    rangelist = list(range(start, finish+1))
    rangelist[0] = function(rangelist[0])
    return _reduce((lambda x, y: x+function(y)), rangelist)

@mathfunc
def sigmoid(x, /):
    '''Sigmoid function'''
    epow = exp(-x)
    return 1/(1+epow)

def dist(p, q, /):
    try: return _math.dist(p, q)
    except: pass
    if len(p) != len(q):
        raise ValueError('both points must have the same number of dimensions')
    args = [x-y for x, y in zip(p, q)]
    return hypot(*args)

def hypot(*coordinates):
    try: return _math.hypot(*coordinates)
    except: return sqrt(sum(map(square, coordinates)))

### powers and exponents ###
def rt(nth, of):
    '''Find the nth root of (n must be an integer)'''
    assert _validation.is_integer(nth)
    try: nth = int(nth)
    except: nth = int(float(nth))
    
    try: is_negative = of < 0
    except: is_negative = False

    if is_negative: of, final = -of, 1j
    else: final =1
    approx = of
    nthm1 = nth-1
    
    done = False
    while not done:
        change = (approx**nth-of)/(nth*approx**nthm1)
        approx -= change
        done = abs(change) < (5e-16)

    return approx*final

def irt(nth, num, /):
    '''Return floor nth root of num'''
    assert _validation.is_integer(nth)
    try: nth = int(nth)
    except: nth = int(float(nth))
    return floor(rt(nth, num))

def ldexp(x, i, /):
    '''The inverse of frexp().'''
    try: return _math.ldexp(x, i)
    except: pass
    return x*(2**i)

def frexp(x, /):
    '''Return the mantissa and exponent of x, as pair (m, e).

m is a float and e is an int, such that x = m * 2.**e.
If x is 0, m and e are both 0.  Else 0.5 <= abs(m) < 1.0.'''
    try: return _math.frexp(x) # Always try to use optimized method
    except: pass
    n = floor(log2(x)) + 1
    n1 = x/(2**n)
    return (n1, n)

@mathfunc
def exp(x, /):
    '''Return e to the power of x'''
    try: return _math.exp(x)
    except: pass
    try: return _cmath.exp(x)
    except: pass
    try: return x.__exp__()
    except: return e**x # this final section may cause a recursive loop if 
    # the method __pow__ or __rpow__ calls exp, but if it doesn't then this
    # handles it.

exp.prime_cycle = 1

@mathfunc
def expm1(x, /):
    '''Return exp(x)-1'''
    try: return _math.expm1(x)
    except: return exp(x)-1

exp.sub1 = expm1
expm1.derivative = exp
expm1.add1 = exp

@mathfunc
def sqrt(x, /):
    '''Return the square root of x'''
    try: return _math.sqrt(x)
    except: pass
    try: return _cmath.sqrt(x)
    except: pass
    try: return x**(1/2)
    except: pass
    return rt(2, x)

def isqrt(x, /):
    '''Return the floored square root of x'''
    try: return _math.isqrt(x)
    except: return floor(sqrt(x))

@mathfunc
def cbrt(x, /):
    '''Return the cube root of x'''
    try: return x**(1/3)
    except: pass
    return rt(3, x)

def icbrt(x, /):
    '''Return the floored cube root of x'''
    try: return floor(x**(1/3))
    except: pass
    return irt(3, x)

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
    x = _validation.trynumber(x)
    if x == 0:
        raise ValueError('math domain error')
    if _validation.is_float(x):
        return _math.log(x)
    elif _validation.is_complex(x):
        return _cmath.log(x)
    else:
        try: return x.__ln__()
        except: pass
        try: return x.__log__(e)
        except: pass
    raise TypeError('Natural logarithm cannot be found of a type %s.' % type(x))

ln.prime1 = 1/identity

@_decorators.shift_args({2:(0, 1), 1:((10,), 0)})
def log(base, x):
    ''' log([base = 10], x)
    Return the log base 'base' of x
    recources to x.__log__(base) if log cannot be found'''
    base = _validation.trynumber(base)
    x = _validation.trynumber(x)
    if x == base: return 1
    if x == 0:
        raise ValueError('math domain error')
    if _validation.is_float(x):
        return _math.log(x, base)
    elif _validation.is_complex(x):
        return _cmath.log(x, base)
    else:
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
    x = _validation.trynumber(x)
    if x == 0:
        raise ValueError('math domain error')
    elif _validation.is_float(x):
        return _math.log2(x)
    else:
        try: return log(2, x)
        except: pass
    raise TypeError('Logarithm base 2 cannot be found of a type %s.' % type(x))

@mathfunc
def log1p(x, /):
    '''Return the natural logarithm of x+1'''
    try: return _math.log1p(x)
    except: return ln(x+1)

### complex ###

def phase(z, /):
    '''Return angle of number'''
    try:
        if _validation.is_float(z):z=float(z)
        z = complex(z)
        return (_cmath.phase(z), 1j)
    except: pass
    try: return z.__phase__()
    except:pass
    raise TypeError('%s has no phase' % type(z))

def polar(z, /):
    '''Return a number in polar form'''
    try:
        if _validation.is_float(z):z=float(z)
        z = complex(z)
        return (*_cmath.polar(z), 1j)
    except: pass
    try: return z.__polar__()
    except:pass
    raise TypeError('%s has no polar' % type(z))

def rect(r, phi, n = 1j):
    '''Create complex back from polar form'''
    return r*(cos(phi) + n*sin(phi))

##
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

##BUG: adding two trig funcs returns a mathfunc, which stops non-default setting calling.
class trig_func(mathfunc):

    def __call__(self, θ, /, setting = None):
        try:
            θ.__call__
            y = θ
            return mathfunc(lambda θ: self(y(θ)))
        except: pass
        if setting is None: setting = _angle
        θ = _validation.trynumber(convert(θ, setting, 'rad'))
        return self.func(θ)

    def __repr__(self):
        return  f'<nmath.trig_func {self.composition} at {hex(id(self))}>'

@_decorators.io_opt
def trig_func_with_extras(**extras):

    def trig_func_dec(func): return trig_func(func, **extras)
    return trig_func_dec

class inverse_trig_func(mathfunc):

    def __call__(self, x, /, setting = None):
        try:
            x.__call__
            y = x
            return mathfunc(lambda x: self(y(x)))
        except: pass
        if setting is None: setting = _angle
        θ = self.func(_validation.trynumber(x))
        return _validation.trynumber(convert(θ, 'rad', setting))

    def __repr__(self):
        return  f'<nmath.inverse_trig_func {self.composition} at {hex(id(self))}>'

@_decorators.io_opt
def inverse_trig_func_with_extras(**extras):

    def inverse_trig_func_dec(func): return inverse_trig_func(func, **extras)
    return inverse_trig_func_dec

def get_angle():
    return _angle

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
    if not isclose(abs(n), 1):
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

tan.prime1 = (pow, (sec, 2))
sec.prime1 = (mul, (sec, tan))
cot.prime1 = neg, ((pow, (csc, 2)), None)
csc.prime1 = neg, ((mul, (csc, cot)), None)

sin.__dict__[f'div{cos}'] = tan
cos.__dict__[f'div{sin}'] = cot
(-sin).__dict__[f'div{cos}'] = -tan
(-cos).__dict__[f'div{sin}'] = -cot

class t: #taylor series
    def cos(theta, /):
        '''taylor series for cos.'''
        def iteration(n):
            trueiter = 2*n
            sign = (-1)**n
            denom = factorial(trueiter)
            return sign * (theta**trueiter)/denom
        return summation(0, inf, iteration)

    def sin(theta, /):
        '''taylor series for sin.'''
        def iteration(n):
            trueiter = 2*n+1
            sign = (-1)**n
            denom = factorial(trueiter)
            return sign * (theta**trueiter)/denom
        return summation(0, inf, iteration)

    def tan(theta, /):
        ##TODO: Add Taylor Series for tan
        return t.sin(theta)/t.cos(theta) 

    def exp(num):
        def iteration(x): 
            if x == 0: return 1
            if x == 1: return num
            return (num**x)/factorial(x)
        return summation(0, inf, iteration)

    def ln(x):
        '''taylor series for ln. Only works for real numbers. A complex number
will return an incorrect value.'''
        x = _validation.trynumber(x)
        if x == 0: raise ValueError('math domain error')
        if x == 1: return 0
        if x == 2: return 0.6931471805599453
        if not _validation.is_numeric(x): raise TypeError(f'Value {x} is not a numeric value (a numeric type is any which supports all arithmetic operations with int, float, and complex')
        if abs(x) >=2: return 0.6931471805599453+t.ln(x/2)
        def iteration(n):
            if n == 0: return 0
            return -((x**n)/n)
        x = -x+1
        return summation(0, inf, iteration)

#eof
