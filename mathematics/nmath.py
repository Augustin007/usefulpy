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
'''
##Usefulpy 1.2.1
__version__='3.1.1'
__author__ = 'Austin Garcia'

from usefulpy import validation as _validation

from decimal import Decimal as number
from fractions import Fraction as fraction

import cmath as _cmath
import math as _math
import json as _json
import os as _os

from math import comb, copysign, dist, erf, erfc, expm1, fabs, factorial
from math import fmod, frexp, fsum, gamma, hypot, ldexp, lgamma, modf
from math import nextafter, perm, prod, remainder, trunc, ulp

dirlist = __file__.split(_os.sep)
dirlist[-1] = 'Conversions.json'

_conversions_file_name = _os.sep.join(dirlist)

#Some of the values here are not acurate enough for perfect use
conversions = _json.loads(open(_conversions_file_name).read())

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


# Our irrationals

# more digits than it will store... so the most accurate possible
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

#Algebraic numbers

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
# (r-1) = (1/r) ## No need to go any further, this is a definition of φ
# r = φ, or the radical conjugate of φ, which we will note as φ_
# Thus:
# (1/a)**(1/φ_) = φ_*a and (1/a)**(1/φ) = ra
# or
# (1/a)**(1/r) = ra
# where r assumes the properties of φ and φ_
# (1/a)**(1/r) = ra
# (1/a)**(r-1) = ra   ##prop of φ
# a**(1-r) = ra
# a**r = r
# a = ^r√r ## rth root of r, true for φ and φ_
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

# Its a bit of a tongue twister, but: the number nicknamed monster is the
#Number of sets of symmetries in the largest finite group of sets of symmetries
monster = 808017424794512875886459904961710757005754368000000000

Avogadro = 6.02214076e+23

#checks
def odd(num, /):
    '''Return True if num is odd'''
    return num%2 != 0

def even(num, /):
    '''Return True if num is even'''
    return num%2 == 0

def isclose(a, b, *, rel_tol=1e-09, abs_tol=0.0):
    '''Return True if a is close to b'''
    if isnan(a) or isnan(b): return False
    if isinf(a) or isinf(b): return a == b
    tol, difference = max((abs(abs(b)*rel_tol)), abs(abs_tol)), abs(a-b)
    return tol >= difference

def isinf(x, /):
    '''Return True if x is inf in any direction'''
    if x in (inf, infj, neg_inf, neg_infj): return True
    try:
        if x.real in (inf, neg_inf): return True
        else: return x.imag in (inf, neg_inf)
    except:
        if x.real in (inf, neg_inf): return True
        if x.i in (inf, neg_inf): return True
        if x.j in (inf, neg_inf): return True
        return x.k in (inf, neg_inf)

def isnan(x, /):
    '''Return True if x is nan in any way'''
    if x in (nan, nanj): return True
    try:
        if (x.real in nan): return True
        else: return x.imag in (nan)
    except:
        if x.real in (nan): return True
        if x.i in (nan): return True
        if x.j in (nan): return True
        return x.k in (nan)

def isfinite(x, /):
    '''Return True if x is finite'''
    return not (isnan(x) or isinf(x))

#Broadening abilities
class math_tuple(tuple):
    '''A tuple modified for math work'''
    def __add__(self, other):
        '''Return self+other'''
        return math_tuple([n+other for n in self])
    def __radd__(self, other):
        '''Return other+self'''
        return math_tuple([other+n for n in self])
    def __sub__(self, other):
        '''Return self-other'''
        return math_tuple([n-other for n in self])
    def __rsub__(self, other):
        '''Return other-self'''
        return math_tuple([other-n for n in self])
    def __mul__(self, other):
        '''Return self*other'''
        return math_tuple([n*other for n in self])
    def __rmul__(self, other):
        '''Return other*self'''
        return math_tuple([other*n for n in self])
    def __truediv__(self, other):
        '''Return self/other'''
        return math_tuple([n/other for n in self])
    def __rtruediv__(self, other):
        '''Return other/self'''
        return math_tuple([other/n for n in self])
    def __pow__(self, other):
        '''Return self**other'''
        return math_tuple([n**other for n in self])
    def __rpow__(self, other):
        '''Return other**self'''
        return math_tuple([other**n for n in self])
    def floor(self):
        '''Return floor(self)'''
        return math_tuple([floor(n) for n in self])
    def ceil(self):
        '''Return ceil(self)'''
        return math_tuple([ceil(n) for n in self])

_setting = 'approx'
_mathfuncs = {}
def add_mathfunc(name, approx, exact, *argnames):
    '''Create a math function'''
    tmp = ['self']
    tmp.extend(argnames)
    
    args = '('+ ', '.join(argnames)+ ')'

    call_args = '('+ ', '.join(tmp)+ ')'
    del tmp
    
    class mathfunc():
        def __new__(cls, name, approx, exact):
            self = super(mathfunc, cls).__new__(cls)
            self.approx = approx
            
            self.exact = exact

            split = name.split('_')
            self.name = split[0]
            self.extras = split[1:]

            self.hexid = hex(id(self))
            _mathfuncs[name] = self
            return self

        exec(f'''def __call__{call_args}:
            if _setting == 'exact':
                return self.exact{args}
            if _setting == 'approx':
                return self.approx{args}''')

        def __repr__(self):
            return f'<nmath.mathfunc {self.name} at {self.hexid}>'

    
    tmp = mathfunc(name, approx, exact)
    exec(f'global {name}\n{name} = tmp')
    return tmp

def pm(a, b):
    '''Return a ± b'''
    return math_tuple((a+b, a-b))

def floor(x, /):
    '''Return the floor of x'''
    try:
        if x > 0: return int(x)
        else:
            return int(x) if _validation.is_integer(x) else int(x) - 1
    except:pass #lower nesting
    return floor(x.real) + floor(x.imag)*1j if type(x) is complex else x.floor()

def ceil(x, /):
    '''Return the ceil of x'''
    try:
        if x > 0:
            return int(x) if _validation.is_integer(x) else int(x) + 1
        else: return int(x)
    except: pass
    return ceil(x.real) + ceil(x.imag)*1j if type(x) is complex else x.ceil()

def convert(value, frm, to):
    '''Convert value from 'frm' units to 'to' units.'''
    if frm == to: return value
    assert conversions[frm]['type'] == conversions[to]['type']
    valuefrm, valueto = eval(conversions[frm]['value']), eval(conversions[to]['value'])
    return _validation.trynumber((value/valuefrm)*valueto)

#miscillaneous
def summation(start, finish, function = lambda x: x):
    '''Σ'''
    if finish == inf: #This is not true infinite summation, but it does give an
        #approximation, (this does mean that it can be stuck in an infinite
        #loop... not yet sure how to counter this accurately and efficiently.
        #but eventually a number gets to big or to small for python to handle
        #This temporary version is mostly for a few _experimental functions
        #(see line 584) which uses this to simulate an infinite taylor series
        #aproxmiating trigonometric expressions, where it stays (from my
        #observations and experiments) mostly in the 75-100 range before a number
        #is 'too large to convert to a float'.
        sm = function(start)
        while True:
            start += 1
            try: sm += function(start)
            except: return sm
    rangelist = list(range(start, finish+1))
    rangelist[0] = function(rangelist[0])
    return _reduce((lambda x, y: x+function(y)), rangelist)

def sigmoid(x, /):
    '''Sigmoid function'''
    epow = exp(-x)
    return 1/(1+epow)

#powers and exponents
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

def exp(x, /):
    '''Return e to the power of x'''
    try: return _math.exp(x)
    except: pass
    try: return _cmath.exp(x)
    except: return e**x

def expm1(x, /):
    '''Return e**x-1'''
    try: return _math.expm1(x)
    except: return exp(x)-1

def sqrt(x, /):
    '''Return the square root of x'''
    try: return _math.sqrt(x)
    except: pass
    try: return _cmath.sqrt(x)
    except: return rt(2, x)

def isqrt(x, /):
    '''Return the floored square root of x'''
    try: return _math.isqrt(x)
    except: return floor(sqrt(x))

def cbrt(x, /):
    '''Return the cube root of x'''
    return rt(3, x)

def icbrt(x, /):
    '''Return the floored cube root of x'''
    return irt(3, x)

def square(x, /):
    '''Return x**2'''
    return x*x

def cube(x, /):
    '''Return x**3'''
    return x*x*x

def tesser(x, /):
    '''Return x**4'''
    return x*x*x*x

def ln(x, /):
    '''Return the natural logarithm of x'''
    try: return _math.log(x)
    except: return _cmath.log(x)

def log(x, base = 10, /):
    '''Return the log base 'base' of x'''
    try: return _math.log(x, base)
    except: return _cmath.log(x, base)

def log2(x, /):
    '''Return the log base 2 of x'''
    try: return _math.log2(x)
    except: return log(x, 2)

def log1p(x, /):
    '''Return the natural logarithm of x+1'''
    try: return _math.log1p(x)
    except: return ln(x+1)
#complex

def phase(z, /):
    '''Return angle of number'''
    try: return z.__polar__()[1:]
    except:pass
    if _validation.is_float(z): z = float(z)
    z = complex(z)
    return atan(z.imag/z.real)

def polar(z, /):
    '''Return a number in polar form'''
    try: return z.__polar__() #Catch a quaternion class.
    except:pass
    if _validation.is_float(z): z = float(z)
    z = complex(z)
    return (abs(z), _math.atan2(z.imag, z.real))

def rect(r, phi, /):
    '''Create complex back from polar form'''
    return r*cis(phi)

#trig
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

def acos(θ, /):
    '''Return the arc cosine of θ'''
    try: ans = _math.acos(θ)
    except: ans = _cmath.acos(θ)
    return convert(ans, 'rad', _angle)

def acosh(θ, /):
    '''Return the inverse hyperbolic cosine of θ'''
    try: ans = _math.acosh(θ)
    except: ans = _cmath.acosh(θ)
    return convert(ans, 'rad', _angle)

def asin(θ, /):
    '''Return the arc sine of θ'''
    try: ans = _math.asin(θ)
    except: ans = _cmath.asin(θ)
    return convert(ans, 'rad', _angle)

def asinh(θ, /):
    '''Return the inverse hyperbolic sine of θ'''
    try: ans = _math.asinh(θ)
    except: ans = _cmath.asinh(θ)
    return convert(ans, 'rad', _angle)

def atan(θ, /):
    '''Return the arc tangent of θ'''
    try: ans = _math.atan(θ)
    except: ans = _cmath.atan(θ)
    return convert(ans, 'rad', _angle)

def atanh(θ, /):
    '''Return the inverse hyperbolic tangent of θ'''
    try: ans = _math.atanh(θ)
    except: ans = _cmath.atanh(θ)
    return convert(ans, 'rad', _angle)

def asec(θ, /):
    '''Return the arc secant of θ'''
    try: return acos(1/θ)
    except ZeroDivisionError: return nan

def asech(θ, /):
    '''Return the inverse hyperbolic secant of θ'''
    try: return acosh(1/θ)
    except ZeroDivisionError: return nan

def acsc(θ, /):
    '''Return the arc cosecant of θ'''
    try: return asin(1/θ)
    except ZeroDivisionError: return nan

def acsch(θ, /):
    '''Return the inverse hyperbolic cosecant of θ'''
    try: return asinh(1/θ)
    except ZeroDivisionError: return nan

def acot(θ, /):
    '''Return the arc cotangent of θ'''
    try: return atan(1/θ)
    except ZeroDivisionError: return nan

def acoth(θ, /):
    '''Return the inverse hyperbolic cotangent of θ'''
    try: return atanh(1/θ)
    except ZeroDivisionError: return nan

def cos(θ, /):
    '''Return the cosine of θ'''
    try:
        θ = θ%_circle
        qc = _circle/4
        if θ == qc: return 0
        if θ == 3*qc: return 0
        if θ == 2*qc: return -1
        if θ == 0: return 1
    except: pass
    θ = convert(θ, _angle, 'rad')
    try: return _math.cos(θ)
    except: return _cmath.cos(θ)

def cosh(θ, /):
    '''Return the hyperbolic cosine of θ'''
    θ = convert(θ, _angle, 'rad')
    try: return _math.cosh(θ)
    except: return _cmath.cosh(θ)

def sin(θ, /):
    '''Return the sine of θ'''
    try:
        θ = θ%_circle
        qc = _circle/4
        if θ == qc: return 1
        if θ == 3*qc: return -1
        if θ == 2*qc: return 0
        if θ == 0: return 0
    except: pass
    θ = convert(θ, _angle, 'rad')
    try: return _math.sin(θ)
    except: return _cmath.sin(θ)

def sinh(θ, /):
    '''Return the hyperbolic sine of θ'''
    θ = convert(θ, _angle, 'rad')
    try: return _math.sinh(θ)
    except: return _cmath.sinh(θ)

def tan(θ, /):
    '''Return the tangent of θ'''
    try:
        θ = θ%_circle
        qc = _circle/4
        if θ == qc: return nan
        if θ == 3*qc: return nan
        if θ == 2*qc: return 0
        if θ == 0: return 0
    except: pass
    θ = convert(θ, _angle, 'rad')
    try: return _math.tan(θ)
    except: return _cmath.tan(θ)

def tanh(θ, /):
    '''Return the hyperbolic tangent of θ'''
    θ = convert(θ, _angle, 'rad')
    try: return _math.tanh(θ)
    except: return _cmath.tanh(θ)

def sec(θ, /):
    '''Return the secant of θ'''
    try: return 1/cos(θ)
    except ZeroDivisionError: return nan

def sech(θ, /):
    '''Return the hyperbolic secant of θ'''
    try: return 1/cosh(θ)
    except ZeroDivisionError: return nan

def csc(θ, /):
    '''Return the cosecant of θ'''
    try: return 1/sin(θ)
    except ZeroDivisionError: return nan

def csch(θ, /):
    '''Return the hyperbolic cosecant of θ'''
    try: return 1/sinh(θ)
    except ZeroDivisionError: return nan

def cot(θ, /):
    '''Return the cotangent of θ'''
    try: return 1/tan(θ)
    except ZeroDivisionError: return nan

def coth(θ, /):
    '''Return the hyperbolic cotangent of θ'''
    try: return 1/tanh(θ)
    except ZeroDivisionError: return nan

def cis(θ, /):
    '''Return cos(θ) + isin(θ)'''
    return cos(θ)+(1j*sin(θ))

class _experiment:
    #math denotes with a t refers to Taylor series
    class t:
        def cos(theta, /):
            def iteration(n):
                trueiter = 2*n
                sign = (-1)**n
                denom = factorial(trueiter)
                return sign * (theta**trueiter)/denom
            return summation(0, inf, iteration)

        def sin(theta, /):
            def iteration(n):
                trueiter = 2*n+1
                sign = (-1)**n
                denom = factorial(trueiter)
                return sign * (theta**trueiter)/denom
            return summation(0, inf, iteration)

        def tan(theta, /):
            def iteration(n):
                pass

#eof
