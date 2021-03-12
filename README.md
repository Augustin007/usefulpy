# Usefulpy

[Check out the Usefulpy site](https://augustin007.github.io/usefulpy/)

_Usefulpy site is not always up to date_

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

Simple, but works well and can be used in a variety of situations.

Essentially, usefulpy is a large library of functions that improve the quality of python programming. One catch, it can't use any sort of third party libraries... so no numpy, scipy, manim, or any others... 

# A note on documentation

### Triple quotes:

Triple quotes are only to be used when writing docstrings or long strings, use `#` for multi line commenting

### Comments:

Single `#` for comments, These include comments on how something works, what something is, or a mathematical proof!

from 'quaternion.py'
```python
# My thought process is such:
# e**n = 1+x+x^2/2!+x^3/3!...
# so o**s = e**(ln(o)*s)
num = ln(other)*self
```

from 'validation.py'
```python
#for easier reference of the function type.
function = type(lambda: None)
```


Double `##` for markers that mark something that needs to be done. Additional stuff like `BUG`, `TODO`, or `FIXME` may be there as well.
This is also used for deactivating statements that were only there for the purposes of debuging

from 'quaternion.py'
```python
##TODO: I need to get log/ln for these first...
raise NotImplementedError('Raising quaternions to non-real powers has not been implemented yet')
```

from 'quaternion.py'
```python
##print(a, b, c, d)
```

Triple `###` on each side of the name of a segment of code; these serve to partition the code into several parts. Search for the `###` to find the headers of these sections.

from '__init__.py' for usefulpy
```python
### IMPORTS ###
try: import validation, formatting, mathematics, quickthreads
except: from usefulpy import validation, formatting, mathematics, quickthreads
```
