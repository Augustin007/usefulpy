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

'''

__version__ = '1.1.2'

#Primary importations
from functools import reduce as _reduce
from math import *
del degrees, radians, log10
import warnings
from decimal import Decimal as num
from fractions import Fraction as fraction
from usefulpy import validation

def RadiansToDegrees(r):
    '''Convert radians to degrees.'''
    d = (r*180)/pi; return validation.tryint(d)

def DegreesToRadians(r):
    '''Convert degrees to radians.'''
    d = (r*pi)/180; return validation.tryint(d)

def makefraction(numer, denom = 1):
    '''Make a valid fraction type out of a float type'''
    numer = validation.tryint(round(float(numer), 15))
    denom = validation.tryint(round(float(denom), 15))
    while not (validation.is_integer(numer) and validation.is_integer(denom)):
        denom *= 10
        numer *= 10
    return fraction(int(numer), int(denom))

def rt(nth, num, /):
    '''return nth root of num'''
    return validation.tryint(num**(1/nth))

def irt(nth, num, /):
    '''return integer nth root of num'''
    return int(rt(nth, num))

_log = log
ln = lambda x: _log(x)
def log(x, base = 10, /): return _log(x, base)

_angle = 'rad'
def radians():
    global _angle
    _angle = 'rad'
def degrees():
    global _angle
    _angle = 'deg'
_acos=acos
def acos(θ, /):
    ans = _acos(θ)
    if _angle == 'deg':
        return RadiansToDegrees(ans)
    return ans
_acosh=acosh
def acosh(θ, /):
    ans = _acosh(θ)
    if _angle == 'deg':
        return RadiansToDegrees(ans)
    return ans
_asin=asin
def asin(x, /):
    ans = _asin(x)
    if _angle == 'deg':
        return RadiansToDegrees(ans)
    return ans
_asinh=asinh
def asinh(θ, /):
    ans = _asinh(θ)
    if _angle == 'deg':
        return RadiansToDegrees(ans)
    return ans
_atan=atan
def atan(θ, /):
    ans = _atan(θ)
    if _angle == 'deg':
        return RadiansToDegrees(ans)
    return ans
_atan2=atan2
def atan2(θ, /):
    ans = _atan2(θ)
    if _angle == 'deg':
        return RadiansToDegrees(ans)
    return ans
_atanh=atanh
def atanh(θ, /):
    ans = _atanh(θ)
    if _angle == 'deg':
        return RadiansToDegrees(ans)
    return ans
_cos=cos
def cos(θ, /):
    if _angle == 'deg':
        θ = DegreesToRadians(θ)
    return _cos(θ)
_cosh=cosh
def cosh(θ, /):
    if _angle == 'deg':
        θ = DegreesToRadians(θ)
    return _cosh(θ)
_sin=sin
def sin(θ, /):
    if _angle == 'deg':
        θ = DegreesToRadians(θ)
    return _sin(θ)
_sinh=sinh
def sinh(θ, /):
    if _angle == 'deg':
        θ = DegreesToRadians(θ)
    return _sinh(θ)
_tan=tan
def tan(θ, /):
    if _angle == 'deg':
        θ = DegreesToRadians(θ)
    return _tan(θ)
_tanh=tanh
def tanh(θ, /):
    if _angle == 'deg':
        θ = DegreesToRadians(θ)
    return _tanh(θ)

def cis(θ, /):
    return cos(θ)+(1j*sin(θ))

cbrt = lambda x: rt(3, x)

icbrt = lambda x: irt(3, x)

def odd(num, /): return num%2 != 0

def even(num, /): return num%2 == 0

def summation(start, finish, function = lambda x: x):
    '''Σ'''
    return _reduce((lambda x, y: x+function(y)), range(start, finish+1))

Σ = Sigma = summation #Summation is usually noted with a capital greek Sigma

pi = π = pi # π, ratio of diameter to circumference in circle
tau = τ = tau # τ, ratio of diameter to circumference in circle
e = e #e, number where f(x)=e^x, its derivative, f'(x) also equals e^x
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
