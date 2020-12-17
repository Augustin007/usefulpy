# Usefulpy
Filled with simple resources and modules for a cleaner looking program, Usefulpy is a module filled with many useful functions and modules in various subjects geared to cut down and simplify some little bits of code that can become messy or repetitive.

So instead of checking, say
```python
float(x) == int(float(x))
```

You can check it as
```python
is_integer(x)
```

Which calls 
```python
def is_integer(s):
    '''Check if an object is an integer can be turned into an integer without
losing any value'''
    try: return int(float(s)) == float(s)
    except: return False
```

Simple, but works well and can be used in a variety of situations. This also allows you to quickly write the check without having to go back and make a module, interupting your flow of thought; or without marking it down for later creation, and then forget it (happens to me all the time).

While I would recommend getting aquainted with the code by sifting through it by hand, here is a quick introduction:

## validation
Validation includes various tools for getting input and preparing clean output, as well quick checks for types.

_note: it imports the_ `datetime` _module, as well as namedtuple and deque from the_ `collections` _module_ 

#### Integer/Float Tools:
 - `is_integer`/`is_float`: return `True` if s is an integer/float or can be converted into one.
 - `intinput`/`floatinput`: continue to ask for input until input is an integer/float... Useless in a gui environment but useful in shell scripts
 - `tryint`/`tryfloat`: converts to an integer if `is_integer`/`is_float`
 - `trynumber`: `tryfloat(tryint(s))`
 - `is_intlist`/`is_floatlist`: checks if a list or a string with spaces is composed only of integers/floats.
 - `intlistinput`/`floatlistinput`: continues to ask for input until input can be converted to a list of integers/floats

#### Simple randomizers:
 - `lowbias`/`highbias`/`centerbias`/`outerbias`: random number biased towards the lower/higher/central/outer numbers
 - `rbool`/`truebias`/`falsebias`: return a random bool, not biased or biased to `True` or `False`

#### Custumizable Tools:
 - `validquery`: return `True` if an object can be converted to a type.
 - `validinput`: continue asking for input until the input can be converted to a certain type. This can be used for multiple inputs at once. It has a lot of possible arguments.
 - `trytype`: converts something to a type if `validquery` for the object and the type returns `True`

