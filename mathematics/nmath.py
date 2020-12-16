'''
File: nmath.py
Version: 1.1.2
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
'''

__version__ = '2.1.1'

#Primary importations
from functools import reduce as _reduce
from usefulpy import validation as _validation
import cmath as _cmath
import math as _math
from math import e, pi, tau, nan, inf
from cmath import infj, nanj

import warnings
from decimal import Decimal as num
from fractions import Fraction as fraction

from cmath import phase, polar, rect
from math import ceil, comb, copysign, dist, erf, erfc, expm1, fabs, factorial
from math import floor, fmod, frexp, fsum, gamma, hypot, ldexp, lgamma, modf
from math import nextafter, perm, prod, remainder, trunc, ulp

def sqrt(x, /):
    try: return _math.sqrt(x)
    except: return _cmath.sqrt(x)

def isqrt(x, /):
    try: return _math.isqrt(x)
    except: return complex(int(_cmath.sqrt(x).real), int(_cmath.sqrt(x).imag))

def exp(x, /):
    '''return e to the power of x'''
    try: return _math.exp(x)
    except: return _cmath.exp(x)

def isclose(a, b, *, rel_tol=1e-09, abs_tol=0.0):
    try: return _math.isclose(a, b, rel_tol=1e-09, abs_tol=0.0)
    except: return _cmath.isclose(a, b, rel_tol=1e-09, abs_tol=0.0)

def isfinite(x, /):
    try: return _math.isfinite(x)
    except: return _cmath.isfinite(x)

def isinf(x, /):
    try: return _math.isinf(x)
    except: return _cmath.isinf(x)

def isnan(x, /):
    try: return _math.isnan(x)
    except: return _cmath.isnan(x)

def RadiansToDegrees(r):
    '''Convert radians to degrees.'''
    d = (r*180)/pi; return _validation.tryint(d)

def DegreesToRadians(r):
    '''Convert degrees to radians.'''
    d = (r*pi)/180; return _validation.tryint(d)

def makefraction(numer, denom = 1):
    '''Make a valid fraction type out of a float type'''
    numer = _validation.tryint(round(float(numer), 15))
    denom = _validation.tryint(round(float(denom), 15))
    while not (_validation.is_integer(numer) and _validation.is_integer(denom)):
        denom *= 10
        numer *= 10
    return fraction(int(numer), int(denom))

def rt(nth, num, /):
    '''return nth root of num'''
    return _validation.tryint(num**(1/nth))

def irt(nth, num, /):
    '''return integer nth root of num'''
    try: return int(rt(nth, num))
    except: return complex(int(rt(nth, num).real), int(rt(nth, num).imag))


def ln(x, /):
    try: return _math.log(x)
    except: return _cmath.log(x)
    
def log(x, base = 10, /):
    try: return _math.log(x, base)
    except: return _cmath.log(x, base)

_angle = 'rad'
_circle = tau

def radians():
    global _angle, _circle 
    _angle = 'rad'
    _circle = tau

def degrees():
    global _angle, _circle 
    _angle = 'deg'
    _circle = 360

def acos(θ, /):
    try: ans = _math.acos(θ)
    except: ans = _cmath.acos(θ)
    if _angle == 'deg':
        return RadiansToDegrees(ans)
    return ans

def acosh(θ, /):
    try: ans = _math.acosh(θ)
    except: ans = _cmath.acosh(θ)
    if _angle == 'deg':
        return RadiansToDegrees(ans)
    return ans

def asin(θ, /):
    try: ans = _math.asin(θ)
    except: ans = _cmath.asin(θ)
    if _angle == 'deg':
        return RadiansToDegrees(ans)
    return ans

def asinh(θ, /):
    try: ans = _math.asinh(θ)
    except: ans = _cmath.asinh(θ)
    if _angle == 'deg':
        return RadiansToDegrees(ans)
    return ans

def atan(θ, /):
    try: ans = _math.atan(θ)
    except: ans = _cmath.atan(θ)
    if _angle == 'deg':
        return RadiansToDegrees(ans)
    return ans

def atanh(θ, /):
    try: ans = _math.atanh(θ)
    except: ans = _cmath.atanh(θ)
    if _angle == 'deg':
        return RadiansToDegrees(ans)
    return ans

def asec(θ, /):
    try: return acos(1/θ)
    except ZeroDivisionError: return nan

def asech(θ, /):
    try: return acosh(1/θ)
    except ZeroDivisionError: return nan

def acsc(θ, /):
    try: return asin(1/θ)
    except ZeroDivisionError: return nan

