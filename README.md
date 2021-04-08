# Usefulpy

![Usefulpy Logo](https://github.com/Augustin007/Augustin007/blob/main/UsefulPY_with_quote.png)

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


![mini_usefulpy_logo](https://github.com/Augustin007/Augustin007/blob/main/Mini_usefulpy.png)
