'''
File: quaternion.py
Version: 1.2.1
Author: Austin Garcia

a quaternion class

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

'''

__version__ = '1.2.1'

from usefulpy import validation as _validation
try: from nmath import *
except: from usefulpy.mathematics.nmath import *

class quaternion(object):
    '''A quaternion class'''
    def __init__(self, a = None, b = None, c = None, d = None):
        '''__init__ for quaternion class:
>>> quaternion(1, 2, 3, 4)
(1+2i+3j+4k)
>>> quaternion(1+3j)
(1+3i)
>>> '''
        if a == None: a = 0
        if type(a) == quaternion:
            self.real = a.real
            self.i = a.i
            self.j = a.j
            self.k = a.k
            return
        if type(a) == complex:
            if b != None or c != None or d != None: raise ValueError
            self.real = a.real
            self.i = a.imag
            self.j = 0
            self.k = 0
            return
        if b == None: b = 0
        if c == None: c = 0
        if d == None: d = 0
        for num in (a, b, c, d):
            if not _validation.is_float(num):raise ValueError
        self.real = a
        self.i = b
        self.j = c
        self.k = d

    def __complex__(self):
        '''return complex(self) if j and k are empty'''
        if self.j != 0: return
        if self.k != 0: return
        return complex(self.real, self.i)

    def __abs__(self):
        '''return abs(self)'''
        return hypot(self.real, self.i, self.j, self.k)

    def __float__(self):
        '''return float(self) if i, j, and k are empty'''
        if self.i != 0: return
        if self.j != 0: return
        if self.k != 0: return
        return float(self.real)

    def __int__(self):
        '''return int(self) if i, j, and k are empty'''
        if self.i != 0: return
        if self.j != 0: return
        if self.k != 0: return
        return int(self.real)

    def __add__(self, other):
        '''return self+other'''
        if type(self) != type(other):
            other = quaternion(other)
        real = self.real+other.real
        i = self.i+other.i
        j = self.j+other.j
        k = self.k+other.k
        return _validation.trynumber(quaternion(real, i, j, k))

    def __radd__(other, self):
        '''return self+other'''
        return _validation.trynumber(other+self)

    def __sub__(self, other):
        '''return self-other'''
        if type(self) != type(other):
            other = quaternion(other)
        real = self.real+other.real
        i = self.i-other.i
        j = self.j-other.j
        k = self.k-other.k
        return _validation.trynumber(quaternion(real, i, j, k))

    def __rsub__(other, self):
        '''return self-other'''
        return _validation.trynumber(self+(-1*other))

    def __mul__(self, other):
        '''return self*other'''
        if type(self) != type(other):
            other = quaternion(other)
        a, b, c, d = self.real, self.i, self.j, self.k
        e, f, g, h = other.real, other.i, other.j, other.k
        real = a*e - b*f - c*g - d*h
        i = a*f + b*e + c*h - d*g
        j = a*g - b*h + c*e + d*f
        k = a*h + b*g - c*f + d*e
        return _validation.trynumber(quaternion(real, i, j, k))

    def __rmul__(other, self):
        '''return self*other'''
        if type(self) != type(other):
            self = quaternion(self)
        a, b, c, d = self.real, self.i, self.j, self.k
        e, f, g, h = other.real, other.i, other.j, other.k
        real = a*e - b*f - c*g - d*h
        i = a*f + b*e + c*h - d*g
        j = a*g - b*h + c*e + d*f
        k = a*h + b*g - c*f + d*e
        return _validation.trynumber(quaternion(real, i, j, k))

    def floor(self):
        return _validation.trynumber(floor(self.real), floor(self.i), floor(self.j), floor(self.k))

    def __floordiv__(self, other):
        n = self/other
        if type(n) in (int, float): return int(n)
        return n.floor()

    def __rfloordiv__(other, self):
        n = self/other
        if type(n) in (int, float): return int(n)
        return n.floor()

    def __truediv__(self, other):
        '''return self/other'''
        if type(self) != type(other):
            other = quaternion(other)
        another = self*(other.converse())
        divfactor=((abs(other))**2)
        another.real = another.real/divfactor
        another.i = another.i/divfactor
        another.j = another.j/divfactor
        another.k = another.k/divfactor
        return _validation.trynumber(another)

    def __rtruediv__(other, self):
        '''return self/other'''
        if type(self) != other.__class__: self = other.__class__(self)
        return _validation.trynumber(self/other)

    def __str__(self):
        '''str(self)'''
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
        return ' + '.join(List)

    def converse(self):
        '''return the mathematical converse of self:
>>> x = quaternion(1, 1, 5)
(1+1i+5j)
>>> x.converse()
1-1i-5j
>>> '''
        return _validation.trynumber(quaternion(self.real, -self.i, -self.j, -self.k))

    def __lt__(self, other):
        '''return self<other'''
        if not type(other) is self.__class__: other = self.__class__(other)
        if self.real != other.real: return self.real<other.real
        if self.i != other.i: return self.i<other.i
        if self.j != other.j: return self.j<other.j
        return self.k<other.k
        

    def __gt__(self, other):
        '''return self>other'''
        if not type(other) is self.__class__: other = self.__class__(other)
        if self.real != other.real: return self.real>other.real
        if self.i != other.i: return self.i>other.i
        if self.j != other.j: return self.j>other.j
        return self.k>other.k

    def __le__(self, other):
        '''return self<=other'''
        if not type(other) is self.__class__: other = self.__class__(other)
        if self.real != other.real: return self.real<other.real
        if self.i != other.i: return self.i<other.i
        if self.j != other.j: return self.j<other.j
        return self.k<=other.k

    def __ge__(self, other):
        '''return self>=other'''
        if not type(other) is self.__class__: other = self.__class__(other)
        if self.real != other.real: return self.real>other.real
        if self.i != other.i: return self.i>other.i
        if self.j != other.j: return self.j>other.j
        return self.k>=other.k

    def __eq__(self, other):
        '''return self==other'''
        if type(other) != self.__class__: other = self.__class__(other)
        if self.real != other.real: return False
        if self.i != other.i: return False
        if self.j != other.j: return False
        return self.k == other.k

    def __ne__(self, other):
        '''return self != other'''
        return not self == other

    def __gcd__(self):
        '''findgcd(self.real, self.i, self.j, self.k)'''
        return findgcd(self.real, self.i, self.j, self.k)

    def gcd(self, other):
        return findgcd(self.__gcd__, other)

    def rgcd(self, other):
        return self.gcd(other)

    def __repr__(self):
        '''IDLE representation'''
        return '('+str(self)+')'

    def __pow__(self, other):
        '''return self**other'''
        try:
            self = _validation.trynumber(complex(self))
            self**other
        except: pass
        if _validation.is_integer(other) and other>=0:
            current = 1
            for l in range(int(other)): current *= self
            return current
        else: raise NotImplementedError('Raising quaternions to non-integer powers has not been implemented yet')

    def __rpow__(other, self):
        '''return other**self'''
        try:
            other = _validation.trynumber(complex(other))
            self**other
        except: pass
        if _validation.is_integer(other) and other>=0:
            current = 1
            for l in range(int(other)): current *= self
            return current
        else:
            print('2')
            r, theta = polar(self)
            print(r, theta)
            return _validation.trynumber((r**other)*cis(theta*other))

i = quaternion(b = 1)
j = quaternion(c = 1)
k = quaternion(d = 1)

#eof
