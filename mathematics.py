'''
File: mathematics.py
Version: 1.1.3
Author: Austin Garcia

Several mathematical functions plopped together.

LICENSE: See license file.

PLATFORMS:
This program imports the python built-ins functools, math, warnings and
statistics as well as my validation... should work on any python platform
where these are available.

INSTALLATION:
Put this file where Python can see it.

RELEASE NOTES:
1
 1.1
  Version 1.1.1:
   mathematics.py contains many mathematical functions.
  Version 1.1.2:
   An updated description and various bug fixes. Cleaner looking code with more
   comments.
  Version 1.1.3:
   Some small bug fixes
   Raises warnings at unfinished sections

'''
__version__ = '1.1.3'
from functools import reduce as _reduce
from math import *
del degrees, radians, log10
import warnings

from statistics import Decimal as num, Fraction as fraction
import validation

#log changed to work more like regular algebra
_log = log
ln = lambda x: _log(x)
def log(x, base = 10): return _log(x, base)

def lcf(a, b):
    '''Return least common factor of a and b'''
    ngcd = gcd(a, b)
    a, b = a//ngcd, b//ngcd
    return a*b*ngcd

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
            if validation.is_float(num):
                pass
            else: raise ValueError
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
        return validation.trynumber(quaternion(real, i, j, k))

    def __radd__(other, self):
        '''return self+other'''
        return validation.trynumber(other+self)

    def __sub__(self, other):
        '''return self-other'''
        if type(self) != type(other):
            other = quaternion(other)
        real = self.real+other.real
        i = self.i-other.i
        j = self.j-other.j
        k = self.k-other.k
        return validation.trynumber(quaternion(real, i, j, k))

    def __rsub__(other, self):
        '''return self-other'''
        return validation.trynumber(self+(-1*other))

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
        return validation.trynumber(quaternion(real, i, j, k))

    def __rmul__(other, self):
        '''return self*other'''
        if type(self) != type(other):
            other = quaternion(other)
        a, b, c, d = other.real, other.i, other.j, other.k
        e, f, g, h = self.real, self.i, self.j, self.k
        real = a*e - b*f - c*g - d*h
        i = a*f + b*e + c*h - d*g
        j = a*g - b*h + c*e + d*f
        k = a*h + b*g - c*f + d*e
        return validation.trynumber(quaternion(real, i, j, k))

    def floor(self):
        return validation.trynumber(floor(self.real), floor(self.i), floor(self.j), floor(self.k))

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
        another.real = makefraction(another.real, divfactor)
        another.i = makefraction(another.i, divfactor)
        another.j = makefraction(another.j, divfactor)
        another.k = makefraction(another.k, divfactor)
        return validation.trynumber(another)

    def __rtruediv__(other, self):
        '''return self/other'''
        if type(self) != other.__class__: self = other.__class__(self)
        return validation.trynumber(self/other)

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
        return validation.trynumber(quaternion(self.real, -self.i, -self.j, -self.k))

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

i = quaternion(b = 1)
j = quaternion(c = 1)
k = quaternion(d = 1)
    
_primes = [2]
_composites = []
def PrimeOrComposite(num):
    '''return 'prime' if prime and 'composite' if composite'''
    Prime = 'prime'
    Composite = 'composite'
    if not validation.is_integer(num): raise TypeError
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
    #if type(num) in Expression.ExpressionTypes: return num.__factor__ agh!
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

def makefraction(numer, denom = 1):
    '''Make a valid fraction type out of a float type'''
    numer = validation.tryint(round(float(numer), 15))
    denom = validation.tryint(round(float(denom), 15))
    while not (validation.is_integer(numer) and validation.is_integer(denom)):
        denom *= 10
        numer *= 10
    return fraction(int(numer), int(denom))

def isTriangle(a, b, c):
    '''Check if values can form a real triangle.'''
    a, b, c = abs(a), abs(b), abs(c)
    return not (a+b <= c or a+c <= b or b+c <= a or (0 in (a, b, c)))

def rt(nth, num):
    '''return nth root of num'''
    return validation.tryint(num**(1/nth))

def irt(nth, num):
    '''return integer nth root of num'''
    return int(rt(nth, num))

cbrt = lambda x: rt(3, x)

icbrt = lambda x: irt(3, x)

def TriangleType(a, b, c):
    '''Return type of triangle.'''
    if a == b and a == c: return 'equilateral'
    elif a == b or a == c or b == c: return 'isosceles'
    return 'scalene'

