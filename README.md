# Usefulpy

![Usefulpy Logo](https://github.com/Augustin007/Augustin007/raw/main/UsefulPY_with_quote.png)

[Check out the Usefulpy site](https://augustin007.github.io/usefulpy/)

(Usefulpy site is not always up to date)

## Download and Import

download and install with with

```console
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

Quaternions

```python
In [1]: from usefulpy.mathematics import quaternion

In [2]: quaternion(1, 2, 2, 2)
Out[2]: 1+2i+2j+2k

In [3]: _ * quaternion(2, 1, 1, 1)
Out[3]: -4+5i+5j+5k
```

Prime sieves

```python
In [1]: from usefulpy.mathematics import Prime

In [2]: import timeit

In [3]: timeit.timeit("Prime(9999999999998999999999)", number=1000, globals=globals()) / 1000 # Average time over 1000 runs.
Out[3]: 0.008421884500188753

In [4]: Prime(9999999999998999999999)
Out[4]: True
```

Basic algebraic simplifier and derivative finder

```python
In [1]: from usefulpy.mathematics import cos, x

In [2]: x + x
Out[2]: <mathfunc (2*x) at 0x20115c616f0>

In [3]: x * x
Out[3]: <mathfunc (x**2) at 0x2011566b0d0>

In [4]: x ** x
Out[4]: <mathfunc (x**x) at 0x20115c62200>

In [5]: _.partial(x)
Out[5]: <mathfunc ((x**x)+(ln(x)*(x**x))) at 0x20116781180>

In [6]: cos(x) * 2 == cos(x) + cos(x)
Out[6]: True
```

And indeed ${\frac{d}{dx}\left[x^{x}\right]}={x^{x}+\ln\left({x}\right)x^{x}}$

3d projection systems

(This does break about five times a day, still in its early stages)

![Rotating Cube](https://github.com/Augustin007/Augustin007/raw/main/Cube_rot.gif)

\
Essentially, usefulpy is a large library of functions that improve the quality of python programming. One catch, it can't use any sort of third party libraries... so no numpy, scipy, manim, or any others...

![mini_usefulpy_logo](https://github.com/Augustin007/Augustin007/raw/main/Mini_usefulpy.png)
