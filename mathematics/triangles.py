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
  Version 1.1.1
   Several functions to do with triangles
  Version 1.1.2
   Changed some variable names and importations. More comments.

'''

__version__ = '1.1.2'

try: from nmath import *
except: from usefulpy.mathematics.nmath import *

from usefulpy import validation as _validation

def isTriangle(a, b, c):
    '''Check if values can form a real triangle.'''
    a, b, c = abs(a), abs(b), abs(c)
    return not (a+b <= c or a+c <= b or b+c <= a or (0 in (a, b, c)))

def TriangleType(a, b, c):
    '''Return type of triangle.'''
    if a == b and a == c: return 'equilateral'
    elif a == b or a == c or b == c: return 'isosceles'
    return 'scalene'

def LawofCos(a, b, /, c = None, gamma = None):
    '''Return the appropriate value of either gamma or c, using law of
Cosine, one or the other must be given, not both'''
    if gamma == None and c == None: raise BaseException
    if gamma != None and c != None: raise BaseException
    if gamma == None:
        pyth = (a**2)+(b**2)-(c**2)
        if pyth == 0: return (pi/2)
        anglecos = (pyth)/(2*a*b); Angle = acos(anglecos)
        return _validation.tryint(Angle)
    pyth = (a**2)+(b**2); anglecos = cos(gamma)
    c = rt(2, pyth + (a*b*anglecos))
    return _validation.tryint(c)

def LawofSin(alpha, a, /, beta = None, b = None):
    '''Return the appropiate value of either beta or b, using law of Sines,
one or the other must be given, not both'''
    if beta == None and b == None: raise BaseException
    if beta != None and b != None: raise BaseException
    if beta == None: ratio = sin(alpha)/a; beta = asin(ratio*b); return _validation.tryint(beta)
    ratio = a/sin(alpha); b = ratio*sin(beta); return _validation.tryint(d)

def Heron(a, b, c):
    '''Use heron's formula to find the area of a triangle'''
    s = (a+b+c)/2; Area = sqrt(s*(s-a)*(s-b)*(s-c))
    return _validation.tryint(d)

def AngleType(Ang):
    '''Check whether an angle Ang is an acute, obtuse, or right angle.'''
    if Ang < 90: return 'acute'
    elif Ang > 90: return 'obtuse'
    return 'right'

#eof
