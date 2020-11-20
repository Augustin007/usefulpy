# useful
_A module filled with many useful functions and modules in various subjects._

Simple resources and modules for a cleaner looking program

These are all simple functions that pop up a lot in programming, nothing particularily difficult or brilliant, 
but these cut down a lot of little bits of code that can become quite messy.

While these codes have a long way to go to be perfect, they can be quite helpful

#validation
validation includes various modules for getting input and preparing clean output, as well quick checks for types.

_note: it imports the datetime module, as well as namedtuple and deque from collections_ 

While I would recommend going through the code by hand, a quick introduction

>>> dir(validation)

['YesOrNo', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', '_getinp', '_keyob', 'datetime', 'deque', 'floatinput', 'floatlistinput', 'fromrepr', 'func', 'function', 'getYesOrNo', 'intinput', 'intlistinput', 'is_float', 'is_floatlist', 'is_function', 'is_integer', 'is_intlist', 'isbool', 'makelist', 'namedtuple', 'tryfloat', 'tryint', 'trynumber', 'trytype', 'validdate', 'validinput', 'validquery']

makelist makes a list from any sort of input, this works well with any sort of iterable, but non-iterables usually wind up being a list with a single value, 

is_intlist checks if an input is a list of integers... this includes a single integer, a string containing integers spaced out, a file containing integers spaced out, a string in the format of a list, a list, tuple, or other iterable that contains only integers.

is_floatlist does something similar, it takes the same thing, but checks whether the values can be converted to floats.

is_function tests whether a variable is a function.

is_integer checks if an object can be converted to an integer without losing any value

is_float checks if an object can be converted to a float.

isbool checks if type(s) is bool.

fromrepr is supposed to be the opposite of repr, but still needs some work.

tryint converts s into an integer if is_integer(s)

trytype trys to convers an object into a specified type, else returning original value

intinput continues to ask for input until the input is an integer... useless in a gui environment, but quite useful in shell scripts.

etc.

#mathematics
Contains a lot of useful mathematical stuff

_note, imports the whole math module, imports validation_

['AngleType', 'Composite', 'DegreesToRadians', 'Expression', 'Heron', 'LawofCos', 'LawofSin', 'Phi', 'Prime', 'PrimeOrComposite', 'RadiansToDegrees', 'TriangleType', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', '_composites', '_primes', '_reduce', 'acos', 'acosh', 'asin', 'asinh', 'atan', 'atan2', 'atanh', 'basenum', 'cbrt', 'ceil', 'comb', 'copysign', 'cos', 'cosh', 'create', 'degrees', 'dist', 'e', 'eq', 'erf', 'erfc', 'exp', 'expm1', 'fabs', 'factor', 'factorial', 'findgcd', 'floor', 'fmod', 'fraction', 'frexp', 'fromNumBaseFormat', 'fsum', 'gamma', 'gcd', 'gcd2', 'hypot', 'i', 'icbrt', 'inf', 'irrational', 'irt', 'isTriangle', 'isclose', 'isfinite', 'isinf', 'isnan', 'isqrt', 'j', 'k', 'kappa', 'lcf', 'ldexp', 'lgamma', 'ln', 'log', 'log10', 'log1p', 'log2', 'lsigma', 'makefraction', 'modf', 'nan', 'num', 'perm', 'phi', 'pi', 'pow', 'prepare', 'prod', 'psi', 'quaternion', 'radians', 'remainder', 'rho', 'rt', 'sigma', 'sin', 'sinh', 'sqrt', 'summation', 'tan', 'tanh', 'tau', 'trunc', 'validation', 'var', 'Φ', 'κ', 'π', 'ρ', 'ς', 'σ', 'τ', 'φ', 'ψ']

includes several constants, variables with both their english and greek names. includes a quaternion class, for using quaternions. a basenum class, for working in different number systems
Triangle stuff, angles, valid triangle, law of cosines and law of sines functions. 
Prime and composites functions. factoring numbers
least commmon factor functions
