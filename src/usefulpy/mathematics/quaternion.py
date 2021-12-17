'''
Quaternion

a quaternion class

LICENSE PLATAFORMS and INSTALLATION:
This is a section of usefulpy. See usefulpy.__init__ and usefulpy license
file

RELEASE NOTES:
0
 0.0
  Version 0.0.0
   quaternion class holds data for a quaternion, can be added, subtracted, etc.
  Version 0.0.1
   several bug fixes
 0.1
  Version 0.1.0
   __init__ changed to work for a lot more classes.
   Comparison operators are now supported
   i, j, and k are added as variables.
  Version 0.1.1
   Some more testing and thus... more bug fixes
 0.2
  Version 0.2.0
   Small internal changes, addition of __pow__, but not complete, only works
   with integers.
1
 1.0
  Version 1.0.0
   quaternion class recreated, is now immutable, much more broad reach
   implimented. __pow__ now works for floats more often, but still has some
   problems
  Version 1.0.1
   improved __pow__ somewhat, still has problems (gah!)
   improved look of repr and str.
 1.1
  Version 1.1.0
   __pow__, __rpow__, __ln__, __log__, (et cetera) are working.
  Version 1.1.1
   Small bug-fixes and clean up.
  Version 1.1.2
   __hash__ implemented
2
 2.0
  Version 2.0.0
   Code rewritten, heavy efficiency improvements, bugfixes.
   Customized setattr, better documentation.
  Verion 2.0.1
   You guessed it! debugging!

   Parenthesis wrong in asin function, fixed!

   Several functions were depending on the old nmath functions even though
    These were no longer being imported and built-in math and cmath were being
    imported instead
'''

# DUNDERS #
__author__ = 'Augustin Garcia'
__version__ = '2.0.0'
__all__ = ('quaternion', 'i', 'j', 'k', 'tesseract')

# IMPORTS #
import math
import cmath
import functools


