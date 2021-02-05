'''
File: nmath.py
Version: 3.1.1
Author: Austin Garcia

This file is essentially the importation of the math module, but a few small
functions are added or changed.

LICENSE:
This is a section of usefulpy. See usefulpy's lisence.md file.

PLATFORMS:
This is a section of usefulpy. See usefulpy.__init__'s "PLATFORMS" section.

INSTALLATION:
Put this file where Python can see it.

RELEASE NOTES:
1
 1.1
  Version 1.1.1
   Simple math importations with some changes and additions
  Version 1.1.2
   Changed some variable names and importations. More comments.
2
 2.1
  Version 2.1.1
   Reworked a lot of little details to allow for use with complex numbers
   throughout.
  Version 2.1.2
   Several new functions.
  Version 2.1.3
   Bug fixes
 2.2
  Version 2.2.1
   Some new functions and changing some internal workings
  Version 2.2.2
   Bug fixes (again)
3
 3.1
  Version 3.1.1
     ——Wednesday, the thirteenth day of the firstmonth Janurary, 2021——
   Rewrote on another document, cleaning up, improving, and adding functions
   throughout
  Version 3.2.2
   Small bugfixes
 3.2
  Version 3.2.1
  ...
'''

##UPDATED TO: Usefulpy 1.2.1
##TODO: Update for use with quaternions


### HEADERS ###
__version__='3.1.1'
__author__ = 'Austin Garcia'


### IMPORTS ###
from usefulpy import validation as _validation
from usefulpy import decorators as _decorators

from decimal import Decimal as number
from fractions import Fraction as fraction

import operator as _op
import cmath as _cmath
import math as _math
import json as _json
import os as _os

from math import comb, copysign, erf, erfc, fabs, factorial
from math import fmod, fsum, gamma, lgamma, modf
from math import nextafter, perm, prod, remainder, trunc, ulp

### CONVERSIONS ###
_dirlist = __file__.split(_os.sep)
_dirlist[-1] = 'Conversions.json'
_conversions_file_name = _os.sep.join(_dirlist)
conversions = _json.loads(open(_conversions_file_name).read())

##TODO: Update values for better use
#Some of the values here are not acurate enough for perfect use


### Support
def _reduce(function, sequence):
    it = iter(sequence); value = next(it)
    for element in it: value = function(value, element)
    return value

inf = float('inf')
neg_inf = -inf
infj = complex('infj')
neg_infj = -infj
nanj = complex('nanj')
nan = float('nan')


### Non-Algebraic Numbers ###

# way more digits than it will store... so the most accurate possible
# I originially had it be calculated with formulae, (averaging the leibniz
# and basil approach with odd numbers for pi) but I decided that this
# was more efficient and more accurate (I kept on adjusting the numbers to get
# a bit more accuracy, but I still wasn't quite happy with it.

#e, number where f(x)=e^x, its derivative, f'(x) also equals e^x
e = 2.7182818284590452353602874713526624977572470936999595749669676277240766303535475945713821785251664274#...
# π, ratio of diameter to circumference in circle
π = pi =  3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421#...
# τ, ratio of diameter to circumference in circle
τ = tau = 2*pi

### Algebraic numbers ###

# φ
#
# 1/(1+1/(1+1/(1+1/(1+1/(1+1/(1+1/(1+1/(1+1/(...)))))))))
# φ-1 = 1/φ, φ**2-φ = 1, φ**2-φ-1 = 0, etc.
# also (a+a*Φ)/a*Φ = a/a*Φ, golden ratio
#
# pops up everywhere
# for example, a math problem I did recently:
#
# f'(x) = f^-1(x)
# If you try to find a solution in the form
# f(x) = a(x**r)
# then f'(x) = (x**(r-1))
# and f^-1(x) = ((1/a)**(1/r))*(x**(1/r))
# if the equations will be equal, the power of x has to be equal, so
# (x**(r-1)) = (x**(1/r))
# (r-1) = (1/r) # No need to go any further, this is a definition of φ
# r = φ, (or the radical conjugate of φ, which we will note as φ_)
# Thus:
# (1/a)**(1/φ_) = φ_*a and (1/a)**(1/φ) = ra
# or
# (1/a)**(1/r) = ra
# where r assumes the properties of φ and φ_
# (1/a)**(1/r) = ra
# (1/a)**(r-1) = ra   #property of φ
# a**(1-r) = ra
# a**r = r
# a = ^r√r # rth root of r, true for φ and φ_
#
# this means f'(x) = f^-1(x) when f(x) = (^φ√φ)*(x**φ) or (^φ_√φ_)*(x**φ_)
# let's check this (because I've gotten carried away)
# f'(x) = φ(φ^√(1/φ))*(x**(φ-1))
# f'(x) = φ(φ^√φ**-1)*(x**(1/φ))
# f'(x) = φ(φ^√φ**-1)*(^φ√x)
# f'(x) = ^φ√(φ**φ)(φ^√φ**-1)*(^φ√x)
# f'(x) = ^φ√((φ**φ)φ**-1)*(^φ√x)
# f'(x) = ^φ√((φ**(φ-1))*^φ√x
# f'(x) = ^φ√((φ**(1/φ))*^φ√x
#
# f'(x) = ^(φ**2)√φ * ^φ√x
#
# f^-1(x) = (1/^φ√(1/φ))**(1/φ) * φ**1/φ
# f^-1(x) = (1/^φ√(1/φ))**(1/φ) * ^φ√x
# f^-1(x) = (1/(1/φ**(1/φ)))**(1/φ) * ^φ√x
# f^-1(x) = (φ**(1/φ))**(1/φ) * ^φ√x
# f^-1(x) = φ**(1/φ**2) * ^φ√x
#
# f^-1(x) = ^(φ**2)√φ * ^φ√x
#
# f'(x) = ^(φ**2)√φ * ^φ√x, f^-1(x) = ^(φ**2)√φ * ^φ√x
# f'(x) = f^-1(x)
# Quod Erat Demonstratum!

