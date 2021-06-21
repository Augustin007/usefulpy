'''
nmath or 'new math'

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
3
 3.0
  Version 3.0.0
   Downsized, most of its ability has been moved over to 'mathfunc.py'.
   Functionality from PrimeComposite 0.0.0 and triangles 0.1.0 has been moved
   here
'''


### DUNDERS ###
__version__ ='3.0.0'
__author__ = 'Augustin Garcia'

##TEMP
__package__ = 'usefulpy.mathematics'


### IMPORTS ###
from .mathfuncs import *
from functools import reduce as _reduce
import math as _math
import cmath as _cmath

from math import comb, copysign, erf, erfc, fabs, factorial, fmod, fsum, gamma
from math import lgamma, modf, nextafter, perm, prod, remainder, trunc, ulp

### checks ###

def odd(num, /):
    '''Return True if num is odd'''
    try: return num%2 == 1
    except: return False

def even(num, /):
    '''Return True if num is even'''
    try: return num%2 == 0
    except: return False

def persistance(n):
    if n >= 10: 
        yield n
        yield from persistance(prod([int(i) for i in str(n)]))
    else: yield n

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
    try: return x.isinf()
    except: pass
    raise TypeError(f'invalid type, type {type(x).__name__}')

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
    try: return x.isnan()
    except: pass
    raise TypeError(f'invalid type, type {type(x).__name__}')

def isfinite(x, /):
    try: return _math.isfinite(x)
    except: pass
    try: return _cmath.isfinite(x)
    except: pass
    try: return x.isfinite()
    except: pass
    try: return not (isnan(x) or isinf(x))
    except: pass    
    raise TypeError(f'invalid type, type {type(x).__name__}')


### MISCILLANEOUS ###
def summation(start, finish, function = lambda x: x):
    '''Σ'''
    return sum(map(function, range(start, finish+1)))
    rangelist = list(range(start, finish+1))
    rangelist[0] = function(rangelist[0])
    return _reduce((lambda x, y: x+function(y)), rangelist)

def product(start, finish, function = lambda x:x):
    '''∏'''
    return prod(map(function, range(start, finish+1)))

def _taylor_summation(function):
    try:
        # This is not true infinite summation, but it does give an
        # approximation, (this does mean that it can be stuck in an infinite
        # loop... not yet sure how to counter this accurately and efficiently.
        # but eventually a number gets to big or to small for python to handle
        prev = 10
        prev1 = 10
        prev2 = 10
        start = 0
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
    assert type(nth) is int
    
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
    assert type(nth) is int
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

def phase(z, /):
    '''Return angle of number'''
    try: z = complex(z)
    except:
        try: z = complex(float(z))
        except: pass
    try: return (_cmath.phase(z), 1j)        
    except: pass
    try: return z.__phase__()
    except:pass
    raise TypeError('%s has no phase' % type(z))

def polar(z, /):
    '''Return a number in polar form'''
    try:z = complex(z)
    except:
        try: z = complex(float(z))
        except: pass
    try: return (_cmath.polar(z), 1j)
    except: pass
    try: return z.__polar__()
    except:pass
    raise TypeError('%s has no polar' % type(z))

def rect(r, phi, n = 1j):
    '''Create complex back from polar form'''
    return r*(cos(phi) + n*sin(phi))

class t: #taylor series
    def cos(theta, /):
        '''taylor series for cos.'''
        def iteration(n):
            trueiter = 2*n
            sign = (-1)**n
            denom = factorial(trueiter)
            return sign * (theta**trueiter)/denom
        return _taylor_summation(iteration)

    def sin(theta, /):
        '''taylor series for sin.'''
        def iteration(n):
            trueiter = 2*n+1
            sign = (-1)**n
            denom = factorial(trueiter)
            return sign * (theta**trueiter)/denom
        return _taylor_summation(iteration)

    def tan(theta, /):
        ##TODO: Add Taylor Series for tan
        return t.sin(theta)/t.cos(theta) 

    def exp(num):
        def iteration(x): 
            if x == 0: return 1
            if x == 1: return num
            return (num**x)/factorial(x)
        return _taylor_summation(iteration)

    def ln(x):
        '''taylor series for ln. Only works for real numbers. A complex number
will return an incorrect value.'''
        if x == 0: raise ValueError('math domain error')
        if x == 1: return 0
        if x == 2: return 0.6931471805599453
        if abs(x) >=2: return 0.6931471805599453+t.ln(x/2)
        def iteration(n):
            if n == 0: return 0
            return -((x**n)/n)
        x = 1-x
        return _taylor_summation(iteration)

