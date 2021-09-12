'''
nmath or 'new math'

Access to basic mathematical functions

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
  Version 3.0.1
   Improve functionality
   Bugfixes
   Documentation
   Prime sieve implementation
'''

__version__ ='3.0.0'
__author__ = 'Augustin Garcia'

from itertools import repeat as _repeat
from functools import reduce as _reduce
import math as _math
import cmath as _cmath
import types

from math import comb, copysign, erf, erfc, fabs, factorial, fmod, fsum, gamma, lgamma
from math import modf, nextafter, perm, prod, remainder, trunc, ulp, ldexp, frexp

### simple checks with failsafe ###
def odd(n:int, /) -> bool:
    '''Return True if num is odd'''
    try: return n%2 == 1
    except: return False

def even(n:int, /) -> bool:
    '''Return True if num is even'''
    try: return n%2 == 0
    except: return False

def isclose(a, b, *, rel_tol=1e-09, abs_tol=0.0) -> bool:
    '''Return True if a is close to b'''
    # Always try optimized c methods first
    try: return _math.isclose(a, b) 
    except: pass
    try: return _cmath.isclose(a, b)
    except: pass

    # If these fail
    # case checks
    if isnan(a) or isnan(b): return False
    if isinf(a) or isinf(b): return a == b

    # find tolerance for 'closeness' and the distance between the values
    tol, difference = max((abs(abs(b)*rel_tol)), abs(abs_tol)), abs(a-b)
    
    return tol >= difference

def isinf(x, /):
    '''Return True if x is inf in any direction'''
    # C methods
    try: return _math.isinf(x)
    except: pass
    try: return _cmath.isinf(x)
    except: pass

    #if these fail

    # allow for customized types
    try: return x.isinf()
    except: pass

    #otherwise
    raise TypeError(f'invalid type, type {type(x).__name__}')

def isnan(x, /):
    '''Return True if x is nan in any way'''
    # C methods
    try: return _math.isnan(x)
    except: pass
    try: return _cmath.isnan(x)
    except: pass

    # allow for customized types
    try: return x.isnan()
    except: pass
    raise TypeError(f'invalid type, type {type(x).__name__}')

def isfinite(x, /):
    '''Return True if x is neither an infinity nor a NaN, and False otherwise'''
    try: return _math.isfinite(x)
    except: pass
    try: return _cmath.isfinite(x)
    except: pass

    # allow for customized types
    try: return x.isfinite()
    except: pass
    try: return not (isnan(x) or isinf(x))
    except: pass
    raise TypeError(f'invalid type, type {type(x).__name__}')



### persistance ###

def _persistance_generator(n:int, /):
    '''Generates numbers of product of digits in n'''
    if n >= 10: 
        yield n
        #recursive call with digit prod of itself until
        #the number is less than ten
        # is called by `persistance_generator` which does a type check first.
        yield from _persistance_generator(prod([int(i) for i in str(n)]))
        
    else: yield n

def persistance_generator(n:int, /):
    '''Generate numbers of product of digits in n'''
    # uses _persitance_generator but checks type first
    if type(n) is not int:
        raise TypeError(f'Invalid type, type {type(n).__name__}')
    return _persistance_generator(n)

def persistance(n:int, /):
    '''Find persistance of number n'''
    if type(n) is not int:
        raise TypeError(f'Invalid type, type {type(n).__name__}')
    return len(tuple(_persistance_generator(n)))


### Sum and prod ###
def digit_prod(n:int, /):
    '''Return the product of the digits of n'''
    if type(n) is not int:
        raise TypeError(f'Invalid type, type {type(n).__name__}')
    return prod([int(i) for i in str(n)])

def digit_sum(n:int, /):
    '''Return the sum of the digits of n'''
    if type(n) is not int:
        raise TypeError(f'Invalid type, type {type(n).__name__}')
    return sum([int(i) for i in str(n)])

def summation(start:int, finish:int, function = lambda x: x):
    '''Σ'''
    return sum(map(function, range(start, finish+1)))

def product(start:int, finish:int, function = lambda x:x):
    '''∏'''
    return prod(map(function, range(start, finish+1)))

#
def _taylor_summation(function):
    try:
        # Not up to date.
        # 
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


# Dist and hypot

def dist(p, q, /):
    '''returns the distance between the coordinates of iterables p and q'''
    #begins by making padding with 0s if p and q are different length
    if len(p) != len(q):
        p, q = list(max(p, q, key = len)), list(min(p, q, key = len))
        q[len(q):]=[0]*(len(p)-len(q))

    #trys compiled method
    try: return _math.dist(p, q)
    except: pass

    #otherwise does slow method
    args = [x-y for x, y in zip(p, q)]
    return hypot(*args)