def RadiansToDegrees(r):
    '''Convert radians to degrees.'''
    d = (r*180)/pi; return validation.tryint(d)

def DegreesToRadians(r):
    '''Convert degrees to radians.'''
    d = (r*pi)/180; return validation.tryint(d)

def LawofCos(a, b, /, c = None, gamma = None):
    '''Return the appropriate value of either gamma or c, using law of
Cosine, one or the other must be given, not both'''
    if gamma == None and c == None: raise BaseException
    if gamma != None and c != None: raise BaseException
    if gamma == None:
        pyth = (a**2)+(b**2)-(c**2)
        if pyth == 0: return (pi/2)
        anglecos = (pyth)/(2*a*b); Angle = acos(anglecos)
        return validation.tryint(Angle)
    pyth = (a**2)+(b**2); anglecos = cos(gamma)
    c = rt(2, pyth + (a*b*anglecos))
    return validation.tryint(c)

def LawofSin(alpha, a, /, beta = None, b = None):
    '''Return the appropiate value of either beta or b, using law of Sines,
one or the other must be given, not both'''
    if beta == None and b == None: raise BaseException
    if beta != None and b != None: raise BaseException
    if beta == None: ratio = sin(alpha)/a; beta = asin(ratio*b); return validation.tryint(beta)
    ratio = a/sin(alpha); b = ratio*sin(beta); return validation.tryint(d)

def Heron(a, b, c):
    '''Use heron's formula to find the area of a triangle'''
    s = (a+b+c)/2; Area = sqrt(s*(s-a)*(s-b)*(s-c))
    return validation.tryint(d)

def AngleType(Ang):
    '''Check whether an angle Ang is an acute, obtuse, or right angle.'''
    if Ang < 90: return 'acute'
    elif Ang > 90: return 'obtuse'
    return 'right'

def gcd2(a, b):
    '''return gcd(a, b)'''
    if Expression in (type(a), type(b)):
        if type(a) is Expression: return a.gcd(b)
        return b.gcd(a)
    def acceptable(num):
        if validation.is_float(num): return abs(validation.tryint(float(num)))
        return num.__gcd__()
    ac = acceptable
    nums = (ac(a), ac(b))
    a, b = max(nums), min(nums)
    return gcd(a, b)

def findgcd(*numbers):
    '''Find the gcd of a series of numbers'''
    if len(numbers) == 0: raise BaseException
    if len(numbers) == 1: return numbers[0]
    if len(numbers) > 2: return _reduce(gcd2, numbers)
    return gcd2(*numbers)

def summation(start, finish, function = lambda x: x):
    '''Σ'''
    return _reduce((lambda x, y: x+function(y)), range(start, finish+1))

def fromNumBaseFormat(text):
    '''return a basenum from text:
>>> fromNumBaseFormat('14_5')
14₅
>>> '''
    if '_' in text:
        index = text.find('_')
        num, base = text[:index],text[index+1:]
        if not base.isdigit(): raise ValueError('This could not be converted into a basenum object')
        return basenum(num, int(base))
    else:
        if validation.is_float(text): return basenum(text)
        else: raise ValueError('This could not be converted into a basenum object')