_primes = [2]
_composites = []
def PrimeOrComposite(num):
    '''return 'prime' if prime and 'composite' if composite'''
    Prime = 'prime'
    Composite = 'composite'
    if not isinstance(num, int): raise TypeError
    num = int(num)
    if num < 1: raise TypeError
    if num == 1: return 'neither'
    def upuntil(number):
        for x in range(largestPrime + 1, number + 1):
            PoC=PrimeOrComposite(x)
            if PoC == Prime: _primes.append(x)
            else: _composites.append(x)
    primes = _primes
    if num in primes: return Prime
    if num in _composites: return Composite
    largestPrime = primes[-1]
    if largestPrime**2 < num: upuntil(isqrt(num))
    for x in primes:
        if num%x == 0:
            return Composite
        if x**2>num:
            return Prime
    return Prime

def Prime(num):
    '''return True if number is prime'''
    try: return PrimeOrComposite(num) == 'prime'
    except: return False

def Composite(num):
    '''return True if number is composite'''
    try: return PrimeOrComposite(num) == 'composite'
    except: return False

def factor(num):
    '''return factors of a number'''
    if num == 1: return [1]
    PrimeOrComposite((num//2)**2)
    num = int(num)
    factors = []
    while not Prime(num):
        for prime in _primes:
            if num%prime == 0:
                factors.append(prime)
                num = num//prime
                break
    factors.append(num)
    return factors

def lcm(a, b):
    '''Return least common multiple of a and b'''
    ngcd = gcd(a, b)
    a, b = a//ngcd, b//ngcd
    return a*b*ngcd

def _gcd(a, b):
    a, b = sorted((a, b), reverse = True)
    while b != 0:
        a, b = b, a%b
    return a

def _get_gcd(a, b):
    if hasattr(a, '__gcd__'):
        return a.__gcd__(b)
    if hasattr(b, '__gcd__'):
        return b.__gcd__(a)
    return _gcd(a, b)

def gcd(*args):
    return _reduce(_get_gcd, args)

def lmgm(n, m):
    '''Return the smallest multiple of n greater than or equal to m'''
    assert n>0
    assert m>=0
    return m + ((n - (m % n)) % n)

### CHECKS ###
def isTriangle(a, b, c):
    '''Check if values can form a real triangle.'''
    a, b, c = abs(a), abs(b), abs(c)
    return not (a+b <= c or a+c <= b or b+c <= a or (0 in (a, b, c)))
equilateral = 'equilateral'
isosceles = 'isosceles'
scalene = 'scalene'

def TriangleType(a, b, c):
    '''Return type of triangle.'''
    if not isTriangle(a, b, c):
        raise ValueError('A valid triagle cannot be made from %s, %s, and %s' % (a, b, c))
    if _math.isclose(a, b, rel_tol = 0, abs_tol = 1e-14):
        if _math.isclose(a, c, rel_tol = 0, abs_tol = 1e-14): return equilateral
        return isosceles
    if _math.isclose(a, c, rel_tol = 0, abs_tol = 1e-14):return isosceles
    if _math.isclose(b, c, rel_tol = 0, abs_tol = 1e-14):return isosceles
    return scalene
obtuse = 'obtuse'
acute = 'acute'
right = 'right'
straight = 'straight'
circle = 'circle'

def AngleType(measure):
    '''Check whether an angle measure is acute, obtuse, or right angle.'''
    measure = abs(measure)
    measure = measure%_math.tau
    if measure > _math.pi: measure = _math.tau-measure
    if measure == 0: return circle
    if measure < _math.pi/2: return acute
    if measure == _math.pi/2: return right
    if measure == _math.pi: return straight
    return obtuse


### MATH ###
def LawofCos(a, b, *, c = None, gamma = None):
    '''Return the appropriate value of either gamma or c, using law of
Cosine, one or the other must be given, not both'''
    if gamma == None and c == None:
        raise TypeError('Either c or gamma must be defined')
    if gamma != None and c != None:
        raise TypeError('c and gamma cannot both be defined')
    if gamma == None:
        pyth = (a**2)+(b**2)-(c**2)
        anglecos = (pyth)/(2*a*b); Angle = _math.acos(anglecos)
        return Angle
    pyth = (a**2)+(b**2); anglecos = _math.cos(gamma)
    c = _math.sqrt(pyth - (2*a*b*anglecos))
    return c

def LawofSin(alpha, a, *, beta = None, b = None):
    '''Return the appropiate value of either beta or b, using law of Sines,
one or the other must be given, not both'''
    if beta == None and b == None:
        raise TypeError('Either b or beta must be defined')
    if beta != None and b != None:
        raise TypeError('b and beta cannot both be defined')
    if beta == None: ratio = _math.sin(alpha)/a; beta = _math.asin(ratio*b); return beta
    ratio = a/_math.sin(alpha); b = ratio*_math.sin(beta); return b

def Heron(a, b, c):
    '''Use heron's formula to find the area of a triangle'''
    s = (a+b+c)/2; Area = _math.sqrt(s*(s-a)*(s-b)*(s-c))
    return Area


### TRIANGLE ###
class triangle(object):
    def __init__(self, *, a=None, b=None, c=None, alpha=None, beta=None, gamma=None):
        kwval = {}
        argnames =('a', 'b', 'c', 'alpha', 'beta', 'gamma')
        argvalues = (a, b, c, alpha, beta, gamma)
        for name, value in zip(argnames, argvalues):
            if value:
                kwval[name] = value
        if len(kwval) != 3:
            raise TypeError('Exactly three values must be defined')
        if all(map(lambda x: not x, (a, b, c))):
            raise TypeError('At least one side must be defined')
        if all((a, b, c)):
            if not isTriangle(a, b, c):
                raise ValueError('A valid triagle cannot be made from %s, %s, and %s' % (a, b, c))
            kwval['gamma'] = gamma =  LawofCos(a, b, c = c)
            kwval['beta'] = beta = LawofCos(a, c, c = b)
            kwval['alpha'] = _math.pi-beta-gamma
            self.__dict__ = kwval
            self.compute()
            return
        if len(tuple(filter(bool, (a, b, c)))) == 2:
            wr_args = ValueError('More than one valid triangle can be made from given arguments')
            if not a:
                if alpha:
                    kwval['a'] = a = LawofCos(b, c, gamma = alpha)
                    kwval['beta'] = beta = LawofSin(alpha, a, b=b)
                    kwval['gamma'] = _math.pi-beta-alpha
                    self.__dict__ = kwval
                    self.compute()
                    return
                raise wr_args
            if not b:
                if beta:
                    kwval['b'] = b = LawofCos(a, c, gamma = beta)
                    kwval['alpha'] = alpha = LawofSin(beta, b, b=a)
                    kwval['gamma'] = _math.pi-beta-alpha
                    self.__dict__ = kwval
                    self.compute()
                    return
                raise wr_args
            if gamma:
                kwval['c'] = c = LawofCos(a, b, gamma = gamma)
                kwval['alpha'] = alpha = LawofSin(gamma, c, b=a)
                kwval['beta'] = _math.pi-gamma-alpha
                self.__dict__ = kwval
                self.compute()
                return
            raise wr_args
        if not alpha: kwval['alpha'] = alpha = _math.pi-gamma-beta
        elif not beta: kwval['beta'] = beta = _math.pi-alpha-beta
        else: kwval['gamma'] = gamma = _math.pi-beta-alpha

        if a:
            kwval['b'] = LawofSin(alpha, a, beta = beta)
            kwval['c'] = LawofSin(alpha, a, beta = gamma)
            self.__dict__ = kwval
            self.compute()
            return
        if b:
            kwval['a'] = LawofSin(beta, b, beta = alpha)
            kwval['c'] = LawofSin(beta, b, beta = gamma)
            self.__dict__ = kwval
            self.compute()
            return
        kwval['a'] = LawofSin(gamma, c, beta = alpha)
        kwval['b'] = LawofSin(gamma, c, beta = beta)
        self.__dict__ = kwval
        self.compute()
        return

    def compute(self):
        if hasattr(self, 'type'): return
        self.area = Heron(self.a, self.b, self.c)
        self.angletype = AngleType(max(self.alpha, self.beta, self.gamma))
        self.perimeter = self.a+self.b+self.c
        self.type = TriangleType(self.a, self.b, self.c)

    def __repr__(self):
        return f'triangle(a={self.a}, b={self.b}, c={self.c})'

#eof
