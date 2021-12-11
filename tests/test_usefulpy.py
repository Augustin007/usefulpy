from usefulpy import *
import pytest


### VALIDATION TEST ###

### MATHEMATICS TEST ###

## Basenum ##
def test_basenumlessthanten():
    test = mathematics.basenum('---1010', 2)
    assert test.base == 2
    assert test.num == '1010'
    assert test.floatpart == ''
    assert test.Negative == True

def test_basenumlessthanten1():
    test = mathematics.basenum('1010.1', 3)
    assert test.base == 3
    assert test.num == '1010'
    assert test.floatpart == '1'
    assert test.Negative == False

## Mathfuncs ##

## nmath ##

## vector ##


### FORMATTING TEST ###

### PY3d TEST ###