_radical = 5**(1/2)
φ = phi = (1+_radical)/2
#radical conjugate of φ, same properties
φ_ = phi_ = (1-_radical)/2 


#Bronze ratio, 3+1/(3+1/(3+1/(3+1/(3+1/(...)))))
_radical = 13**(1/2)
κ = kappa = (3+_radical)/2

 #ρ**3 = ρ+1
_radical = 69**(1/2)
_a = (9+_radical)/18
_b = (9-_radical)/18
ρ = rho = _a**(1/3)+_b**(1/3)

#ψ, supergolden ratio x**3 = x**2+1
_radical =93**(1/2)
_a = ((29+3*_radical)/2)**(1/3)
_b = ((29-3*_radical)/2)**(1/3)
_sum = (1+_a+_b)
ψ = psi = _sum/3

del _radical

# Its a bit of a tongue twister, but: the number nicknamed monster is the
# Number of sets of symmetries in the largest finite group of sets of symmetries
monster = 808017424794512875886459904961710757005754368000000000

### checks ###
def odd(num, /):
    '''Return True if num is odd'''
    return num%2 != 0

def even(num, /):
    '''Return True if num is even'''
    return num%2 == 0

def isclose(a, b, *, rel_tol=1e-09, abs_tol=0.0):
    '''Return True if a is close to b'''
    try: return _math.isclose(x) # Always try optimized c methods first
    except: pass
    try: return _cmath.isclose(x)
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

### Broadening abilities ###
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
    def flatten(self):
        '''flatten into 1 dimension'''
        return _validation.flatten(self)

class mathfunc(object):
    def __new__(cls, func): ##, *extras):
        self = super(mathfunc, cls).__new__(cls)
        self.func = func
        self.__name__ = self.func.__name__
        self.__doc__ = self.func.__doc__
        ##self.__call__.__doc__ = self.func.__doc__
        return self

    def __repr__(self):
        return f'<nmath.mathfunc {self.__name__} at {hex(id(self))}>'

    def __call__(self, x):
        return self.func(x)

    def __add__(f, g):
        try:
            g.__call__
            return mathfunc(lambda θ: f(θ) + g(θ))
        except: pass
        if _validation.is_numeric(g): return mathfunc(lambda θ: f.func(θ) + g)
        raise TypeError('Inappropriate argument type.')

    def __radd__(f, g):
        try:
            g.__call__
            return mathfunc(lambda θ: g(θ) + f.func(θ))
        except: pass
        if _validation.is_numeric(g): return mathfunc(lambda θ: g + f.func(θ))
        raise TypeError('Inappropriate argument type.')

    def __sub__(f, g):
        try:
            g.__call__
            return mathfunc(lambda θ: f.func(θ) - g(θ))
        except: pass
        if _validation.is_numeric(g): return mathfunc(lambda θ: f.func(θ) - g)
        raise TypeError('Inappropriate argument type.')

    def __rsub__(f, g):
        try:
            g.__call__
            return mathfunc(lambda θ: g(θ) - f.func(θ))
        except: pass
        if _validation.is_numeric(g): return mathfunc(lambda θ: g - f.func(θ))
        raise TypeError('Inappropriate argument type.')

    def __mul__(f, g):
        try:
            g.__call__
            return mathfunc(lambda θ: f.func(θ)*g(θ))
        except: pass
        if _validation.is_numeric(g): return mathfunc(lambda θ: f.func(θ)*g)
        raise TypeError('Inappropriate argument type.')

    def __rmul__(f, g):
        try:
            g.__call__
            return mathfunc(lambda θ: g(θ)*f.func(θ))
        except: pass
        if _validation.is_numeric(g): return mathfunc(lambda θ: g*f.func(θ))
        raise TypeError('Inappropriate argument type.')

    def __truediv__(f, g):
        try:
            g.__call__
            return mathfunc(lambda θ: f.func(θ)/g(θ))
        except: pass
        if _validation.is_numeric(g): return mathfunc(lambda θ: f.func(θ)/g)
        raise TypeError('Inappropriate argument type.')

    def __rtruediv__(f, g):
        try:
            g.__call__
            return mathfunc(lambda θ: g(θ)/f.func(θ))
        except: pass
        if _validation.is_numeric(g): return mathfunc(lambda θ: g/f.func(θ))
        raise TypeError('Inappropriate argument type.')

    def __pow__(f, g):
        try:
            g.__call__
            return mathfunc(lambda θ: f.func(θ)**g(θ))
        except: pass
        if _validation.is_numeric(g): return mathfunc(lambda θ: f.func(θ)**g)
        raise TypeError('Inappropriate argument type.')

    def __rpow__(f, g):
        try:
            g.__call__
            return mathfunc(lambda θ: g(θ)**f.func(θ))
        except: pass
        if _validation.is_numeric(g): return mathfunc(lambda θ: g**f.func(θ))
        raise TypeError('Inappropriate argument type.')

