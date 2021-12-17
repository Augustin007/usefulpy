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
  Version 3.0.2
   Prime sieve bugfixes
   Faster prime sieve
'''

__version__ = '3.0.0'
__author__ = 'Augustin Garcia'
if __name__ == '__main__':
    __package__ = 'usefulpy.mathematics'


from itertools import repeat as _repeat, compress as _compress
from functools import reduce as _reduce
import math as _math
import cmath as _cmath
from math import factorial, prod


# simple checks with failsafe
def odd(n: int, /) -> bool:
    '''Return True if num is odd'''
    try:
        return n % 2 == 1
    except Exception:
        return False


def even(n: int, /) -> bool:
    '''Return True if num is even'''
    try:
        return n % 2 == 0
    except Exception:
        return False


def isclose(a, b, *, rel_tol=1e-09, abs_tol=0.0) -> bool:
    '''Return True if a is close to b'''
    # Always try optimized c methods first
    try:
        return _math.isclose(a, b)
    except Exception:
        pass
    try:
        return _cmath.isclose(a, b)
    except Exception:
        pass

    # If these fail
    # case checks
    if isnan(a) or isnan(b):
        return False
    if isinf(a) or isinf(b):
        return bool(a == b)

    # find tolerance for 'closeness' and the distance between the values
    tol, difference = max((abs(abs(b)*rel_tol)), abs(abs_tol)), abs(a-b)

    return bool(tol >= difference)


def isinf(x, /) -> bool:
    '''Return True if x is inf in any direction'''
    # C methods
    try:
        return _math.isinf(x)
    except Exception:
        pass
    try:
        return _cmath.isinf(x)
    except Exception:
        pass

    # if these fail

    # allow for customized types
    try:
        return bool(x.isinf())
    except Exception:
        pass

    # otherwise
    raise TypeError(f'invalid type, type {type(x).__name__}')


def isnan(x, /) -> bool:
    '''Return True if x is nan in any way'''
    # C methods
    try:
        return _math.isnan(x)
    except Exception:
        pass
    try:
        return _cmath.isnan(x)
    except Exception:
        pass

    # allow for customized types
    try:
        return bool(x.isnan())
    except Exception:
        pass
    raise TypeError(f'invalid type, type {type(x).__name__}')


def isfinite(x, /):
    '''Return True if x is neither an infinity nor a NaN and False otherwise'''
    try:
        return _math.isfinite(x)
    except Exception:
        pass
    try:
        return _cmath.isfinite(x)
    except Exception:
        pass

    # allow for customized types
    try:
        return x.isfinite()
    except Exception:
        pass
    try:
        return not (isnan(x) or isinf(x))
    except Exception:
        pass
    raise TypeError(f'invalid type, type {type(x).__name__}')


def _persistance_generator(n: int, /):
    '''Generates numbers of product of digits in n'''
    if n >= 10:
        yield n
        # recursive call with digit prod of itself until
        # the number is less than ten
        # is called by `persistance_generator` which does a type check first.
        yield from _persistance_generator(prod([int(i) for i in str(n)]))

    else:
        yield n


def persistance_generator(n: int, /):
    '''Generate numbers of product of digits in n'''
    # uses _persitance_generator but checks type first
    if type(n) is not int:
        raise TypeError(f'Invalid type, type {type(n).__name__}')
    return _persistance_generator(n)


def persistance(n: int, /):
    '''Find persistance of number n'''
    if type(n) is not int:
        raise TypeError(f'Invalid type, type {type(n).__name__}')
    return len(tuple(_persistance_generator(n)))


# Sum and prod #
def digit_prod(n: int, /):
    '''Return the product of the digits of n'''
    if type(n) is not int:
        raise TypeError(f'Invalid type, type {type(n).__name__}')
    return prod([int(i) for i in str(n)])


def digit_sum(n: int, /):
    '''Return the sum of the digits of n'''
    if type(n) is not int:
        raise TypeError(f'Invalid type, type {type(n).__name__}')
    return sum([int(i) for i in str(n)])


def summation(start: int, finish: int, function=lambda x: x):
    '''Σ'''
    return sum(map(function, range(start, finish+1)))


def product(start: int, finish: int, function=lambda x: x):
    '''∏'''
    return prod(map(function, range(start, finish+1)))


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
        check = lambda x:  abs(x) < 1e-25
        while not all(map(check, (change, prev, prev1, prev2))):
            start += 1
            try:
                sm += change
                prev2 = prev1
                prev1 = prev
                prev = change
                change = function(start)
            except Exception:
                return sm
        return sm
    except Exception:
        return sm


# Dist and hypot
def dist(p, q, /):
    '''returns the distance between the coordinates of iterables p and q'''
    # begins by making padding with 0s if p and q are different length
    if len(p) != len(q):
        p, q = list(max(p, q, key=len)), list(min(p, q, key=len))
        q[len(q):] = [0]*(len(p)-len(q))

    # trys compiled method
    try:
        return _math.dist(p, q)
    except Exception:
        pass

    # otherwise does slow method
    args = [x-y for x, y in zip(p, q)]
    return hypot(*args)


def hypot(*coordinates):
    '''returns the distance between origin and the point with
