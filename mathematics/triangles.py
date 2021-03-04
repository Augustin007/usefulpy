'''
File: triangles.py
Version: 1.1.2
Author: Austin Garcia

Several functions to do with triangles

LICENSE:
This is a section of usefulpy. See usefulpy's lisence.md file.

PLATFORMS:
This is a section of usefulpy. See usefulpy.__init__'s "PLATFORMS" section.

INSTALLATION:
Put this file where Python can see it.

RELEASE NOTES:
1
 1.1
  Version 1.1.1:
   Several functions to do with triangles
  Version 1.1.2:
   Changed some variable names and importations. More comments.
 1.2
  Version 1.2.1:
   Triangle class, improved performance, bug fixes

'''
##UPDATED TO: Usefulpy 1.2.1

### INFO ###
__version__ = '1.1.2'
__author__ = 'Austin Garcia'
__package__ = 'usefulpy.mathematics'


### IMPORTS ###
import math as _math
from .. import validation as _validation

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
        return _validation.tryint(Angle)
    pyth = (a**2)+(b**2); anglecos = _math.cos(gamma)
    c = _math.sqrt(pyth - (2*a*b*anglecos))
    return _validation.tryint(c)

def LawofSin(alpha, a, *, beta = None, b = None):
    '''Return the appropiate value of either beta or b, using law of Sines,
one or the other must be given, not both'''
    if beta == None and b == None:
        raise TypeError('Either b or beta must be defined')
    if beta != None and b != None:
        raise TypeError('b and beta cannot both be defined')
    if beta == None: ratio = _math.sin(alpha)/a; beta = _math.asin(ratio*b); return _validation.tryint(beta)
    ratio = a/_math.sin(alpha); b = ratio*_math.sin(beta); return _validation.tryint(b)

def Heron(a, b, c):
    '''Use heron's formula to find the area of a triangle'''
    s = (a+b+c)/2; Area = _math.sqrt(s*(s-a)*(s-b)*(s-c))
    return _validation.tryint(Area)


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
