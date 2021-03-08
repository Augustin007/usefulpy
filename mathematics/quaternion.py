'''
Quaternion

a quaternion class

LICENSE PLATAFORMS and INSTALLATION:
This is a section of usefulpy. See usefulpy.__init__ and usefulpy license
file

RELEASE NOTES:
1
 1.1
  Version 1.1.1
   quaternion class holds data for a quaternion, can be added, subtracted, etc.
  Version 1.1.2
   several bug fixes
 1.2
  Version 1.2.1
   __init__ changed to work for a lot more classes.
   Comparison operators are now supported
   i, j, and k are added as variables.
  Version 1.2.2
   Some more testing and thus... more bug fixes
 1.3
  Version 1.3.1
   Small internal changes, addition of __pow__, but not complete, only works
   with integers.
2
 2.1
  Version 2.1.1
   quaternion class recreated, is now immutable, much more broad reach
   implimented. __pow__ now works for floats more often, but still has some
   problems
  Version 2.1.2
   improved __pow__ somewhat, still has problems (gah!)
   improved look of repr and str.
 2.2
  Version 2.2.1
   __pow__, __rpow__, __ln__, __log__, (et cetera) are working. 
  Version 2.2.2
   Small bug-fixes and clean up.
'''
##UPDATED TO: Usefulpy 1.2.1

__author__ = 'Austin Garcia'
__version__ = '2.1.2'
__package__ = 'usefulpy.mathematics'

from .. import validation as _validation
from ..IDLE import _usefulpy_correct_syntax
from .nmath import *
from .PrimeComposite import *