given coordinates'''
    try:
        return _math.hypot(*coordinates)
    except Exception:
        return _math.sqrt(sum(map(lambda x: x**2, coordinates)))


# Powers and exponents
def rt(nth: int, of):
    '''Find the nth root of (n must be an integer).

Programatically approximates nth root of n as an
alternate method to built in systems in for the sake of
a custom class'''
    assert type(nth) is int

    try:
        is_negative = of < 0
    except Exception:
        is_negative = False

    if is_negative:
        of, final = -of, 1j
    else:
        final = 1
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
    try:
        z = complex(z)
    except Exception:
        try:
            z = complex(float(z))
        except Exception:
            pass
    # Attempting to make sure z will be a complex

    try:
        return (_cmath.phase(z), 1j)
    except Exception:
        pass

    # In case of custom class
    try:
        return z.__phase__()
    except Exception:
        pass

    raise TypeError('%s has no phase' % type(z).__name__)


def polar(z, /):
    '''Return a number in polar form'''
    try:
        z = complex(z)
    except Exception:
        try:
            z = complex(float(z))
        except Exception:
            pass
    # Attempting to make sure z will be a complex

    try:
        return (_cmath.polar(z), 1j)
    except Exception:
        pass

    # allowing for custom class
    try:
        return z.__polar__()
    except Exception:
        pass
    raise TypeError('%s has no polar' % type(z))


def rect(r, phi, n=1j):
    '''Create complex back from polar form'''
    return r*(_math.cos(phi) + n*_math.sin(phi))


class t:  # taylor series
    def cos(theta, /):
        '''taylor series for cos.'''
        def iteration(n):
            trueiter = 2*n
            sign = (-1)**n
            denom = factorial(trueiter)
            return sign*(theta**trueiter)/denom
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
        # TODO:  Add Taylor Series for tan
        return t.sin(theta)/t.cos(theta)

    def exp(num):
        def iteration(x):
            if x == 0:
                return 1
            if x == 1:
                return num
            return (num**x)/factorial(x)
        return _taylor_summation(iteration)

    def ln(x):
        '''taylor series for ln. Only works for real numbers. A complex number
