# Usefulpy
Filled with simple resources and modules for a cleaner looking program, Usefulpy is a module filled with many useful functions and modules in various subjects geared to cut down and simplify some little bits of code that can become messy or repetitive.

So instead of checking, say
```Python
float(x) == int(float(x))
```

You can check it as
```Python
is_integer(x)
```

Which leads to 
```Python
def is_integer(s):
    '''Check if an object is an integer can be turned into an integer without
losing any value'''
    try: return int(float(s)) == float(s)
    except: return False
```

Simple, but works well and can be used in a variety of situations. This also allows you to quickly write the check without having to go back and make a module, interupting your flow of thought; or without marking it down for later creation, and then forget it (happens to me all the time).

While I would recommend getting aquainted with the code by sifting through it, here is a quick introduction:

## validation
Validation includes various tools for getting input and preparing clean output, as well quick checks for types.

_note: it imports the datetime module, as well as namedtuple and deque from collections_ 

Usable functions in validation: YesOrNo, datetime (_note: datetime can be accessed through validation, but is built into python, and is not by me_), deque (_see note on datetime_), floatinput, floatlistinput, fromrepr, getYesOrNo, intinput, intlistinput, is_float, is_floatlist, is_function, is_integer, is_intlist, isbool, makelist, namedtuple (_see note on datetime_), tryfloat, tryint, trynumber, trytype, validdate, validinput, and validquery

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
### version 1.2.3

Contains a lot of useful mathematical stuff, for

_note, imports the whole math module, two classes from statistics, reduce from functools, imports validation, imports formatting... is that all?_

Useable functions in mathematics: AngleType, Composite, DegreesToRadians, Expression, Heron, LawofCos, LawofSin, Phi, Prime, PrimeOrComposite, RadiansToDegrees, TriangleType, basenum, cbrt, create, e, eq, factor, findgcd, fromNumBaseFormat, fsum, gcd2, i, icbrt, irrational, irt, isTriangle, j, k, kappa, lcf, ln, log, makefraction, phi, pi, pow, prepare, psi, quaternion, rho, rt, sigma, summation, validation, var, Φ, κ, π, ρ, ς, σ, τ, φ, and ψ

Also useable is the entire math module, as well as the statistics Decimal (as num) and Fraction (as fraction)

Includes several constants, variables with both their english and greek names. 
Includes a quaternion class, for using quaternions. 
A basenum class, for working in different number systems. 
Triangle stuff, angles, valid triangle, law of cosines and law of sines functions. 
Prime and composites functions. 
Factoring numbers. 
Least commmon factor functions.

I am constructing an 'expression' class for algebraic expressions... still in progress. 

## formatting
### version 1.2.3

Contains a few stuff for formatting output. (and a few other odds and ends that I'm not very sure how they got there)


Useable functions in formatting: ComposeNumber, Syllables, a_an, cap, colors, endingpuncuation, greek_letters, inwordpunctuation, multline, phrasepuncuation, punctuate, scour, subscript, translate, unformat, validation, vowels, and write

ComposeNumber makes the written version of the number ex:(ComposeNumber(10) returns 'ten')

a_an takes the next word as an argument, and returns 'a' or 'an' as the next word demands.

unformat removes any caps from text. It also takes any written numbers and makes them regular numbers in the text, as well as written greek letters.

scour removes all instances of something from a list or string

write adds commas to numbers.

cap capitalizes the first letter of the input string.

multline is an class in progress that is supposed to cocinate and deal with strings that can span various lines as if they were single line 

so, in theory:

' 3 '   '12'   ' 3 12'

'---' + '--' = '-----'

' 4 '   '13'   ' 4 13'


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
