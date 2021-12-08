# Usefulpy

![Usefulpy Logo](https://github.com/Augustin007/Augustin007/raw/main/UsefulPY_with_quote.png)

[Check out the Usefulpy site](https://augustin007.github.io/usefulpy/)

_Usefulpy site is not always up to date_

## Download and Import

download and install with with 
```
pip download usefulpython
pip install usefulpython
```

import with `import usefulpy`

## Description

Filled with simple resources and modules for a cleaner looking program, Usefulpy is a module filled with many useful functions and modules in various subjects geared to cut down and simplify some little bits of code that can become messy or repetitive.

Some are simple - like input validation and versatile type checking.

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

Other parts of the project are a little more complicated, including 

quaternions
```python
>>> from usefulpy.mathematics import quaternions
```
```
>>> quaternion(1, 2, 2, 2)
1+2i+2j+2k
>>> _*quaternion(2, 1, 1, 1)
-4+5i+5j+5k
>>> 
```

Prime sieves
```python
>>> from usefulpy.mathematics import Prime
>>> import timeit
>>> timeit.timeit('Prime(9999999999998999999999)', number = 1000, globals=globals())/1000
0.02101861490000738
timeit.timeit('Prime(9999999999998999999999)', number = 1, globals=globals())
0.020142099994700402
>>> Prime(9999999999998999999999)
True
```

Basic algebraic simplifier and derivative finder
```python
>>> from usefulpy.mathematics import cos, x
>>> x+x
<mathfunc x*2 at 0x3a129d0>
>>> x*x
<mathfunc x**2 at 0x3a30100>
>>> x**x
<mathfunc x**x at 0x3a30118>
>>> _.derivative()
<mathfunc x**x+ln(x)*(x**x) at 0x3ca09a0>
>>> cos*2 == cos+cos
True
>>> 
```

3d projection systems

(This does break about five times a day, still in it's early stages)

![Rotating Cube](https://github.com/Augustin007/Augustin007/raw/main/Cube_rot.gif)

\
Essentially, usefulpy is a large library of functions that improve the quality of python programming. One catch, it can't use any sort of third party libraries... so no numpy, scipy, manim, or any others... 


![mini_usefulpy_logo](https://github.com/Augustin007/Augustin007/raw/main/Mini_usefulpy.png)
