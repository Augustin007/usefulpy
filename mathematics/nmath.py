'''
File: nmath.py
Version: 3.2.1
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
   Mathfunc improvements/ trigfunc stuff, decorators
'''

##UPDATED TO: Usefulpy 1.2.1


### HEADERS ###
__version__='3.1.1'
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

from math import comb, copysign, erf, erfc, fabs, factorial, fmod, fsum, gamma
from math import lgamma, modf, nextafter, perm, prod, remainder, trunc, ulp

### CONVERSIONS ###
_dirlist = __file__.split(_os.sep)
_dirlist[-1] = 'Conversions.json'
_conversions_file_name = _os.sep.join(_dirlist)
conversions = _json.loads(open(_conversions_file_name).read())

##TODO: Add more values to conversions


### Support ###
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

##TODO: (mathfunc) Auto-generate names for this when based on other functions
##TODO: (mathfunc) Auto-generate derivatives, etc for functions based on other functions
##TODO: (mathfunc) add a .ispolynomial() check?
##TODO: (mathfunc) optimize for stuff like (cos**2)**2 should return a single func cos**4, not (cos**2)**2
##TODO: (mathfunc) polynomial class? polynomial
##TODO: (mathfunc) add a .roots() finder... maybe a number of roots
class mathfunc(object):
    def __new__(cls, func, **extras):
        self = super(mathfunc, cls).__new__(cls)
        self.__dict__ = extras
        self.func = func
        self.__name__ = self.func.__name__
        self.__doc__ = self.func.__doc__
        self.composition = self.__name__+'(x)'
        return self
    
    def __repr__(self):
        return f'<nmath.mathfunc {self.__name__} at {hex(id(self))}>'

    def __call__(self, x):
        try:
            x.__call__
            y = x
            h = mathfunc(lambda x: self(y(x)))
            h.composition = self.composition.replace('(x)', '('+x.composition+')')
            h.__name__ = self.__name__[0]+'0'+x.__name__[0]
            hmd = _validation.merge_dicts(self.__dict__, x.__dict__)
            for key, value_pair in hmd.items():
                fv, gv = value_pair
                if key.startswith('prime'):
                    if key == 'prime_cycle':continue
                    h.__dict__[key] = (mul, (nest, (fv, x), gv))
                    continue
            h.composition = '('+f.composition+'+'+g.composition+')'
            return h
        except: pass
        return self.func(x)

    @_decorators.arg_modifier(_validation.trynumber)
    @_decorators.io_opt
    def __add__(f, g):
        if f'add{g}' in f.__dict__: return f.solve_key(f'add{g}')
        if g == 0: return f
        try:
            g.__call__
        except: pass
        else:
            h = mathfunc(lambda x: f(x) + g(x))
            h.__name__ = f.__name__[0]+'p'+g.__name__[0]
            hmd = _validation.merge_dicts(f.__dict__, g.__dict__)
            for key, value_pair in hmd.items():
                fv, gv = value_pair
                if key.startswith('prime'):
                    if key == 'prime_cycle':
                        h.__dict__[key] = _math.gcd(fv, gv)
                        continue
                    h.__dict__[key] = (add, (fv, gv))
                    continue
            h.composition = '('+f.composition+'+'+g.composition+')'
            return h
        if _validation.is_numeric(g):
            h = mathfunc(lambda x: f.func(x) + g)
            h.__name__ = f.__name__[0]+'p'+str(g)[0]
            for key, value in f.__dict__.items():
                if key.startswith('prime'):
                    if key == 'prime_cycle':
                        h.__dict__[key] = value
                        continue
                    h.__dict__[key] = value
                    continue
            h.composition = '('+f.composition+'+'+str(g)
            return h
        raise TypeError('Inappropriate argument type.')

    @_decorators.arg_modifier(_validation.trynumber)
    @_decorators.io_opt
    def __radd__(f, g):
        if f'radd{g}' in f.__dict__: return f.solve_key(f'radd{g}')
        if g == 0: return f
        try:
            g.__call__
        except: pass
        else:
            h = mathfunc(lambda x: g(x)+f(x))
            h.__name__ = g.__name__[0]+'p'+f.__name__[0]
            hmd = _validation.merge_dicts(g.__dict__, f.__dict__)
            for key, value_pair in hmd.items():
                gv, fv = value_pair
                if key.startswith('prime'):
                    if key == 'prime_cycle':
                        h.__dict__[key] = _math.gcd(gv, fv)
                        continue
                    h.__dict__[key] = (add, (gv, fv))
                    continue
            h.composition = '('+g.composition+'+'+f.composition+')'
            return h
        if _validation.is_numeric(g):
            h = mathfunc(lambda x: g + f(x))
            h.__name__ = str(g)+'p'+f.__name__[0]
            for key, value in f.__dict__.items():
                if key.startswith('prime'):
                    if key == 'prime_cycle':
                        h.__dict__[key] = value
                        continue
                    h.__dict__[key] = value
                    continue
            h.composition = '('+str(g)+'+'+f.composition+')'
            return h
        raise TypeError('Inappropriate argument type.')
    
    @_decorators.arg_modifier(_validation.trynumber)
    @_decorators.io_opt
    def __sub__(f, g):
        if g == 0: return f
        if f'sub{g}' in f.__dict__: return f.solve_key(f'sub{g}')
        try:
            g.__call__
        except: pass
        else:
            h = mathfunc(lambda x: f(x) - g(x))
            h.__name__ = f.__name__[0]+'m'+g.__name__[0]
            hmd = _validation.merge_dicts(f.__dict__, g.__dict__)
            for key, value_pair in hmd.items():
                fv, gv = value_pair
                if key.startswith('prime'):
                    if key == 'prime_cycle':
                        h.__dict__[key] = _math.gcd(fv, gv)
                        continue
                    h.__dict__[key] = (sub, (fv, gv))
                    continue
            h.composition = '('+f.composition+'-'+g.composition+')'
            return h
        if _validation.is_numeric(g):
            h = mathfunc(lambda x: f(x) - g)
            h.__name__ = f.__name__[0]+'m'+str(g)[0]
            for key, value in f.__dict__.items():
                if key.startswith('prime'):
                    if key == 'prime_cycle':
                        h.__dict__[key] = value
                        continue
                    h.__dict__[key] = value
                    continue
            h.composition = '('+f.composition+'-'+str(g)+')'
            return h
        raise TypeError('Inappropriate argument type.')

    @_decorators.arg_modifier(_validation.trynumber)
    @_decorators.io_opt
    def __rsub__(f, g):
        if g == 0: return -f
        if f'rsub{g}' in f.__dict__: return f.solve_key(f'rsub{g}')
        try:
            g.__call__
        except: pass
        else:
            h = mathfunc(lambda x: g(x) - f(x))
            h.__name__ = g.__name__[0]+'m'+f.__name__[0]
            hmd = _validation.merge_dicts(g.__dict__, f.__dict__)
            for key, value_pair in hmd.items():
                gv, fv = value_pair
                if key.startswith('prime'):
                    if key == 'prime_cycle':
                        h.__dict__[key] = _math.gcd(gv, fv)
                        continue
                    h.__dict__[key] = (sub, (gv, fv))
                    continue
            h.composition = '('+g.composition+'-'+f.composition+')'
            return h
        if _validation.is_numeric(g):
            h = mathfunc(lambda x: g-f(x))
            h.__name__ = str(g)+'m'+f.__name__[0]
            for key, value in f.__dict__.items():
                if key.startswith('prime'):
                    if key == 'prime_cycle':
                        h.__dict__[key] = value
                        continue
                    h.__dict__[key] = value
                    continue
            h.composition = '('+str(g)+'-'+f.composition+')'
            return h
        raise TypeError('Inappropriate argument type.')

    
    @_decorators.arg_modifier(_validation.trynumber)
    @_decorators.io_opt
    def __mul__(f, g):
        if g == 1: return f
        if f'mul{g}' in f.__dict__: return f.solve_key(f'mul{g}')
        try:
            g.__call__
        except: pass
        else:
            h = mathfunc(lambda x: f(x) * g(x))
            h.__name__ = f.__name__[0]+'t'+g.__name__[0]
            hmd = _validation.merge_dicts(f.__dict__, g.__dict__)
            for key, value_pair in hmd.items():
                fv, gv = value_pair
                if key.startswith('prime'):
                    if key == 'prime_cycle':
                        h.__dict__[key] = _math.gcd(fv, gv)
                        continue
                    h.__dict__[key] = (add, ((mul, (fv, g)) ,(mul, (gv, f))))
                    continue
            h.composition = '('+f.composition+'*'+g.composition+')'
            return h
        if _validation.is_numeric(g):
            h = mathfunc(lambda x: f(x) * g)
            h.__name__ = f.__name__[0]+'t'+str(g)[0]
            for key, value in f.__dict__.items():
                if key.startswith('prime'):
                    if key == 'prime_cycle':
                        h.__dict__[key] = value
                        continue
                    h.__dict__[key] = (mul, (value, g))
                    continue
            h.composition = '('+f.composition+'*'+str(g)+')'
            return h
        raise TypeError('Inappropriate argument type.')

    @_decorators.arg_modifier(_validation.trynumber)
    @_decorators.io_opt
    def __rmul__(f, g):
        if g == 1: return f
        if f'rmul{g}' in f.__dict__: return f.solve_key(f'rmul{g}')
        try:
            g.__call__
        except: pass
        else:
            h = mathfunc(lambda x: g(x) * f(x))
            h.__name__ = g.__name__[0]+'t'+f.__name__[0]
            hmd = _validation.merge_dicts(g.__dict__, f.__dict__)
            for key, value_pair in hmd.items():
                gv, fv = value_pair
                if key.startswith('prime'):
                    if key == 'prime_cycle':
                        h.__dict__[key] = _math.gcd(gv, fv)
                        continue
                    h.__dict__[key] = (add, ((mul, (fv, g)) ,(mul, (gv, f))))
                    continue
            h.composition = '('+g.composition+'*'+f.composition+')'
            return h
        if _validation.is_numeric(g):
            h = mathfunc(lambda x: g * f(x))
            h.__name__ = str(g)+'t'+f.__name__[0]
            for key, value in f.__dict__.items():
                if key.startswith('prime'):
                    if key == 'prime_cycle':
                        h.__dict__[key] = value
                        continue
                    h.__dict__[key] = (rmul, (value, g))
                    continue
            h.composition = '('+str(g)+'*'+f.composition+')'
            return h
        raise TypeError('Inappropriate argument type.')

    @_decorators.arg_modifier(_validation.trynumber)
    @_decorators.io_opt
    def __truediv__(f, g):
        if g == 1: return f
        if f'div{g}' in f.__dict__: return f.solve_key(f'div{g}')
        try:
            g.__call__
        except: pass
        else:
            h = mathfunc(lambda x: f(x) / g(x))
            h.__name__ = f.__name__[0]+'o'+g.__name__[0]
            hmd = _validation.merge_dicts(f.__dict__, g.__dict__)
            for key, value_pair in hmd.items():
                fv, gv = value_pair
                if key.startswith('prime'):
                    if key == 'prime_cycle': continue
                    h.__dict__[key] = (div, (sub, (mul(g, fv), mul(f, gv))), (mul, (g, g)))
                    continue
            h.composition = '('+f.composition+'/'+g.composition+')'
            return h
        if _validation.is_numeric(g):
            h = mathfunc(lambda x: f(x) / g)
            h.__name__ = f.__name__[0]+'o'+str(g)[0]
            for key, value in f.__dict__.items():
                if key.startswith('prime'):
                    if key == 'prime_cycle':
                        h.__dict__[key] = value
                        continue
                    h.__dict__[key] = (div, (value, g))
                    continue
            h.composition = '('+f.composition+'/'+str(g)+')'
            return h
        raise TypeError('Inappropriate argument type.')

    @_decorators.arg_modifier(_validation.trynumber)
    @_decorators.io_opt
    def __rtruediv__(f, g):
        if f'rdiv{g}' in f.__dict__: return f.solve_key(f'rdiv{g}')
        try:
            g.__call__
        except: pass
        else:
            h = mathfunc(lambda x: f(x) / g(x))
            h.__name__ = g.__name__[0]+'o'+f.__name__[0]
            hmd = _validation.merge_dicts(g.__dict__, f.__dict__)
            for key, value_pair in hmd.items():
                gv, fv = value_pair
                if key.startswith('prime'):
                    if key == 'prime_cycle': continue
                    h.__dict__[key] = (div, (rsub, (mul(g, fv), mul(f, gv))), (mul, (f, f)))
                    continue
            h.composition = '('+g.composition+'/'+f.composition+')'
            return h
        if _validation.is_numeric(g):
            h = mathfunc(lambda x: f(x) / g)
            h.__name__ = str(g)+'o'+f.__name__[0]
            for key, value in f.__dict__.items():
                if key.startswith('prime'):
                    if key == 'prime_cycle':
                        h.__dict__[key] = value
                        continue
                    h.__dict__[key] = (div, (value, -(f**2)))
                    continue
            h.composition = '('+str(g)+'/'+f.composition+')'
            return h
        raise TypeError('Inappropriate argument type.')

    @_decorators.arg_modifier(_validation.trynumber)
    @_decorators.io_opt
    def __pow__(f, g):
        if g == 1: return f
        if f'pow{g}' in f.__dict__: return f.solve_key(f'pow{g}')
        try:
            g.__call__
        except: pass
        else:
            h = mathfunc(lambda x: f(x) ** g(x))
            h.__name__ = f.__name__[0]+'r'+g.__name__[0]
            hmd = _validation.merge_dicts(f.__dict__, g.__dict__)
            for key, value_pair in hmd.items():
                fv, gv = value_pair
                if key.startswith('prime'):
                    if key == 'prime_cycle':
                        h.__dict__[key] = _math.gcd(fv, gv)
                        continue
                    h.__dict__[key] = (mul, (h, (add, ((mul, (ln(f), gv)),(mul, ((div, (fv, f)), g))))))
                    continue
            h.composition = '('+f.composition+'**'+g.composition+')'
            return h
        if _validation.is_numeric(g):
            h = mathfunc(lambda x: f(x) ** g)
            h.__name__ = f.__name__[0]+'r'+str(g)[0]
            for key, value in f.__dict__.items():
                if key.startswith('prime'):
                    if key == 'prime_cycle':
                        h.__dict__[key] = value
                        continue
                    h.__dict__[key] = (mul, ((mul, (g, pow(f, g-1)), (value))))
                    continue
            h.composition = '('+f.composition+'**'+str(g)+')'
            return h
        raise TypeError('Inappropriate argument type.')

    @_decorators.arg_modifier(_validation.trynumber)
    @_decorators.io_opt
    def __rpow__(f, g):
        if f'rpow{g}' in f.__dict__: return f.solve_key(f'rpow{g}')
        try:
            g.__call__
        except: pass
        else:
            h = mathfunc(lambda x: f(x) ** g(x))
            h.__name__ = g.__name__[0]+'r'+f.__name__[0]
            hmd = _validation.merge_dicts(g.__dict__, f.__dict__)
            for key, value_pair in hmd.items():
                gv, fv = value_pair
                if key.startswith('prime'):
                    if key == 'prime_cycle': continue
                    h.__dict__[key] = (mul, (add, ((mul, (ln(g), fv)),(mul, (div, (gv, g)), f))))
                    continue
            h.composition = '('+g.composition+'**'+f.composition+')'
            return h
        if _validation.is_numeric(g):
            h = mathfunc(lambda x: f(x) + g)
            h.__name__ = str(g)+'o'+f.__name__[0]
            for key, value in f.__dict__.items():
                if key.startswith('prime'):
                    if key == 'prime_cycle': continue
                    h.__dict__[key] = (mul, (mul, (h, ln(g)), value))
                    continue
            h.composition = '('+str(g)+'**'+f.composition+')'
            return h
        raise TypeError('Inappropriate argument type.')

    @_decorators.arg_modifier(_validation.trynumber)
    @_decorators.io_opt
    def __neg__(f):
        if 'negative' in f.__dict__: return f.__dict__['negative']
        h = mathfunc(lambda x: -(f(x)), negative=f)
        for key, value in f.__dict__.items():
            if key.startswith('prime'):
                if key == 'prime_cycle':
                    h.__dict__[key] = value
                    continue
                h.__dict__[key] = (sub, (0, value))
                continue
        h.__name__=f'neg_{f.__name__}'
        h.composition = '-'+f.composition
        return h

    def __pos__(f):
        return f

    @_decorators.arg_modifier(_validation.trynumber)
    @_decorators.io_opt
    def __abs__(f):
        return mathfunc(lambda x: abs(f(x)))

    @staticmethod
    @_decorators.io_opt
    @_decorators.debug
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

    @_decorators.debug
    def solve_key(self, key):
        self.__dict__[key] = self.resolve_tuple_key(self.__dict__[key])
        return self.__dict__[key]

    @_decorators.arg_modifier(_validation.trynumber)
    @_decorators.io_opt
    def derivative(f, kth=1):
        '''find the kth derivative of f'''
        if 'prime_cycle' in f.__dict__: kth = kth%f.prime_cycle
        if f'prime{kth}' in f.__dict__: return f.solve_key(f'prime{kth}')
        assert _validation.is_integer(kth)
        assert kth >= 0
        
        if kth == 0: return f
        if kth == 1:
            return mathfunc(lambda x: ((f(x+dx)-f(x))/dx))
        return f.derivative(kth-1).derivative()