will return an incorrect value.'''
        if x == 0:
            raise ValueError('math domain error')
        if x == 1:
            return 0
        if x == 2:
            return 0.6931471805599453
        if abs(x) >= 2:
            return 0.6931471805599453+t.ln(x/2)

        def iteration(n):
            if n == 0:
                return 0
            return -((x**n)/n)

        x = 1-x
        return _taylor_summation(iteration)


def _lcm_ngem(n: int, m: int) -> int:
    return m + ((n - (m % n)) % n)


def _custom_bin_search(sorted_, i):
    low = 0
    high = len(sorted_)-1
    mid = 0

    while low <= high:
        mid = (high + low) // 2
        if sorted_[mid] == i:
            return mid
        elif sorted_[mid] < i:
            low = mid + 1
        else:
            high = mid - 1
    return mid


class segmented_sieve:
    primes: list[int] = [2, 3, 5, 7]
    end_segment: int = 1
    searched_till: int = 8

    @staticmethod
    def extend() -> None:
        k = segmented_sieve.end_segment
        add = 1
        p = segmented_sieve.primes[k]
        length = len(segmented_sieve.primes)
        while 2*p*add+add**2 < 1000 and k+add+1 < length:
            add += 1
        p, q = segmented_sieve.primes[k], segmented_sieve.primes[k+add]
        segment_min = p*p
        segment_len = q*q-segment_min
        is_prime = [True]*segment_len
        for pk in segmented_sieve.primes[: k+add]:
            start = _lcm_ngem(pk, segment_min)
            prime_count = _math.ceil((segment_len-(start-segment_min))/pk)
            is_prime[start-segment_min:: pk] = _repeat(False, prime_count)
        segmented_sieve.primes.extend(_compress(
            range(segment_min, q*q), is_prime))
        segmented_sieve.end_segment += add
        segmented_sieve.searched_till = segmented_sieve.primes[k+add]**2-1

    @staticmethod
    def is_prime(n: int) -> bool:
        if n <= segmented_sieve.searched_till:
            return n in segmented_sieve.primes
        for test_number in segmented_sieve.Primes_till(_math.isqrt(n)+1):
            if n % test_number == 0:
                return False
        return True

    @staticmethod
    def is_composite(n: int) -> bool:
        if n <= segmented_sieve.searched_till:
            return n not in segmented_sieve.primes
        for test_number in segmented_sieve.Primes_till(_math.isqrt(n)+1):
            if n % test_number == 0:
                return True
        return False

    @staticmethod
    def Primes_till(n: int) -> list[int]:
        while n >= segmented_sieve.searched_till:
            segmented_sieve.extend()

        index = _custom_bin_search(segmented_sieve.primes, n)
        if segmented_sieve.primes[index] > n:
            index -= 1
        return segmented_sieve.primes[: index+1]


sieve = segmented_sieve()


def _Prime_test(n):
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    d = (n-1)//2

    r = 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for a in sieve.Primes_till(min(n-2, _math.floor(2*_math.log(n)**2))):
        x = pow(a, d, n)
        if x in (1, n-1):
            continue
        for t in range(r):
            x = pow(x, 2, n)
            if x in (1, n-1):
                break
        else:
            return False
    return True


def Prime(n):
    if type(n) is not int:
        raise TypeError('n must be an int')
    if n < 0:
        raise ValueError('Only natural numbers can be Prime or Composite')
    return _Prime_test(n)


def Composite(n):
    if type(n) is not int:
        raise TypeError('n must be an int')
    if n < 0:
        raise ValueError('Only natural numbers can be Prime or Composite')
    return not _Prime_test(n)


def primes_till(n: int):
    return tuple(sieve.Primes_till(n))


def _factor_sub(n):
    if not ((type(n) is int) and (n >= 0)):
        raise ValueError('Only natural numbers can be Prime or Composite')
    if n in (0, 1):
        yield n
        return
    if Prime(n):
        yield n
        return [n]

    for p in sieve.primes:
        while n % p == 0:
            yield p
            n //= p
        if p > _math.sqrt(n):
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
    try:
        _math.lcm(*integers)
    except Exception:
        pass
    return _reduce(_lcm1, integers)


def _get_gcd(n):
    if type(n) is complex:
        return _math.gcd(n.real, n.imag)
    try:
        return n.gcd()
    except Exception:
        pass
    return n


def gcd(*integers):
    return _math.gcd(map(_get_gcd, integers))


# Triangle checks #
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
        raise ValueError(f'lengths {a}, {b}, and {c} cannot form a triangle')
    if _math.isclose(a, b, rel_tol=0, abs_tol=1e-14):
        if _math.isclose(a, c, rel_tol=0, abs_tol=1e-14):
            return equilateral
        return isosceles
    if _math.isclose(a, c, rel_tol=0, abs_tol=1e-14):
        return isosceles
    if _math.isclose(b, c, rel_tol=0, abs_tol=1e-14):
        return isosceles
    return scalene


obtuse = 'obtuse'
acute = 'acute'
right = 'right'
straight = 'straight'
circle = 'circle'


def AngleType(measure):
    '''Check whether an angle measure is acute, obtuse, or right angle.'''
    measure = abs(measure)
    measure = measure % _math.tau
    if measure > _math.pi:
        measure = _math.tau-measure
    if measure == 0:
        return circle
    if measure < _math.pi/2:
        return acute
    if measure == _math.pi/2:
        return right
    if measure == _math.pi:
        return straight
    return obtuse


# MATH #
def LawofCos(a, b, *, c=None, gamma=None):
    '''Return the appropriate value of either gamma or c, using law of