def hypot(*coordinates):
    '''returns the distance between origin and the point with given coordinates'''
    try: return _math.hypot(*coordinates)
    except: return _math.sqrt(sum(map(lambda x:x**2, coordinates)))

# Powers and exponents
def rt(nth:int, of):
    '''Find the nth root of (n must be an integer).

Programatically approximates nth root of n as an
alternate method to built in systems in for the sake of
a custom class'''
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

def phase(z, /):
    '''Return angle of number'''
    try: z = complex(z)
    except:
        try: z = complex(float(z))
        except: pass
    #Attempting to make sure z will be a complex
    
    try: return (_cmath.phase(z), 1j)        
    except: pass

    # In case of custom class
    try: return z.__phase__()
    except:pass
    
    raise TypeError('%s has no phase' % type(z).__name__)

def polar(z, /):
    '''Return a number in polar form'''
    try:z = complex(z)
    except:
        try: z = complex(float(z))
        except: pass
    #Attempting to make sure z will be a complex
    
    try: return (_cmath.polar(z), 1j)
    except: pass

    #allowing for custom class
    try: return z.__polar__()
    except:pass
    raise TypeError('%s has no polar' % type(z))

def rect(r, phi, n = 1j):
    '''Create complex back from polar form'''
    return r*(_math.cos(phi) + n*_math.sin(phi))

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


def _lcm_ngem(n:int, m:int)->int:
    return m+((n-(m%n)) %n)

class segmented_sieve:
    primes:list[int] = [2, 3, 5, 7]
    end_segment: int = 1
    searched_till: int=8
    

    @staticmethod
    def extend() -> None:
        k = segmented_sieve.end_segment
        add = 1
        p = segmented_sieve.primes[k]
        while 2*p*add+add**2 < 1000 and k+add+1<len(segmented_sieve.primes): add += 1
        p, q = segmented_sieve.primes[k], segmented_sieve.primes[k+add]
        segment = range(p*p, q*q)
        segment_min = min(segment)
        segment_len = len(segment)
        is_prime = [True]*segment_len
        for i in range(k+add):
            pk = segmented_sieve.primes[i]
            start = _lcm_ngem(pk, segment_min)
            is_prime[start-segment_min::pk] = _repeat(False, len(range(start-segment_min, segment_len, pk)))
        segmented_sieve.primes.extend([a for a, b in zip(segment, is_prime) if b])
        segmented_sieve.end_segment += add
        segmented_sieve.searched_till =segmented_sieve.primes[k+add]**2-1

    @staticmethod
    def is_prime(n:int) -> bool:
        for l in segmented_sieve.Primes_till(_math.isqrt(n)+1):
            if n%l == 0: return False
        return True

    @staticmethod
    def is_composite(n:int)->bool:
        for l in segmented_sieve.Primes_till(_math.isqrt(n)+1):
            if n%l == 0: return True
        return False

    @staticmethod
    def Primes_till(n:int)->types.GeneratorType:
        while n >=segmented_sieve.searched_till:
            segmented_sieve.extend()
        for p in segmented_sieve.primes:
            if p >=n:return
            yield p
    

sieve = segmented_sieve()
def Prime(n):
    if type(n) is not int:
        raise TypeError('n must be an int')
    if n<0:
        raise ValueError('Only natural numbers can have properties as Prime or Composite')
    return sieve.is_prime(n)

def Composite(n):
    if type(n) is not int:
        raise TypeError('n must be an int')
    if n<0:
        raise ValueError('Only natural numbers can have properties as Prime or Composite')
    return sieve.is_composite(n)

def primes_till(n:int)->tuple[int]:
    return tuple(sieve.Primes_till(n))

def _factor_sub(n):
    if not ((type(n) is int) and (n >= 0)):
        raise ValueError('Only natural numbers can have properties as Prime or Composite')    
    if n in (0, 1):
        yield n; return
    if Prime(n):
        yield n; return [n]
    
    for p in sieve.primes:
        while n%p==0:
            yield p
            n//=p
        if p>_math.sqrt(n):
            break
    if n not in (0, 1):
        yield n

def Factor(n):
    return tuple(_factor_sub(n))

def _lcm1(a, b):
    ngcd = gcd(a, b)
    a, b = a//ngcd, b//ngcd

def lcm(*integers):
    '''Return least common multiple of a and b'''
    try:_math.lcm(*integers)
    except:pass
    return _reduce(_lcm1, integers)

def _get_gcd(n):
    if type(n) is complex:
        return _math.gcd(n.real, n.imag)
    try: return n.gcd()
    except: pass
    return n

def gcd(*integers):
    return _math.gcd(map(_get_gcd, integers))


### Triangle checks ###
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