dx = 1e-14

add = lambda x, y: x+y
radd = lambda x, y: y+x
sub = lambda x, y: x-y
rsub = lambda x, y: y-x
mul = lambda x, y: x*y
rmul = lambda x, y: y*x
div = lambda x, y: x/y
rdiv = lambda x, y: y/x
rpow = lambda x, y: y**x
nest = lambda x, y: x(y)

@_decorators.io_opt
def mathfunc_with_extras(**extras):
    @_decorators.io_opt
    def mathfunc_dec(func): return mathfunc(func, **extras)
    return mathfunc_dec

def pm(a, b):
    '''Return a ± b'''
    return tuple((a+b, a-b))

@mathfunc
def identity(x):
    return x
identity.composition = 'x'

identity.prime1 = 1

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
        return  f'<nmath.trig_func {self.__name__} at {hex(id(self))}>'

@_decorators.io_opt
def trig_func_with_extras(**extras):
    @_decorators.io_opt
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
        return  f'<nmath.inverse_trig_func {self.__name__} at {hex(id(self))}>'

@_decorators.io_opt
def inverse_trig_func_with_extras(**extras):
    @_decorators.io_opt
    def inverse_trig_func_dec(func): return inverse_trig_func(func, **extras)
    return inverse_trig_func_dec

def get_angle():
    return _angle

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
cos.prime_cycle = 4

sin.prime1=cos
sin.prime2=-sin
sin.prime3=-cos
sin.prime_cycle = 4

(-sin).prime1=-cos
(-sin).prime2=sin
(-sin).prime3=cos
(-sin).prime_cycle = 4

(-cos).prime1=sin
(-cos).prime2=cos
(-cos).prime3=-sin
(-cos).prime_cycle = 4

tan.prime1 = sec**2
sec.prime1 = sec*tan
cot.prime1 = -(csc**2)
csc.prime1 = -csc*cot



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
