import pytest
from usefulpy import mathematics

### MATHEMATICS TEST ###

## Basenum ##
def test_basenumlessthanten():
    test = mathematics.basenum('---1010', 2)
    assert test.base == 2
    assert test.num == '1010'
    assert test.floatpart == ''
    assert test.Negative

def test_basenumlessthanten1():
    test = mathematics.basenum('1010.1', 3)
    assert test.base == 3
    assert test.num == '1010'
    assert test.floatpart == '1'
    assert not test.Negative

## Mathfuncs ##
def test_mathfunc_add():
    cos = mathematics.cos
    x = mathematics.x
    assert cos(x)+cos(x) == 2*cos(x)

def test_mathfunc_sub():
    x = mathematics.x
    assert x-x == 0

def test_mathfunc_mul():
    x = mathematics.x
    cos = mathematics.cos
    assert x*x == x**2
    assert (x+cos(x))*x == x**2+x*cos(x)

def test_mathfunc_derivative():
    x = mathematics.x
    tetra = x**x
    assert tetra.partial(x) == (x**x+mathematics.ln(x)*(x**x))

## nmath ##
def test_primality():
    assert mathematics.Prime(9999999999998999999999)
    assert not mathematics.Prime(9999999999999000000000)

## vector ##
def test_vector():
    v = mathematics.vector
    v1 = v(1, 2)
    assert tuple(2*v1) == (2, 4)
    m = mathematics.matrix
    m1 = m(v(0, -1), v(1, 0))
    assert tuple(m1*v1) == (2, -1)

## Interval ##
def test_interval():
    interval = mathematics.interval
    i1 = interval(0, 1, 2)
    i2 = interval(1, 2, 2)
    assert 1 in i2
    assert 1.1 in i2
    assert 2 not in i2
    assert 0.9 not in i2
    assert 2.1 not in i2
    i3 = i1 | i2
    assert 0 in i3
    assert 1 in i3
    assert 2 not in i3
    assert -1 not in i3
    assert 2.1 not in i3
    i4 = i3 ^ interval(-1, 0, 1)
    assert 0 not in i4
    assert -0.5 in i4
    assert -1 not in i4
    assert -1.1 not in i4
    assert 1 in i4
    assert 2 not in i4
    assert 2.1 not in i4

## Quaternion ##
def test_quaternion():
    ...

# eof
