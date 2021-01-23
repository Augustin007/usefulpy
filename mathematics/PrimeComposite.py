'''
File: PrimeComposite.py
Version: 1.1.1
Author: Austin Garcia

Several functions to do with gcd, lcf, and numbers being prime or composite.

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
   Basenum class can hold a number in a certain counting system

'''
##UPDATEME: Unreviewed for Usefulpy 1.2.1
__author__ = 'Austin Garcia'
__version__ = '1.1.1'

try: from nmath import *
except: from usefulpy.mathematics.nmath import *

from usefulpy import validation as _validation

from math import gcd

_primes = [2]
_composites = []
def PrimeOrComposite(num):
    '''return 'prime' if prime and 'composite' if composite'''
    Prime = 'prime'
    Composite = 'composite'
    if not _validation.is_integer(num): raise TypeError
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

def lcm(a, b):
    '''Return least common multiple of a and b'''
    ngcd = gcd(a, b)
    a, b = a//ngcd, b//ngcd
    return a*b*ngcd

def gcd2(a, b):
    '''return gcd(a, b)'''
    if Expression in (type(a), type(b)):
        if type(a) is Expression: return a.gcd(b)
        return b.gcd(a)
    def acceptable(num):
        if _validation.is_float(num): return abs(_validation.tryint(float(num)))
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

#eof