class quaternion(object):
    '''A quaternion class:
>>> quaternion(1, 2, 3, 4)
(1+2i+3j+4k)
>>> quaternion(1+3j)
(1+3i)
>>> 
'''
    def __new__(cls, a = None, b = None, c = None, d = None):
        '''__new__ for quaternion class, works well (hopefully) for most
variations of input'''
        ##print(a, b, c, d)

        self = super(quaternion, cls).__new__(cls)
        
        if a == None: a = 0

        if b == None and c == None and d == None:
            if type(a) is quaternion:
                self.real = _validation.trynumber(a.real)
                self.i = _validation.trynumber(a.i)
                self.j = _validation.trynumber(a.j)
                self.k = _validation.trynumber(a.k)
                return self
            if _validation.is_complex(a):
                self.real = _validation.trynumber(a.real)
                self.i = 0
                self.j = _validation.trynumber(a.imag)
                self.k = 0
                return self
            if _validation.is_float(a):
                self.real = _validation.trynumber(a)
                self.i = 0
                self.j = 0
                self.k = 0
                return self
            if type(a) is str:
                try: return quaternion(fromstring(a))
                except: pass
                raise ValueError('quaternion() arg is a malformed string')
            try:
                q = a.__quaternion__()
                if type(q) is quaternion: return q
                else: raise TypeError(f'__quaternion__ method returned a non-quaternion type: (type {type(q)})')
            except: pass
            raise TypeError('A quaternion could not be made from a type {type(a)}')

        if b == None: b = 0
        if c == None: c = 0
        if d == None: d = 0

        allnums = True
        for num in (a, b, c, d):
            if not _validation.is_float(num): allnums = False

        if allnums:
            self.real = _validation.trynumber(a)
            self.i = _validation.trynumber(b)
            self.j = _validation.trynumber(c)
            self.k = _validation.trynumber(d)
            return self

        qsum = 0

        for multer, num in zip((1, i, j, k), (a, b, c, d)):
            ##print(qsum)
            qsum += multer*num

        return qsum

    ### Miscelaneous ###

    def vector(self, /):
        '''return self as a vector in a tuple'''
        return self.__getnewargs__()

    def is_versor(self, /):
        '''return True if quaternion is a versor (unit quaternion)'''
        return isclose(1, abs(self), rel_tol = 0, abs_tol = 1e-14)

    def normal(self):
        return self/abs(self)

    def vtuple(q):
        return q.i, q.j, q.k

    def astuple(q):
        return q.real, q.i, q.j, q/k

    def dot(v1, v2):
        '''dot product of v1 and v2'''
        a1, b1, c1, d1 = v1.astuple()
        a2, b2, c2, d2 = v2.astuple()
        return a1*a2+b1*b2+c1*c2+d1*d2

    

    def cross(v1, v2):
        '''cross product of v1 and v2'''
        if v1.real:
            raise ValueError('v1 must have no real part')
        if v2.real:
            raise ValueError('v2 must have no real part')
        b1, c1, d1 = v1.vtuple()
        b2, c2, d2 = v2.vtuple()
        return quaternion(0,(c1*d2-d1*c2),(d1*b2-b1*d2),(b1*c2-c1*b2))

    def is_unit(self, /):
        '''return True if distance from 0 is a single unit'''
        return isclose(1, abs(self), rel_tol = 0, abs_tol = 1e-14)

    def rotate(p, r, v, a):
        '''rotate point p r radians around vector v'''
        p = p-a
        v = v.normal().v()
        q = cis(r/2, v)
        p1 = q*p*(q**-1)
        return p1.v()+a.v()

    def __invert__(self, /):
        '''return the mathematical conjugate of self'''
        return quaternion(self.real, -self.i, -self.j, -self.k)

    def conjugate(self, /):
        '''return the mathematical conjugate of self'''
        return quaternion(self.real, -self.i, -self.j, -self.k)

    def gcd(self, /):
        '''return gcd of self'''
        return findgcd(self.real, self.i, self.j, self.k)

    def floor(self, /):
        '''return a quaternion composed only of integers and i, j, and k
(closer to zero)'''
        return quaternion(floor(self.real), floor(self.i), floor(self.j), floor(self.k))

    def ceil(self, /):
        '''return a quaternion composed only of integers and i, j, and k
(farther to zero)'''
        return quaternion(ceil(self.real), ceil(self.i), ceil(self.j), ceil(self.k))

    def __cos__(q, /):
        '''return cos of self in radians'''
        r, p, n = q.__polar__()
        return cos(q.real)*cosh(r*sin(p))-n*sin(q.real)*sinh(r*sin(p))

    def __sin__(q, /):
        '''return cos of self in radians'''
        r, p, n = q.__polar__()
        return sin(q.real)*cosh(r*sin(p))+n*cos(q.real)*sinh(r*sin(p))

    def __tan__(q, /):
        return q.__sin__()*(q.__cos__()**-1)

    def __cot__(q, /):
        return q.__cos__()*(q.__sin__()**-1)

    def __csc__(q, /):
        return q.__sin__()**-1

    def __sec__(q, /):
        return q.__cos__()**-1

    def __atan__(q, /):
        return -(n/2)*ln((n-q)/(n+q))

    def __acos__(q, /):
        return pi/2-asin(q)

    def __asin__(q, /):
        r, p, n = q.__polar__()
        return n*ln(sqrt(1-(q**2))-n*q)

    def __acsc__(q, /):
        return asin(1/q)

    def __asec__(q, /):
        return acos(1/q)

    def __acot__(q, /):
        return atan(1/q)

    def __cosh__(q, /):
        r, p, n = q.__polar__()
        return cosh(q.real)*cos(r*sin(p))+n*sinh(q.real)*sin(r*sin(p))

    def __sinh__(q, /):
        r, p, n = q.__polar__()
        return sinh(q.real)*cos(r*sin(p))+n*cosh(q.real)*sin(r*sin(p))

    def __tanh__(q, /):
        return q.__sinh__()*(q.__cosh__()**-1)

    def __sech__(q, /):
        return q.__cosh__()**-1

    def __csch__(q, /):
        return q.__sinh__()**-1

    def __coth__(q, /):
        return q.__cosh__()*(q.__sinh__()**-1)

    def __acosh__(q, /):
        return ln(q+sqrt((q**2)-1))

    def __asinh__(q, /):
        return ln(q+sqrt((q**2)+1))

    def __atanh__(q, /):
        return (1/2)*ln((1+q)*((1-q)**-1))

    def __asech__(q, /):
        return acosh(1/q)

    def __acsch__(q, /):
        return asinh(1/q)

    def __acoth__(q, /):
        return atanh(1/q)

    def __polar__(q, /):
        '''the distance and three angles from 0 that can represent the
quaternion'''
        r = hypot(q.real, q.i, q.j, q.k)
        phi = acos(q.real/abs(q))
        ñ = q.v()/abs(q.v())
        return (r, phi, ñ)

    def __phase__(self, /):
        theta1 = atan(self.i/self.real)
        theta2 = atan(self.j/hypot(self.i, self.real))
        theta3 = atan(self.k/hypot(self.real, self.i, self.j))
        return (theta1, theta2, theta3)

    def __ln__(x, /):
        return ln(abs(x))+(x.v()/abs(x.v())*acos(x.real/abs(x)))

    def __log__(self, other):
        return ln(self)/ln(other)

    ### Conversion to other types ###

    def __complex__(self, /):
        '''return complex(self) if j and k are empty'''
        if self.i != 0: return
        if self.k != 0: return
        return complex(self.real, self.i)

    def __int__(self, /):
        '''return int(self) if i, j, and k are empty'''
        if self.i != 0: return
        if self.j != 0: return
        if self.k != 0: return
        return int(self.real)

    def __float__(self, /):
        '''return float(self) if i, j, and k are empty'''
        if self.i != 0: return
        if self.j != 0: return
        if self.k != 0: return
        return float(self.real)

    def __str__(self, /):
        '''str(self)'''
        if self == 0: return '0'
        List = [self.real, self.i, self.j, self.k]
        nList = List.copy()
        List = list(map(str, List))
        List[1] += 'i'
        List[2] += 'j'
        List[3] += 'k'
        count = 0
        for val in nList:
            if val == 0: List.pop(count)
            else: count+=1
        return '+'.join(List).replace('+-', '-')

    def __repr__(self, /):
        '''IDLE representation'''
        if self == 0: return '(0)'
        List = [self.real, self.i, self.j, self.k]
        nList = List.copy()
        List = list(map(str, List))
        List[1] += 'i'
        List[2] += 'j'
        List[3] += 'k'
        count = 0
        for val in nList:
            if val == 0: List.pop(count)
            else: count+=1
        return '('+'+'.join(List).replace('+-', '-')+')'

    def __bool__(self, /):
        '''return False if self is 0, return True otherwise'''
        return self != 0

    def __getnewargs__(self, /):
        return self.real, self.i, self.j, self.k

    ### Arithmetic Operators ###

    def __abs__(self, /):
        '''return abs(self)'''
        return hypot(self.real, self.i, self.j, self.k)

    def __add__(self, other, /):
        '''return self+other'''
        if type(self) != type(other):
            other = quaternion(other)
        real = self.real+other.real
        i = self.i+other.i
        j = self.j+other.j
        k = self.k+other.k
        return quaternion(real, i, j, k)

    def __radd__(other, self, /):
        '''return self+other'''
        return other+self

    def __sub__(self, other, /):
        '''return self-other'''
        if type(self) != type(other): other = quaternion(other)
        real = self.real-other.real
        i = self.i-other.i
        j = self.j-other.j
        k = self.k-other.k
        return quaternion(real, i, j, k)

    def __rsub__(other, self, /):
        '''return self-other'''
        return self+(-1*other)

    def __mul__(self, other, /):
        '''return self*other'''
        if type(self) != type(other): other = quaternion(other)
        a, b, c, d = self.real, self.i, self.j, self.k
        e, f, g, h = other.real, other.i, other.j, other.k
        real = a*e - b*f - c*g - d*h
        i = a*f + b*e + c*h - d*g
        j = a*g - b*h + c*e + d*f
        k = a*h + b*g - c*f + d*e
        return quaternion(real, i, j, k)

    def __rmul__(other, self, /):
        '''return self*other'''
        if type(self) != type(other): self = quaternion(self)
        a, b, c, d = self.real, self.i, self.j, self.k
        e, f, g, h = other.real, other.i, other.j, other.k
        real = a*e - b*f - c*g - d*h
        i = a*f + b*e + c*h - d*g
        j = a*g - b*h + c*e + d*f
        k = a*h + b*g - c*f + d*e
        return quaternion(real, i, j, k)

    def __floordiv__(self, other, /):
        '''return self//other'''
        n = self/other
        if type(n) in (int, float): return int(n)
        return n.floor()

    def __rfloordiv__(other, self, /):
        '''return self//other'''
        n = self/other
        if type(n) in (int, float): return int(n)
        return n.floor()

    def __truediv__(self, other, /):
        '''return self/other'''
        if type(self) != type(other): other = quaternion(other)
        another = quaternion(self*(other.conjugate()))
        divfactor=((abs(other))**2)
        real = another.real/divfactor
        i = another.i/divfactor
        j = another.j/divfactor
        k = another.k/divfactor
        return quaternion(real, i, j, k)

    def __rtruediv__(other, self, /):
        '''return self/other'''
        if type(self) != other.__class__: self = other.__class__(self)
        return _validation.trynumber(self/other)

    def __gcd__(self, other, /):
        return findgcd(self.gcd(), other)

    def __rgcd__(self, other, /):
        return self.__gcd__(other)
    
    def __pow__(self, other, /):
        '''return self**other'''
        if other == 0: return 1
        if _validation.is_complex(self):
            self = _validation.trynumber(self)
            return quaternion(self**other)
        if _validation.is_integer(other) and other>=0:
            current = 1
            for l in range(int(other)): current *= self
            return quaternion(current)
        if _validation.is_integer(other):
            return 1/(self**-other)
        r, p, n = self.__polar__()
        return (r**other)*(cos(other*p)+n*sin(other*p))

    def __exp__(q):
        a = q.real
        v = q.v()
        return (e**a)*(cos(abs(v))+ ((v/abs(v)*sin(abs(v)))))
    
    def __rpow__(self, other, /):
        '''return other**self'''
        # okay, I know math... so I can figure this out! I think:
        # My thought process is such:
        # e**n = x^0/0!+x^1/1!+x^2/2!+x^3/3!...
        # so o**s = e**(ln(o)*s)
        num = ln(other)*self
        # Here the comparison of two versions: 
        # The left one is my method
        # The right one is python's built in method for
        # the identical complex method
        # ((1.5384778027279444+1.277922552627269i), (1.5384778027279442+1.2779225526272695j))
        return exp(num)

    def __mod__(self, other):
        return self-((self//other)*other)

    def __rmod__(other, self):
        return self-((self//other)*other)

    def __divmod__(self, other, /):
        return (self//other, self%other)

    def __rdivmod__(other, self, /):
        return (self//other, self%other)

    def __neg__(self, /):
        return -1*self

    def __pos__(self, /):
        return self

    ### Comparison Operators ###

    def __eq__(self, other, /):
        '''return self==other'''
        try:
            if type(other) != self.__class__: other = self.__class__(other)
            if self.real != other.real: return False
            if self.i != other.i: return False
            if self.j != other.j: return False
            return self.k == other.k
        except: return False

    def __ne__(self, other, /):
        '''return self != other'''
        return not self == other

    def __ge__(self, other, /):
        return float(self)>=float(other)

    def __le__(self, other, /):
        return float(self)<=float(other)

    def __lt__(self, other, /):
        return float(self)<float(other)

    def __gt__(self, other, /):
        return float(self)>float(other)

    def v(self):
        return quaternion(0, self.i, self.j, self.k)

    ## TODO: __hash__ still needs to be implimented


def hyperrect(r, theta1, theta2, theta3):
    real = r*cos(theta1)*cos(theta2)*cos(theta3)
    i = r*sin(theta1)*cos(theta2)*cos(theta3)
    j = r*sin(theta2)*cos(theta3)
    k = r*sin(theta3)
    return quaternion(real, i, j, k)

def fromstring(string):
    string = _usefulpy_correct_syntax(string)
    try: return quaternion(eval(string))
    except: pass
    return ValueError('String does not represent a quaternion')

i = quaternion(b = 1)
j = quaternion(c = 1)
k = quaternion(d = 1)
tesseract = 1+i+j+k

#eof