# QUATERNION #
class quaternion:
    '''A quaternion class:
>>> quaternion(1, 2, 3, 4)
(1+2i+3j+4k)
>>> quaternion(1+3j)
(1+3i)
>>>
'''
    __slots__ = ('real', 'i', 'j', 'k')

    def __new__(cls, a=0, b=0, c=0, d=0):
        '''__new__ for quaternion class'''
        self = super(quaternion, cls).__new__(cls)

        # If there is a single argument input
        if all(map(lambda x: not x, (b, c, d))):
            if type(a) in (int, float):
                super.__setattr__(self, 'real', a)
                super.__setattr__(self, 'i', 0)
                super.__setattr__(self, 'j', 0)
                super.__setattr__(self, 'k', 0)
                return self
            elif type(a) is quaternion:
                return a
            elif type(a) is complex:
                return quaternion(a.real, 0, a.imag, 0)
            try:
                q = a.__quaternion__()
                if type(q) is quaternion:
                    return q
                else:
                    raise TypeError(f'__quaternion__ method returned \
                        non-quaternion, {type(q)}')
            except AttributeError:
                pass
            raise TypeError(f'A quaternion could not be made from {type(a)}')

        # If all arguments are real numbers
        if all(map(lambda x: type(x) in (int, float), (a, b, c, d))):
            super.__setattr__(self, 'real', float(a))
            super.__setattr__(self, 'i', float(b))
            super.__setattr__(self, 'j', float(c))
            super.__setattr__(self, 'k', float(d))
            return self

        # Otherwise
        try:
            qsum = 0

            for multer, num in zip((1, i, j, k), (a, b, c, d)):
                qsum += num*multer

            return qsum
        except Exception:
            pass
        raise TypeError(f'A quaternion could not be made from a {type(a)}')

    # Miscelaneous #

    def vector(self, /):
        '''return self as a vector in a tuple'''
        return self.__getnewargs__()

    def v(self):
        ''' return imag part of self'''
        return quaternion(0, self.i, self.j, self.k)

    @property
    def imag(self):
        return self.v()

    def __setattr__(self, name, value):
        '''set attribute name to value'''
        raise AttributeError('Attributes may not be assigned')

    def is_versor(self, /):
        '''return True if quaternion is a versor (unit quaternion)'''
        return math.isclose(1, abs(self), rel_tol=0, abs_tol=1e-14)

    def normal(self, /):
        '''return normal of vector'''
        return self*(1/abs(self))

    def vtuple(q, /):
        '''return tuple containing imag parts'''
        return q.i, q.j, q.k

    def astuple(q, /):
        '''self as tuple'''
        return q.real, q.i, q.j, q.k

    @staticmethod
    def dot(v1, v2, /):
        '''dot product of v1 and v2'''
        a1, b1, c1, d1 = v1.astuple()
        a2, b2, c2, d2 = v2.astuple()
        return a1*a2+b1*b2+c1*c2+d1*d2

    @staticmethod
    def cross(v1, v2, /):
        '''cross product of v1 and v2'''
        if v1.real:
            raise ValueError('v1 must have no real part')
        if v2.real:
            raise ValueError('v2 must have no real part')
        b1, c1, d1 = v1.vtuple()
        b2, c2, d2 = v2.vtuple()
        return quaternion(0, (c1*d2-d1*c2), (d1*b2-b1*d2), (b1*c2-c1*b2))

    def is_unit(self, /):
        '''return True if distance from 0 is a single unit'''
        return math.isclose(1, abs(self), rel_tol=0, abs_tol=1e-14)

    def isinf(self):
        ''' return True if any value is infinite '''
        if math.inf in self.astuple():
            return True
        if -math.inf in self.astuple():
            return True
        return False

    def isnan(self):
        ''' return True if any value is infinite '''
        return math.nan in self.astuple()

    def isfinite(self):
        return not (self.isinf() & self.isnan())

    def rotate(p, r, v, a):
        '''rotate point p r radians around vector v'''
        p = p-a
        v = v.normal().v()
        q = math.cos(r/2)+v*math.sin(r/2)
        p1 = q*p*(q**-1)
        return p1.v()+a.v()

    def gcd(self, /):
        '''return gcd of self'''
        return math.gcd(self.real, self.i, self.j, self.k)

    def floor(self, /):
        '''return a quaternion composed only of integers and i, j, and k
(closer to zero)'''
        return quaternion(math.floor(self.real), math.floor(self.i),
                          math.floor(self.j), math.floor(self.k))

    __floor__ = floor

    def ceil(self, /):
        '''return a quaternion composed only of integers and i, j, and k
(farther to zero)'''
        return quaternion(math.ceil(self.real), math.ceil(self.i),
                          math.ceil(self.j), math.ceil(self.k))

    __ceil__ = ceil

    # TRIG #
    def cos(q, /):
        '''return mcos of self in radians'''
        r, p, n = q.__polar__()
        return math.cos(q.real)*math.cosh(r*math.sin(p))- \
            n*math.sin(q.real)*math.sinh(r*math.sin(p))

    def sin(q, /):
        '''return sin of self in radians'''
        r, p, n = q.__polar__()
        return math.sin(q.real)*math.cosh(r*math.sin(p))+ \
            n*math.cos(q.real)*math.sinh(r*math.sin(p))

    def tan(q, /):
        '''return tan of self in radians'''
        return q.sin()*(q.cos()**-1)

    def cot(q, /):
        '''return cot of self in radians'''
        return q.cos()*(q.sin()**-1)

    def csc(q, /):
        '''return csc of self in radians'''
        return q.sin()**-1

    def sec(q, /):
        '''return sec of self in radians'''
        return q.cos()**-1

    def atan(q, /):
        '''return atan of self in radians'''
        r, p, n = q.__polar__()
        return -(n/2)*math.log((n-q)/(n+q))

    def acos(q, /):
        '''return acos of self in radians'''
        return math.pi/2-q.asin()

    def asin(q, /):
        '''return asin of self in radians'''
        r, p, n = q.__polar__()
        return n*((1-(q**2))**(1/2)-n*q).ln()

    def acsc(q, /):
        '''return acsc of self in radians'''
        return (q**-1).asin()

    def asec(q, /):
        '''return asec of self in radians'''
        return (q**-1).asin()

    def acot(q, /):
        '''return acot of self in radians'''
        return (1/q).atan()

    def cosh(q, /):
        '''return cosh of self in radians'''
        r, p, n = q.__polar__()
        return math.cosh(q.real)*math.cos(r*math.sin(p))+ \
            n*math.sinh(q.real)*math.sin(r*math.sin(p))

    def sinh(q, /):
        '''return sinh of self in radians'''
        r, p, n = q.__polar__()
        return math.sinh(q.real)*math.cos(r*math.sin(p))+ \
            n*math.cosh(q.real)*math.sin(r*math.sin(p))

    def tanh(q, /):
        '''return tanh of self in radians'''
        return q.sinh()*(q.cosh()**-1)

    def sech(q, /):
        '''return sech of self in radians'''
        return q.cosh()**-1

    def csch(q, /):
        '''return csch of self in radians'''
        return q.sinh()**-1

    def coth(q, /):
        '''return coth of self in radians'''
        return q.cosh()*(q.sinh()**-1)

    def acosh(q, /):
        '''return acosh of self in radians'''
        return (q+((q**2)-1**(1/2))).ln()

    def asinh(q, /):
        '''return asinh of self in radians'''
        return (q+((q**2)+1**(1/2))).ln()

    def atanh(q, /):
        '''return atanh of self in radians'''
        return (1/2)*(((1+q)*((1-q)**-1))).ln()

    def asech(q, /):
        '''return asech of self in radians'''
        return (1/q).acosh()

    def acsch(q, /):
        '''return acsch of self in radians'''
        return (1/q).asin()

    def acoth(q, /):
        '''return acoth of self in radians'''
        return (1/q).atan()

    # ALGEBRAIC #

    def __invert__(self, /):
        '''return the mathematical conjugate of self'''
        return quaternion(self.real, -self.i, -self.j, -self.k)

    def conjugate(self, /):
        '''return the mathematical conjugate of self'''
        return quaternion(self.real, -self.i, -self.j, -self.k)

    @functools.cache
    def __polar__(q, /):
        '''the distance and angles and slice from 0 that can represent the
quaternion'''
        r = math.hypot(q.real, q.i, q.j, q.k)
        phi = math.acos(q.real/abs(q))
        ñ = q.v()/abs(q.v())
        return (r, phi, ñ)
    polar = __polar__

    def __phase__(self, /):
        '''returns the angle phase between (0, 1) and self'''
        return math.acos(self.real/abs(self))

    def ln(x, /):
        '''return the natural logarithm of self'''
        return math.log(abs(x))+(x.v()/abs(x.v())*math.acos(x.real/abs(x)))

    def log(self, other):
        '''return the logarithm base other of self'''

        def gln(n):
            try:
                return math.log(n)
            except Exception:
                pass
            try:
                return cmath.log(n)
            except Exception:
                pass
            try:
                return n.ln()
            except Exception:
                pass
            try:
                return n.log(math.e)
            except Exception:
                return NotImplemented

        try:
            return self.ln()/gln(other)
        except Exception:
            pass
        try:
            return other.rlog(self)
        except Exception:
            pass
        raise TypeError(f'invalid log base of type {type(other).__name__}')

    def rlog(self, other):
        '''return the logarithm base self of other'''

        def gln(n):
            try:
                return math.log(n)
            except Exception:
                pass
            try:
                return cmath.log(n)
            except Exception:
                pass
            try:
                return n.ln()
            except Exception:
                pass
            try:
                return n.log(math.e)
            except Exception:
                return NotImplemented

        try:
            return gln(other)/self.ln()
        except Exception:
            pass
        raise TypeError(f'log of {type(other).__name__} cannot be found')

    def exp(q):
        '''return e**self'''
        a = q.real
        v = q.v()
        return math.exp(a)*(math.cos(abs(v))+((v/abs(v)*math.sin(abs(v)))))

    # CONVERSION #

    def __complex__(self, /):
        '''return complex(self) if j and k are empty'''
        if self.i != 0:
            return NotImplemented
        if self.k != 0:
            return NotImplemented
        return complex(self.real, self.j)

    def __int__(self, /):
        '''return int(self) if i, j, and k are empty'''
        if self.i != 0:
            return NotImplemented
        if self.j != 0:
            return NotImplemented
        if self.k != 0:
            return NotImplemented
        return int(self.real)

    def __float__(self, /):
        '''return float(self) if i, j, and k are empty'''
        if self.i != 0:
            return NotImplemented
        if self.j != 0:
            return NotImplemented
        if self.k != 0:
            return NotImplemented
        return float(self.real)

    @functools.cache
    def __str__(self, /):
        '''return string representation of self'''
        if self == 0:
            return '(0)'
        return '+'.join([(str(a if int(a) != float(a) else int(a))+b
                          if a not in (1, -1) or b == '' else b)
                         for a, b in zip(self.astuple(),
                         ('', 'i', 'j', 'k')) if a]).replace('+-', '-')

    __repr__ = __str__

    def __bool__(self, /):
        '''return False if self is 0, return True otherwise'''
        return self != 0

    def __getnewargs__(self, /):
        return self.real, self.i, self.j, self.k

    # ARITHMETIC #
    def __abs__(self, /):
        '''return abs(self)'''
        return math.hypot(self.real, self.i, self.j, self.k)

    def __add__(self, other, /):
        '''return self+other'''
        if isinstance(other, (int, float, complex)):
            return quaternion(self.real+other.real, self.i,
                              self.j+other.imag, self.k)
        elif type(other) is quaternion:
            return quaternion(self.real+other.real, self.i+other.i,
                              self.j+other.j, self.k+other.k)
        return NotImplemented

    __radd__ = __add__

    def __sub__(self, other, /):
        '''return self-other'''
        if type(other) in (int, float, complex):
            return quaternion(self.real-other.real, self.i,
                              self.j-other.imag, self.k)
        elif type(other) is quaternion:
            return quaternion(self.real-other.real, self.i-other.i,
                              self.j-other.j, self.k-other.k)
        return NotImplemented

    def __rsub__(self, other, /):
        '''return other-self'''
        if isinstance(other, (int, float, complex)):
            return quaternion(other.real-self.real, -self.i,
                              other.imag-self.j, -self.k)
        elif type(other) is quaternion:
            return quaternion(other.real-self.real, other.i-self.i,
                              self.j+other.j, self.k+other.k)
        return NotImplemented

    def __mul__(self, other, /):
        '''return self*other'''
        if isinstance(other, (int, float)):
            return quaternion(*map(lambda q: q*other, self.astuple()))
        if isinstance(other, complex):
            other = quaternion(other)
        if type(other) is quaternion:
            a, b, c, d = self.astuple()
            e, f, g, h = other.astuple()
            real = a*e - b*f - c*g - d*h
            i = a*f + b*e + c*h - d*g
            j = a*g - b*h + c*e + d*f
            k = a*h + b*g - c*f + d*e
            return quaternion(real, i, j, k)
        return NotImplemented

    def __rmul__(self, other, /):
        '''return other*self'''
        if isinstance(other, (int, float)):
            return quaternion(*map(lambda q: q*other, self.astuple()))
        if isinstance(other, complex):
            other = quaternion(other)
        if type(other) is quaternion:
            a, b, c, d = other.astuple()
            e, f, g, h = self.astuple()
            real = a*e - b*f - c*g - d*h
            i = a*f + b*e + c*h - d*g
            j = a*g - b*h + c*e + d*f
            k = a*h + b*g - c*f + d*e
            return quaternion(real, i, j, k)
        return NotImplemented

    def __truediv__(self, other, /):
        '''return self/other if other is real'''
        if isinstance(other, (int, float)):
            return quaternion(*map(lambda q: q/other, self.astuple()))
        return NotImplemented

    def __rtruediv__(self, other, /):
        '''Not possible with quaternion'''
        if isinstance(other, (int, float)):
            return other*self**-1
        return NotImplemented

    def __pow__(self, other, /):
        '''return self**other'''
        if other == 0:
            return 1
        if isinstance(other, (int, float, complex, quaternion)):
            r, p, n = self.__polar__()
            return (r**other)*(math.cos(other*p)+n*math.sin(other*p))
        return NotImplemented

    def __rpow__(self, other, /):
        '''return other**self'''
        if isinstance(other, (int, float)):
            return (math.log(other)*self).__exp__()
        if isinstance(other, (complex)):
            return (cmath.log(other)*self).__exp__()
        if type(other) is quaternion:  # TODO: double check this
            return (other.__ln__()*self).__exp__()
        return NotImplemented

    def __neg__(self, /):
        '''return -self'''
        return quaternion(*map(lambda x: -x, (self.astuple())))

    def __pos__(self, /):
        '''return +self'''
        return self

    # COMPARISON OPERATORS #
    def __eq__(self, other, /):
        '''return self==other'''
        try:
            if type(other) != self.__class__:
                other = self.__class__(other)
            if self.real != other.real:
                return False
            if self.i != other.i:
                return False
            if self.j != other.j:
                return False
            return self.k == other.k
        except Exception:
            return False

    def __hash__(self):
        '''__hash__ for self'''
        return hash((self.astuple()))

    def __ne__(self, other, /):
        '''return self != other'''
        return not self == other

    def __ge__(self, other, /):
        '''return self >= other'''
        try:
            return float(self) >= float(other)
        except Exception:
            return NotImplemented

    def __le__(self, other, /):
        '''return self <= other'''
        try:
            return float(self) <= float(other)
        except Exception:
            return NotImplemented

    def __lt__(self, other, /):
        '''return self < other'''
        try:
            return float(self) < float(other)
        except Exception:
            return NotImplemented

    def __gt__(self, other, /):
        '''return self > other'''
        return float(self) > float(other)


i = quaternion(b=1)
j = quaternion(c=1)
k = quaternion(d=1)
tesseract = 1+i+j+k