def acsch(θ, /):
    try: return asinh(1/θ)
    except ZeroDivisionError: return nan

def acot(θ, /):
    try: return atan(1/θ)
    except ZeroDivisionError: return nan

def acoth(θ, /):
    try: return atanh(1/θ)
    except ZeroDivisionError: return nan

def cos(θ, /):
    try:
        θ = θ%_circle
        qc = _circle/4
        if θ == qc: return 0
        if θ == 3*qc: return 0
        if θ == 2*qc: return -1
        if θ == 0: return 1
    except: pass
    if _angle == 'deg':
        θ = DegreesToRadians(θ)
    try: return _math.cos(θ)
    except: return _cmath.cos(θ)

def cosh(θ, /):
    if _angle == 'deg':
        θ = DegreesToRadians(θ)
    try: return _math.cosh(θ)
    except: return _cmath.cosh(θ)

def sin(θ, /):
    try:
        θ = θ%_circle
        qc = _circle/4
        if θ == qc: return 1
        if θ == 3*qc: return -1
        if θ == 2*qc: return 0
        if θ == 0: return 0
    except: pass
    if _angle == 'deg':
        θ = DegreesToRadians(θ)
    try: return _math.sin(θ)
    except: return _cmath.sin(θ)

def sinh(θ, /):
    if _angle == 'deg':
        θ = DegreesToRadians(θ)
    try: return _math.sinh(θ)
    except: return _cmath.sinh(θ)

def tan(θ, /):
    try:
        θ = θ%_circle
        qc = _circle/4
        if θ == qc: return nan
        if θ == 3*qc: return nan
        if θ == 2*qc: return 0
        if θ == 0: return 0
    except: pass
    if _angle == 'deg':
        θ = DegreesToRadians(θ)
    try: return _math.tan(θ)
    except: return _cmath.tan(θ)

def tanh(θ, /):
    if _angle == 'deg':
        θ = DegreesToRadians(θ)
    try: return _math.tanh(θ)
    except: return _cmath.tanh(θ)

def sec(θ, /):
    try: return 1/cos(θ)
    except ZeroDivisionError: return nan

def sech(θ, /):
    try: return 1/cosh(θ)
    except ZeroDivisionError: return nan

def csc(θ, /):
    try: return 1/sin(θ)
    except ZeroDivisionError: return nan

def csch(θ, /):
    try: return 1/sinh(θ)
    except ZeroDivisionError: return nan

def cot(θ, /):
    try: return 1/tan(θ)
    except ZeroDivisionError: return nan

def coth(θ, /):
    try: return 1/tanh(θ)
    except ZeroDivisionError: return nan

def cis(θ, /):
    return cos(θ)+(1j*sin(θ))

def cbrt(x, /):
    return rt(3, x)

def icbrt(x, /):
    return irt(3, x)

def odd(num, /):
    return num%2 != 0

def even(num, /):
    return num%2 == 0

def summation(start, finish, function = lambda x: x):
    '''Σ'''
    rangelist = list(range(start, finish+1))
    rangelist[0] = function(rangelist[0])
    return _reduce((lambda x, y: x+function(y)), rangelist)

Σ = Sigma = summation #Summation is usually noted with a capital greek Sigma

π = pi # π, ratio of diameter to circumference in circle
τ = tau # τ, ratio of diameter to circumference in circle
#e, number where f(x)=e^x, its derivative, f'(x) also equals e^x
Phi = Φ = (1+sqrt(5))/2 #1/(1+1/(1+1/(1+1/(1+1/(1+1/(1+1/(1+1/(1+1/(...)))))))))
#also (a+a*Φ)/a*Φ = a/a*Φ, golden ratio
phi = φ = (1-sqrt(5))/2 #another solution for Φ, signified by lowecase phi
rho = ρ = cbrt((9+sqrt(69))/18)+cbrt((9-sqrt(69))/18) #ρ**3 = ρ+1
sigma = σ = 1+sqrt(2) #2+1/(2+1/(2+1/(2+1/(2+1/(2+1/(2+1/(2+1/(2+1/(...)))))))))
#Called silver ratio
lsigma = ς = 1-sqrt(2)#Alternate solution for sigma, signified with an alternate
#writing of sigma
kappa = κ = (3+sqrt(13))/2 #Bronze ratio, 3+1/(3+1/(3+1/(3+1/(3+1/(...)))))
psi = ψ = (1+(cbrt((29+3*sqrt(93))/2))+(cbrt((29-3*sqrt(93))/2)))/3
#ψ, supergolden ratio x**3 = x**2+1
#all the numbers I could think of...

#eof