def pm(a, b):
    '''Return a ± b'''
    return tuple((a+b, a-b))

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
    try:
        num = int(num)
    except:
        return floor(rt(nth, of))
    else:
        a = 1 << -(-int.bit_length(xc)//n)
        while True:
            q, r = divmod(xc, a**(n-1))
            if a <= q: break
            a = (a*(n-1) + q)//n
        return a

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

@mathfunc
def expm1(x, /):
    '''Return exp(x)-1'''
    try: return _math.expm1(x)
    except: return exp(x)-1

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

@mathfunc
def log2(x, /):
    '''Return the log base 2 of x'''
    x = _validation.trynumber(x)
    if x == 0:
        raise ValueError('math domain error')
    elif _validation.is_float(x):
        return _math.log2(x)
    else:
        try: return log(x, 2)
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
    return r*(cos(phi) + 1j*sin(phi))

### trig ###
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

##BUG: adding two trig funcs returns a mathfunc, which stops non-setting calling.
class trig_func(mathfunc):
    def __new__(cls, func):
        self = super(trig_func, cls).__new__(cls, func)
        self.func = func
        self.__name__ = self.func.__name__
        self.__doc__ = self.func.__doc__
        ##self.__call__.__doc__ = self.func.__doc__
        return self

    def __call__(self, θ, /, setting = None):
        if setting is None: setting = _angle
        θ = _validation.trynumber(convert(θ, setting, 'rad'))
        return self.func(θ)

    def __repr__(self):
        return  f'<nmath.trig_func {self.__name__} at {hex(id(self))}>'
    
class inverse_trig_func(mathfunc):
    def __new__(cls, func):
        self = super(inverse_trig_func, cls).__new__(cls, func)
        self.func = func
        self.__name__ = self.func.__name__
        self.__doc__ = self.func.__doc__
        ##self.__call__.__doc__ = self.func.__doc__
        return self

    def __call__(self, x, /, setting = None):
        if setting is None: setting = _angle
        θ = self.func(_validation.trynumber(x))
        return _validation.trynumber(convert(θ, 'rad', setting))

    def __repr__(self):
        return  f'<nmath.inverse_trig_func {self.__name__} at {hex(id(self))}>'

@inverse_trig_func
def acos(x):
    '''Return the arc cosine of x,
recources to x.__acos__ if cos cannot be found'''
    if _validation.is_float(x):
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
    if _validation.is_float(x):
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
            except: ZeroDivisionError: zde = True
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
            except: ZeroDivisionError: zde = True
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
            except: ZeroDivisionError: zde = True
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
            except: ZeroDivisionError: zde = True
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
            except: ZeroDivisionError: zde = True
        except:pass
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
            except: ZeroDivisionError: zde = True
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
    raise TypeError('cos cannot be found of a type %s' % (type(x)))

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
    raise TypeError('cosh cannot be found of a type %s' % (type(x)))

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
    raise TypeError('sin cannot be found of a type %s' % (type(x)))

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
    raise TypeError('sinh cannot be found of a type %s' % (type(x)))

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
    raise TypeError('tan cannot be found of a type %s' % (type(x)))

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
    raise TypeError('tanh cannot be found of a type %s' % (type(x)))

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
    raise TypeError('sec cannot be found of a type %s' % (type(x)))

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
    raise TypeError('sech cannot be found of a type %s' % (type(x)))

@trig_func
def csc(θ):
    '''Return the cosecant of θ,
recources to θ.__csc__ if csc cannot be found'''
    if setting is None: setting = _angle
    θ = (_validation.trynumber(convert(θ, setting, 'rad')))
    
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
    raise TypeError('csc cannot be found of a type %s' % (type(x)))

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
    raise TypeError('csch cannot be found of a type %s' % (type(x)))

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
    raise TypeError('cot cannot be found of a type %s' % (type(x)))

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
    raise TypeError('coth cannot be found of a type %s' % (type(x)))

def cis(θ, n=1j):
    '''Return cos(θ) + nsin(θ)'''
    if abs(n) != 1:
        raise ValueError ('math domain error')
    if n.real != 1:
        raise ValueError ('math domain error')
    return cos(θ)+(n*sin(θ))

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
        if abs(x) >=2: return 0.6931471805599453+_experiment.t.ln(x/2)
        def iteration(n):
            if n == 0: return 0
            return -((x**n)/n)
        x = -x+1
        return summation(0, inf, iteration)

#eof