Cosine, one or the other must be given, not both'''
    if gamma is None and c is None:
        raise TypeError('Either c or gamma must be defined')
    if gamma is not None and c is not None:
        raise TypeError('c and gamma cannot both be defined')
    if gamma is None:
        pyth = (a**2)+(b**2)-(c**2)
        anglecos = (pyth)/(2*a*b)
        Angle = _math.acos(anglecos)
        return Angle
    pyth = (a**2)+(b**2)
    anglecos = _math.cos(gamma)
    c = _math.sqrt(pyth - (2*a*b*anglecos))
    return c


def LawofSin(alpha, a, *, beta=None, b=None):
    '''Return the appropiate value of either beta or b, using law of Sines,
one or the other must be given, not both'''
    if beta is None and b is None:
        raise TypeError('Either b or beta must be defined')
    if beta is not None and b is not None:
        raise TypeError('b and beta cannot both be defined')
    if beta is None:
        ratio = _math.sin(alpha)/a
        beta = _math.asin(ratio*b)
        return beta
    ratio = a/_math.sin(alpha)
    b = ratio*_math.sin(beta)
    return b


def Heron(a, b, c):
    '''Use heron's formula to find the area of a triangle'''
    s = (a+b+c)/2
    Area = _math.sqrt(s*(s-a)*(s-b)*(s-c))
    return Area


# TRIANGLE #
class triangle(object):
    def __init__(self, *, a=None, b=None, c=None, alpha=None, beta=None, gamma=None):
        kwval = {}
        argnames = ('a', 'b', 'c', 'alpha', 'beta', 'gamma')
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
                raise ValueError(f'{a}, {b}, and {c} do not form a triangle')
            kwval['gamma'] = gamma = LawofCos(a, b, c=c)
            kwval['beta'] = beta = LawofCos(a, c, c=b)
            kwval['alpha'] = _math.pi-beta-gamma
            self.__dict__ = kwval
            self.compute()
            return
        if len(tuple(filter(bool, (a, b, c)))) == 2:
            tr_e = ValueError('More than one triangle can be formed')
            if not a:
                if alpha:
                    kwval['a'] = a = LawofCos(b, c, gamma=alpha)
                    kwval['beta'] = beta = LawofSin(alpha, a, b=b)
                    kwval['gamma'] = _math.pi-beta-alpha
                    self.__dict__ = kwval
                    self.compute()
                    return
                raise tr_e
            if not b:
                if beta:
                    kwval['b'] = b = LawofCos(a, c, gamma=beta)
                    kwval['alpha'] = alpha = LawofSin(beta, b, b=a)
                    kwval['gamma'] = _math.pi-beta-alpha
                    self.__dict__ = kwval
                    self.compute()
                    return
                raise tr_e
            if gamma:
                kwval['c'] = c = LawofCos(a, b, gamma=gamma)
                kwval['alpha'] = alpha = LawofSin(gamma, c, b=a)
                kwval['beta'] = _math.pi-gamma-alpha
                self.__dict__ = kwval
                self.compute()
                return
            raise tr_e
        if not alpha:
            kwval['alpha'] = alpha = _math.pi-gamma-beta
        elif not beta:
            kwval['beta'] = beta = _math.pi-alpha-beta
        else:
            kwval['gamma'] = gamma = _math.pi-beta-alpha

        if a:
            kwval['b'] = LawofSin(alpha, a, beta=beta)
            kwval['c'] = LawofSin(alpha, a, beta=gamma)
            self.__dict__ = kwval
            self.compute()
            return
        if b:
            kwval['a'] = LawofSin(beta, b, beta=alpha)
            kwval['c'] = LawofSin(beta, b, beta=gamma)
            self.__dict__ = kwval
            self.compute()
            return
        kwval['a'] = LawofSin(gamma, c, beta=alpha)
        kwval['b'] = LawofSin(gamma, c, beta=beta)
        self.__dict__ = kwval
        self.compute()
        return

    def compute(self):
        if hasattr(self, 'type'):
            return
        self.area = Heron(self.a, self.b, self.c)
        self.angletype = AngleType(max(self.alpha, self.beta, self.gamma))
        self.perimeter = self.a+self.b+self.c
        self.type = TriangleType(self.a, self.b, self.c)

    def __repr__(self):
        return f'triangle(a={self.a}, b={self.b}, c={self.c})'

# eof