#### Other Tools:
 - `YesOrNo`: return `True` or `False` for most variations of yes and no: returns `None` otherwise.
 - `getYesOrNo`: take inputs until `YesOrNo` returns either `True` or `False`
 - `fromrepr`: is meant to be the inverse of `repr`
 - `makelist`: makelist makes a list from any sort of input, including from the str version of a list, (so `makelist('[1, [1, 2]]')` returns `[1, [1, 2]]`this works well with any sort of iterable, but many non-iterables wind up being a list with a single value, 
 - `validdate`: return `True` if input numbers form a valid date
 - `isbool`: return `type(s)==bool`
 - `is_function`: returns `True` if the object is a function.

## mathematics
### version 1.2.4
Contains a lot of useful mathematical stuff.

_note: imports the_ `math` _and_ `cmath` _modules,_ `fraction.Fraction as fraction`, `decimal.Decimal as num`, `reduce` _from_ `functools`_,_ `validation`_,_ `formatting`_,_ `warnings`_... is that all?_

mathematics is divided into several programs, though `from usefulpy.mathematics import *` imports all of the functions from all of them.
- `nmath`: new math, essentially imports and combines `math` and `cmath` (complex math), adds some more constants, and allows for a radians or degrees setting.
- `triangles`: different functions dealing with triangles, as from `TriangleType` to `LawofCos`.
- `PrimeComposite`: Functions dealing with factoring, gcd, lcm, primes and composites.
- `basenum`: a class that saves numbers in any base counting system.
- `quaternion`: a quaternion class: **In progress**
- `eq`: a class, requires a string argument in a function `create` which returns an object of the class from a string `create('f(s)=s+1')` returns a callable object represented as `(s + 1)`
- `algebraicsolver`: eventually will be able to solve or simplify algebraic expressions **early stages... still in progress**

#### nmath 2.1.1
 - constants: `e`, `pi`/`π`, `tau`/`τ`, `nan`, `inf`, `infj`, `nanj`, `Phi`/`Φ`, `kappa`/`κ`, `rho`/`ρ`, `lsigma`/`ς`, `sigma`/`σ`, `phi`/`φ`, and `psi`/`ψ`
 - `num`/`fraction`: `Decimal.decimal` and `Fraction.fraction` from python built-ins
 - `makefraction`: creates a correct fraction object out of floats
 - `phase`, `polar`, `rect`, `ceil`, `comb`, `copysign`, `dist`, `erf`, `erfc`, `expm1`, `fabs`, `factorial`, `floor`, `fmod`, `frexp`, `fsum`, `gamma`, `hypot`, `ldexp`, `lgamma`, `modf`, `nextafter`, `perm`, `prod`, `remainder`, `trunc`, `ulp`: functions imported directly `math`, `cmath`
 - `sqrt`, `isqrt`, `exp`, `isclose`, `isfinite`, `isinf`, `isnan`, `ln`, `log`: functions that call `math` and `cmath` versions but are modified to work both for real and complex numbers, instead of only one at a time.
 - `RadiansToDegrees`/`DegreesToRadians`: self explanatory
 - `radians`/`degrees`: functions that set the nmath setting to radians or degrees (default is radians)
 - `acos`, `acosh`, `asin`, `asinh`, `atan`, `atanh`, `asec`, `asech`, `acsc`, `acsch`, `acot`, `acoth`, `cos`, `cosh`, `sin`, `sinh`, `tan`, `tanh`, `sec`, `sech`, `csc`, `csch`, `cot`, `coth`, `cis`: Trigonometric functions, work with real and complex numbers, more functions than available with math and cmath and closer responses for quarter circles. 
 - `rt`, `irt`, `cbrt`, `icbrt`: root functions not in `math` and `cmath`
 - `odd`/`even`: return `True` if number is odd or even.
 - `summation`/`Σ`/`Sigma`: Summation

#### triangles 1.1.2
 - `isTriangle`: Checks whether a triangle can be formed out of three side lengths.
 - `TriangelType`/`AngleType`: returns the type of triangle/angle
 - `LawofCos`/`LawofSin`: Use the law of cos/sin to determine the missing argument.
 - `Heron`: Uses Heron's formula to get area of triangle.

#### PrimeComposite 1.1.1
 - `PrimeOrComposite`: return `'Prime'` and `'Composite'`
 - `Prime`/`Composite`: return `True` if prime/composite
 - `factor`: return a list containing the factors of any given number
 - `lcm`: least common multiple
 - `gcd`/`gcd2`/`findgcd`: use `gcd` for most cases, `gcd2` is meant to work with more classes, but isn't wuite developed, `findgcd` is for a larger number of arguments.


#### basenum 1.1.2
A basenum class:
```python
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
>>> basenum('101', 2)
101₂
>>> _.convert(4)
11₄
>>> _+basenum('10.1', 2)
13.2₄
>>> float(_)
7.5
>>> 
```

#### quaternion 1.3.1
A quaternion class:
```python
>>> quaternion(1, 2, 3, 4)
(1+2i+3j+4k)
>>> quaternion(1+3j)
(1+3i)
>>> 
```

#### eq 2.2.1
This program stores the 'eq' class. It takes a string of an expression of a
function and returns an 'eq' object, which can be called with a number which
replaces the variable with a number.

Note: I originally created this for a specific sceneario in a graphing program
I created that used this to make a turtle graph an input equation. While I am
sure that there are other practical uses for this, some areas are only develope
as necessary within the original program, though I have attempted to broaden its
abilities.

#### algebraicsolver 
_Algebraic expressions/algebraic simplification_ ***Work in progress.*** 

## formatting
### version 1.2.3

#### Data
- `vowels`: a string with all the vowels
- `endingpuncuation`/`phrasepuncuation`/`inwordpunctuation`: strings containing punctuation marks
- `greek_letters`: a dictionary containing written out greek letters and their character counterparts
- `subscript`: a dictionary with subscript number characters.
- `colors`(`colors.fg`/`colors.bg`): Data for character formatting.


#### Functions
- `cap`: Yes, I am aware there is a similar method for str, which capitalizes the first character and lowercases the rest, this one only capitalizes the first
- `punctuate`: adds a punctuation and strips of old punctuation
- `a_an`: returns `'a'` or `'an'` depending on the nextword argument
- `translate`/`scour`: translate .replaces a string with all keys in a list, scour removes all instances of something in a list/str
- `write`/`ComposeNumber`/`syllables`/`unformat`: write adds commas to string numbers, syllables counts syllables in a word/phrase, compose number writes out an input integer (`ComposeNumber(100)` returns `'one hundred'`, unformat .lowers the text, replaces any written out greek letters (for example: pi with π) or written out numbers (`unformat('two hundred forty three thousand six hundred twelve')` returns `'243612'`.

#### Multline class
Formatting includes a `multline` class, still a bit confusing and in its early stages but, in theory, cocinate and deal with strings that can span various lines as if they were single line 
in theory:
```
' 3 '   '12'   ' 3 12'
'---' + '--' = '-----'
' 4 '   '13'   ' 4 13'
```
(of course, in the IDLE this would look different)

## Versions

###### [Usefulpy 1.1.1](https://github.com/Augustin007/usefulpy/releases/tag/1.1.1):
A series of simple functions, data, and programs to make code cleaner
- validation 1.1.2
- formatting 1.2.2
- mathematics 1.1.3

###### [Usefulpy 1.1.2](https://github.com/Augustin007/usefulpy/releases/tag/v1.1.2):
These are all simple functions that pop up a lot in programming geared to cut down a lot of the little bits of code that can become quite messy and repetitive.
Most changes are to the mathematics section.
- validation 1.1.2
- formatting 1.2.2
- mathematics 1.2.3
  - nmath 1.1.2
  - triangles 1.1.2
  - PrimeComposite 1.1.1
  - eq 2.1.5
  - algebraicsolver pr 5 (1.1.1)
  - quaternion 1.2.2