class basenum(object):
    '''Stores numbers of different bases'''
    def __init__(self, strint, base = 10):
        '''__init__ for basenum class:
>>> x = basenum('3a2', 16)
>>> x
3a2₁₆
>>> y = x/2
>>> y
1d1₁₆
>>> float(x)
930.0
>>> int(y)
465
>>> '''
        if base not in range(0x2, 0x25): raise ValueError('This base is not within the range(0x2, 0x25)')
        if base < 10: maximum = str(base)
        else: maximum = chr(ord('a')+(base-10))
        self.Negative = False
        while strint[0] == '-':
            self.Negative = not(self.Negative)
            strint = strint[1:]
        for s in strint:
            if s >= maximum: raise ValueError('This is not a base', str(base), 'number')
            elif s == '.': pass
            elif ord(s)<ord('0'): raise ValueError('This is not a base', str(base), 'number')
            elif ord(s)>ord('9') and ord(s)<ord('a'):raise ValueError('This is not a base', str(base), 'number')
        while strint.startswith('0') and strint != '0': strint = strint[1:]
        if '.' in strint:
            if strint.count('.')!=1: raise ValueError('Too many "."s')
            else:
                index = strint.find('.')
                self.floatpart = strint[index+1:]
                strint = strint[:index]
                while self.floatpart.endswith('0'):self.floatpart = self.floatpart[:-1]
        else: self.floatpart = ''
        self.base = base
        self.num = strint

    def __float__(self):
        '''return float(self)'''
        decimal, num, base, floatpart = 0, self.num, self.base, self.floatpart
        exponent = len(num)-1
        num = (num+floatpart)
        for digit in num:
            if digit >= 'a': digit = str(ord(digit)-ord('a')+10)
            decimal += (float(digit)*base**exponent)
            exponent-=1
        if self.Negative: decimal = 0-decimal
        return decimal

    def __int__(self):
        '''return int(self)'''
        return int(self.num, self.base)

    def __str__(self):
        '''return str(self)'''
        SUB = str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉')
        if self.base != 10: base = str(self.base).translate(SUB)
        else: base = ''
        num = str(self.num)
        if self.floatpart != '': num += '.' + self.floatpart
        if self.Negative: num = '-' + num
        return(num+base)

    def convert(self, base):
        '''return a basenum of another base with same value'''
        if base not in range(0x2, 0x25): raise ValueError('This base is not within the range(0x2, 0x25)')
        if base == self.base: return self
        number = abs(float(self))
        if number == 0: return basenum('0', base)
        if base == 10: return basenum(str(validation.trynumber(self)))
        strint, n, p = "", 0, 0
        if number >= 1:
            while (base**n)<= number: n+=1
            n-=1
        while number > 0:
            if n == -1: strint += '.'
            elif n < -16: break
            value = base**n
            digit = int(number//value)
            strdigit = str(digit)
            if digit >= 10: strdigit = chr(ord('a')+(digit-10))
            strint += strdigit
            number -= (value*digit)
            n-=1
        if n >= 0: strint += '0'*(n+1)
        if self.Negative: strint = '-'+strint
        return basenum(strint, base)

    def __add__(self, other):
        '''return self+other'''
        decanum = float(self) + float(other)
        floatbase = basenum(str(decanum))
        basenumb = (floatbase.convert(self.base))
        return basenumb

    def __radd__(other, self):
        '''return self+other'''
        return validation.tryint(float(self)+float(other))

    def __mul__(self, other):
        '''return self*other'''
        decanum = float(self) * float(other)
        floatbase = basenum(str(decanum))
        basenumb = (floatbase.convert(self.base))
        return basenumb


    def __rmul__(other, self):
        '''return self*other'''
        return validation.tryint(float(self)*float(other))

    def __sub__(self, other):
        '''return self-other'''
        decanum = float(self) - float(other)
        floatbase = basenum(str(decanum))
        basenumb = (floatbase.convert(self.base))
        return basenumb

    def __rsub__(other, self):
        '''return self-other'''
        return validation.tryint(float(self)-float(other))

    def __truediv__(self, other):
        '''return self/other'''
        decanum = float(self)/float(other)
        floatbase = basenum(str(decanum))
        basenumb = (floatbase.convert(self.base))
        return basenumb

    def __rtruediv__(other, self):
        '''return self/other'''
        return validation.tryint(float(self)/float(other))

    def __lt__(self, other):
        '''return self<other'''
        return float(self)<float(other)

    def __gt__(self, other):
        '''return self>other'''
        return float(self)>float(other)

    def __le__(self, other):
        '''return self<=other'''
        return float(self)<=float(other)

    def __ge__(self, other):
        '''return self>=other'''
        return float(self)>=float(other)

    def __eq__(self, other):
        '''return self==other'''
        return float(self)==float(other)

    def __ne__(self, other):
        '''return self!=other'''
        return float(self)!=float(other)

    def __repr__(self):
        '''IDLE representation'''
        return str(self)

pi = π = pi #! π, ratio of diameter to circumference in circle
tau = τ = tau #! τ, ratio of diameter to circumference in circle
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

class irrational(object):
    '''represents irrational number for expression'''
    
    conversions = {'pi': π, 'π': π, 'τ': τ, 'tau': τ, 'e': e}
    def __init__(self, value):
        if value == 'pi': value = 'π'
        if value == 'tau': value = 'τ'
        self.name = None
        if type(value) == str: value = validation.tryfloat(value)
        if type(value) == str:
            self.name, self.value = value
            irrational.conversions[name]
        elif type(value) in (float, int, num, basenum): self.value = value
        else: raise ValueError

    def __float__(self): return float(self.value)

    def __int__(self): return int(self.value)

    def __abs__(self): return float(self.value)

    def __lt__(self, other): return float(self)<float(other)

    def __gt__(self, other): return float(self)>float(other)

    def __le__(self, other): return float(self)<=float(other)

    def __ge__(self, other): return float(self)>=float(other)

    def __eq__(self, other): return float(self)==float(other)

    def __ne__(self, other): return float(self)!=float(other)

    def __str__(self): return str(self.value)

def prepare(text):
    text = text.replace(' ', '')
    while '--' in text: text = text.replace('--', '+')
    while '++' in text: text = text.replace('++', '+')
    while '+-' in text: text = text.replace('+-', '-')
    while '-+' in text: text = text.replace('-+', '-')
    text = text.replace('**', '^')
    if text[1:5]==('(x)='): text = text[5:]
    text = translate(text, translations)
    ntext = ''
    fn = False
    for x in text:
        if fn:
            if x == ' ': fn = False
            if x in digits: ntext += ' ' + x
            else: ntext += x
        else:
            if x in ('\\', '\x0e'):
                ntext += x
                fn = True
            elif x not in digits: ntext += ' '+x+' '
            else: ntext+= x
    if text.startswith('-'): text+='0 '
    text = (ntext+' ').replace('  ', ' ')
    return text

class eq(object):
    def __init__(self, text):
        #creates a function from text that can be solved for a single variable
        #while slow compared to a regular function, it has the ability to create
        #this from *input* which is what makes it useful
        parameter = None
        if '"' in text:
            index = text.index('"')
            text = text[:index]
            del index
        if '{' in text:
            index = text.index('{')
            text, parameter = text[:index], text[index:]
            del index
        self.text = text+' '
        self.ParameterText = parameter
        self.parameter = self.makeParameter()
        self.neq = self.makeEq()
        self.solved = False
        self.value = None
        if self.var is None:
            self.value = self.solve(0)
            self.solved = True

    def makeParameter(self): return NotImplemented #Working on it

    def __eq__(self, other):
        if type(other) != self.__class__: return False
        return self.neq == other.neq

    def makeEq(self):
        text = self.text
        if text.count('(') != text.count(')'): raise SyntaxError('Parenthesis nesting error occured')
        nlist = []
        runstr = ''
        depth = 0
        var = None
        inner = False
        fn = False
        na = 'na' #To avoid errors regarding '-' placed first
        prevtype = na #To avoid 'implied multiplication' leading to errors
        num = 'num' #support for prevtype
        oper = 'oper'#support for prevtype
        va = 'var' #support for prevtype
        f = 'fn'#support for prevtype
        c = 'special'#support for prevtype
        nprev = None
        for char in text:
            l = runstr
            if depth == 0:
                if char == ')': raise SyntaxError('Parenthesis nesting error occured')
                elif char == '(':
                    depth += 1; prevtype = na
                    nlist.append(runstr); runstr = '('
                elif char == ' ':
                    if runstr != '':
                        if is_float(runstr): curtype = num
                        elif runstr in operations: curtype = oper
                        elif runstr.startswith('\\'): curtype = f
                        elif runstr.startswith('\x0e'): curtype = c
                        else:
                            if var == None:
                                if runstr.startswith('-'):
                                    var = runstr[1:]
                                else:
                                    var = runstr
                                curtype = va
                            elif runstr == var: curtype = va
                            else: raise SyntaxError(var + ' seems to be an invalid character')
                        if prevtype in (va, num, c):
                            if curtype == oper: pass
                            else: nlist.append(implied)
                        if runstr == '-' and prevtype == na: pass
                        elif runstr == '-' and prevtype == oper: pass
                        else: nlist.append(tryint(tryfloat(runstr))); runstr = ''
                        prevtype = curtype
                        if fn: fn = False
                elif char == '\\' or char == '\x0e':
                    fn = True
                    if runstr != '':
                        if is_float(runstr): curtype = num
                        elif runstr in operations: curtype = oper
                        elif runstr.startswith('\\'): curtype = f
                        elif runstr.startswith('\x0e'): curtype = c
                        else:
                            if var == None:
                                if runstr.startswith('-'):
                                    var = runstr[1:]
                                else:
                                    var = runstr
                                curtype = va
                            elif runstr == var: curtype = va
                            else: raise SyntaxError(var + ' seems to be an invalid character')
                        if prevtype in (va, num, c):
                            if curtype == oper: pass
                            else: nlist.append(implied)
                        prevtype = curtype
                    nlist.append(tryint(tryfloat(runstr)))
                    runstr = char
                elif fn: runstr += char
                elif char in operations: runstr = char
                else:
                    if runstr == '': runstr += char
                    elif is_float(runstr) or runstr == '-' or runstr == '.' or runstr == '-.':
                        if is_float(char) or char == '.':
                            runstr += char
                        elif runstr == '-':
                            runstr += char
                        else:
                            nlist.append(tryint(tryfloat(runstr)))
                            nlist.append(implied)
                            runstr = char
                    elif is_float(char):
                        nlist.append(tryint(tryfloat(runstr)))
                        nlist.append(implied)
                        runstr = char
                    else: runstr += char
            else:
                runstr += char
                if char == ')': depth -= 1
                elif char == '(': depth += 1
                if depth == 0:
                    ceq = eq(runstr[1:-1])
                    if ceq.solved: ceq = ceq.value
                    elif var == None: var = ceq.var
                    else:
                        if ceq.var != var: raise SyntaxError(ceq.var + ' seems to be an invalid character')
                    nlist.append(ceq)
                    runstr = ''
            nprev = l
        self.var = var
        if nlist[0] == '+': nlist = nlist[1:]
        nlist = scour(nlist)
        return nlist

    def __repr__(self):
        if self.solved: return str(self.value)
        return str(self.neq)

    def solve(self, value):
        if self.solved: return self.value
        Nlist = self.neq.copy()
        def s(Nlist):
            count = 0
            for x in Nlist.copy():
                if self.var != None:
                    if x == self.var:
                        Nlist[count] = value
                    if x == ('-'+self.var):
                        Nlist[count] = 0-value
                if type(x) == str:
                    if x in constants:
                        Nlist[count] = constants[x]
                count += 1
            return Nlist
        def p(Nlist):
            count = 0
            for x in Nlist.copy():
                if type(x) is self.__class__:
                    Nlist[count] = x.solve(value)
                count +=1
            return Nlist
        def imp(Nlist):
            while (implied in Nlist):
                prev1 = ''
                prev2 = ''
                count = 1
                for x in Nlist.copy():
                    if prev1 == implied:
                        if is_float(prev2) and is_float(x):
                            Nlist[count-3:count] = [prev2*x]
                            break
                        else: pass
                    prev2 = prev1
                    prev1 = x
                    count +=1
                else: break
            return Nlist
        def f(Nlist):
            #see mathfuncs
            def done(Nlist):
                for x in Nlist:
                    if (type(x) is str) and (x.startswith('\\')):
                        return False
            while not done(Nlist):
                index = 0
                for x in Nlist.copy():
                    if (type(x) is str) and (x.startswith('\\')):
                        if Nlist[index+1] == '^':
                            Nlist.pop(index+1)
                            power = Nlist.pop(index+1)
                        else: power = 1
                        funcdata = mathfuncs[x]
                        fx = funcdata[0]
                        pardata = funcdata[1]
                        args = []
                        
                        
                        for datum in pardata:
                            args.append(Nlist[index+datum])
                        nvalue = fx(*args)
                        pardata = list(pardata)
                        pardata.append(0)
                        spacer = (min(pardata), max(pardata))
                        Nlist[index+spacer[0]:1+index+spacer[1]] = [nvalue**power]
                    index +=1
                else:
                    break
            return Nlist
        def e(Nlist):
            while '^' in Nlist:
                prev1 = ''
                prev2 = ''
                count = 1
                for x in Nlist.copy():
                    if prev1 == '^':
                        Nlist[count-3:count] = [prev2**x]
                        break
                    prev2 = prev1
                    prev1 = x
                    count +=1
                else: break
            return Nlist
        def m(Nlist):
            while ('*' in Nlist) or ('/' in Nlist) or (implied in Nlist):
                prev1 = ''
                prev2 = ''
                count = 1
                for x in Nlist.copy():
                    if prev1 == '*' or prev1 == implied:
                        Nlist[count-3:count] = [prev2*x]
                        break
                    elif prev1 == '/':
                        Nlist[count-3:count] = [prev2/x]
                        break
                    prev2 = prev1
                    prev1 = x
                    count +=1
                else: break
            return Nlist
        def a(Nlist):
            while ('+' in Nlist) or ('-' in Nlist):
                prev1 = ''
                prev2 = ''
                count = 1
                for x in Nlist.copy():
                    if prev1 == '+':
                        Nlist[count-3:count] = [prev2+x]
                        break
                    elif prev1 == '-':
                        Nlist[count-3:count] = [prev2-x]
                        break
                    prev2 = prev1
                    prev1 = x
                    count +=1
                else: break
            return Nlist
        OOP = 'spifema'
        oop = {'s': s, 'p':p, 'f':f, 'i': imp, 'e':e, 'm': m, 'a':a}
        for op in OOP:
            Nlist = oop[op](Nlist)
        if len(Nlist)==1:
            return Nlist[0]
        else:
            raise ValueError(Nlist)

def create(text): return eq(prepare(text))
hasbeenwarned1 = False
def WarnOnce1():
    global hasbeenwarned1
    if not hasbeenwarned1:
        warnings.warn(NotImplementedError('var class is in progress: expect errors and bugs'))
        hasbeenwarned1 = True
class var(object):
    '''represents a variable'''
    names ={}
    def __init__(self, name, value = None):
        WarnOnce1()
        if type(name) != str: raise TypeError
        if len(name) != 1: raise ValueError
        if value != None:
            if validation.is_float(value):
                value = validation.tryint(float(value))
                if type(value) == float: value = expression(value)
            else: raise FloatingPointError
        self.name = name
        self.solved = value != None
        self.value = value
        if not self.solved:
            if self.name in self.names:
                if self.names[self.name] == None: return
                self.solved = True
                self.value = self.names[self.name]
            else:
                self.names[self.name] = self.value
        if self.solved:
            if self.name in self.names:
                if self.names[self.name] == None:
                    self.names[self.name] = self.value
                elif self.names[self.name] == self.value: pass
                else: raise ArithmeticError
            else: self.names[self.name] = self.value

    def assign(self, value):
        WarnOnce1()
        if self.solved: raise AttributeError
        if value != None:
            if is_float(value):
                value = validation.tryint(float(value))
                if type(value) == float: value = expression(value)
            else: raise FloatingPointError
        self.value = value
        self.solved = True

    def __float__(self):
        WarnOnce1()
        return float(self.value)

    def __int__(self):
        WarnOnce1()
        return int(self.value)

    def __abs__(self):
        WarnOnce1()
        return abs(float(self.value))

    def __str__(self):
        WarnOnce1()
        return str(self.name)

    def __lt__(self, other):
        WarnOnce1()
        return float(self)<float(other)

    def __gt__(self, other):
        WarnOnce1()
        return float(self)>float(other)

    def __le__(self, other):
        WarnOnce1()
        return float(self)<=float(other)

    def __ge__(self, other):
        WarnOnce1()
        return float(self)>=float(other)

    def __eq__(self, other):
        WarnOnce1()
        try: return float(self)==float(other)
        except: return self.name == other.name

    def __ne__(self, other):
        WarnOnce1()
        try: return float(self)!=float(other)
        except: return False

    def __repr__(self):
        WarnOnce1()
        return str(self)

    def Value(self):
        WarnOnce1()
        if not self.solved:
            if self.name in self.names:
                if self.names[self.name] == None: return
                self.solved = True
                self.value = self.names[self.name]
            else:
                self.names[self.name] = self.value
        return self.value

hasbeenwarned2 = False
def WarnOnce2():
    global hasbeenwarned2
    if not hasbeenwarned2:
        warnings.warn(NotImplementedError('Expression class is in progress: Expect errors and bugs'))
        hasbeenwarned2 = True

class Expression:

    def is_negative(num):
        WarnOnce2()
        if type(num) == int:
            return 0>num
        if type(num) == quaternion:
            return 0>num.a

    def getTypes():
        WarnOnce2()
        Types = (int, irrational, quaternion, var)
        return Types+Expression.ExpressionTypes

    def acceptType(number):
        WarnOnce2()
        #Possible return types are int, an Expression subtype, var,
        #irrational, and quaternion
        if type(number) == var:
            if number.solved: number = number.value
        if type(number) in Expression.ExpressionTypes:
            if number.__solved__(): return Expression.acceptType(number.value)
        if validation.is_integer(number): return int(number)
        if validation.is_float(number):
            new, times = round(float(number), 13), 1
            while not validation.is_integer(new): times *= 10; new *= 10
            return Expression.divExpression(int(new), times)
        if type(number) == fraction: return Expression.divExpression(number.as_integer_ratio()[0], '/', number.as_integer_ratio()[1])
        if type(number) == complex: return quaternion(first)
        return number
        
    class divExpression(object):
        classname = 'divExpression'
        symbol = '/'
        def __init__(self, numer, denom = 1):
            Types = Expression.getTypes()
            ExpressionTypes = Expression.ExpressionTypes
            numer = Expression.acceptType(numer)
            denom = Expression.acceptType(denom)
            if type(numer) not in Types: raise TypeError
            if type(denom) not in Types: raise TypeError
            self.solved = False
            self.value = None
            self.numer = numer
            self.denom = denom
            self.Types = Types
            self.ExpressionTypes = ExpressionTypes
            self.simplify()

        def simplify(self):
            WarnOnce2()
            if self.denom == self.numer: self.numer, self.denom = 1, 1
            if self.__solved__(): return
            if type(self.denom) is quaternion:
                self.numer = Expression.acceptType(self.numer*self.denom.converse())
                self.denom = Expression.acceptType(self.denom*self.denom.converse())
                ngcd = findgcd(self.denom, self.numer)
                self.numer, self.denom = self.numer//ngcd, self.denom//ngcd
                return
            if type(self.denom) is int is type(self.numer):
                ngcd = gcd(self.denom, self.numer)
                self.numer, self.denom = self.numer//ngcd, self.denom//ngcd
                return
            if type(self.denom) is self.__class__ is type(self.numer):
                nlcf = lcf(self.numer.denom, self.denom.denom)
                self.numer = Expression.acceptType(self.numer*nlcf)
                self.denom = Expression.acceptType(self.denom*nlcf)
                return
            if type(self.denom) is self.__class__:
                nlcf = self.denom.denom
                self.numer = Expression.acceptType(self.numer*nlcf)
                self.denom = Expression.acceptType(self.denom*nlcf)
                return
            if type(self.numer) is self.__class__:
                nlcf = self.numer.denom
                self.numer = Expression.acceptType(self.numer*nlcf)
                self.denom = Expression.acceptType(self.denom*nlcf)
                return
            if type(self.denom) in self.ExpressionTypes:
                #NOT IMPLEMENTED
                # Maybe something like
                #if type(self.numer) in (int, quaternion, var, irrational):
                #   return
                #self.numer.is_divisible_by(self.denom):
                #   self.set(self.numer/self.denom)
                return
            if type(self.denom) in (irrational, var):
                #Not quite worked out
                return

        def __gcd__(self):#IMPLIMENT LATER
            WarnOnce2()
            pass

        def gcd(self, other): #IMPLIMENT LATER
            WarnOnce2()
            pass

        def rgcd(other, self):
            WarnOnce2()
            pass

        def set(self, to):
            WarnOnce2()
            if type(to) is self.__class__:
                self.numer = to.numer
                self.denom = to.denom
                self.solved = to.solved
                self.value = to.value
                return
            self.solved = True
            self.value = to

        def __repr__(self):
            WarnOnce2()
            if self.__solved__():
                return repr(self.value)
            return str(self)

        def __str__(self):
            WarnOnce2()
            self.simplify()
            def center(multistring, linelen):
                newlist = []
                for line in multistring.split('\n'):
                    newlist.append(line.center(linelen))
                return '\n'.join(newlist)
            if self.__solved__(): return str(self.value)
            top = str(self.numer)
            bottom = str(self.denom)
            toplen = max(list(map(len, top.split('\n'))))
            bottomlen = max(list(map(len, bottom.split('\n'))))
            linelen = max(toplen, bottomlen)+2
            top = center(top, linelen)
            bottom = center(bottom, linelen)
            return top + '\n' + ('–'*linelen) + '\n' + bottom

        def reciprocal(self):
            WarnOnce2()
            return self.__class__(self.denom, self.numer)

        def __mul__(self, other):
            WarnOnce2()
            other = Expression.acceptType(other)
            if self.solved: return other*self.value
            if type(other) in self.ExpressionTypes:
                return self.__class__(other*self.numer, self.denom)
            return self.__class__(self.numer*other, self.denom)

        def __add__(self, other):
            WarnOnce2()
            if self.solved: return self.value+other
            other = Expression.acceptType(other)
            if type(other) in (int, quaternion) and type(self.numer) == int: other = self.__class__(other)
            if type(other) not in self.Types: raise TypeError
            if type(other) is self.__class__: return self.__class__(((self.numer * other.denom) + (other.numer * self.denom)), (self.denom*other.denom))
            answer = Expression.addExpression(self, other)
            if answer.solved(): return answer.value
            return answer

        def __radd__(other, self):
            WarnOnce2()
            return other+self

        def __sub__(self, other):
            WarnOnce2()
            return self + (other*-1)

        def __rsub__(other, self):
            WarnOnce2()
            return (other*-1)+self

        def __truediv__(self, other):
            WarnOnce2()
            return self*(self.__class__(other).reciprocal())

        def __solved__(self):
            WarnOnce2()
            if self.solved: return self.solved
            if self.denom == 1: self.set(self.numer)
            return self.solved

    class addExpression(object):
        classname = 'addExpression'
        symbol = '+'
        def __init__(self, *terms):
            WarnOnce2()
            if len(terms) == 0: raise TypeError
            self.Types = Expression.getTypes()
            self.ExpressionTypes = Expression.ExpressionTypes
            termlist = list(map(Expression.acceptType, terms))
            for term in termlist:
                if type(term) not in self.Types: raise TypeError
            self.terms = termlist
            self.solved = False
            self.value = None
            self.simplify()

        def simplify(self):
            WarnOnce2()
            ncount = 0
            terms = self.terms.copy()
            newterms = []
            while terms:
                current = terms.pop(ncount)
                tcount = 0
                while tcount < len(terms):
                    try:
                        current += terms[tcount]
                        terms.pop(tcount)
                    except:
                        try:
                            current = terms[tcount] + current
                            terms.pop(tcount)
                        except:
                            tcount += 1
                newterms.append(current)
            terms = newterms
            if len(terms) == 1:
                self.solved = True
                self.value = terms[0]
            self.terms = terms

        def __gcd__(self):
            WarnOnce2()
            return findgcd(*self.terms)

        def __str__(self):
            WarnOnce2()
            #TEMPORARY: Doesn't work:must work on multi-line string concatenator
            if self.__solved__(): return str(self.value)
            return ' + '.join(list(map(str, self.terms)))

        def __repr__(self):
            WarnOnce2()
            if self.__solved__(): return str(self.value)
            return str(self.terms) #Also temporary

        def __solved__(self):
            WarnOnce2()
            if self.solved: return self.solved
            if len(self.terms) == 1:
                self.solved = True
                self.value = self.terms[0]
            return self.solved

        def __add__(self, other):
            WarnOnce2()
            other = Expression.acceptType(other)
            if self.solved: return self.__class__(self.value, other)
            if type(other) == self.__class__:
                return self.__class__(*(self.terms + other.terms))
            else:
                nterms = self.terms.copy()
                nterms.append(other)
                return self.__class__(*nterms)

    class mulExpression(object):
        classname = 'mulExpression'
        symbol = '*'
        def __init__(self, *terms):
            raise NotImplementedError(repr(self.__class__) + 'has not been implemented yet')

    class expExpression(object):
        classname = 'expExpression'
        symbol = '^'
        def __init__ (self, base, power = 1):
            raise NotImplementedError(repr(self.__class__) + 'has not been implemented yet')

    class rootExpression(object):
        classname = 'rootExpression'
        symbol = 'rt'
        def __init__(self, base, root = 1):
            raise NotImplementedError(repr(self.__class__)  + 'has not been implemented yet')

    class logExpression(object):
        classname = 'logExpression'
        symbol = 'log'
        def __init__(self, number, base = 10):
            raise NotImplementedError(repr(self.__class__) + 'has not been implemented yet')

    class cosExpression(object):
        classname = 'cosExpression'
        symbol = 'cos'
        def __init__(self, angle):
            raise NotImplementedError(repr(self.__class__)  + 'has not been implemented yet')

    class sinExpression(object):
        classname = 'sinExpression'
        symbol = 'sin'
        def __init__(self, angle):
            raise NotImplementedError(repr(self.__class__)  + 'has not been implemented yet')

    class tanExpression(object):
        classname = 'tanExpression'
        symbol = 'tan'
        def __init__(self, angle):
            raise NotImplementedError(repr(self.__class__) + 'has not been implemented yet')

    class lnExpression(object):
        classname = 'lnExpression'
        symbol = 'ln'
        def __init__(self, number):
            raise NotImplementedError(repr(self.__class__) + 'has not been implemented yet')

    ExpressionTypes = (divExpression, addExpression)
    varTypes = (var, irrational)
