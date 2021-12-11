from usefulpy import *
import pytest


def test_basenum_init():
    ...

def test_basenumlessthanten():
    test = mathematics.basenum('---1010', 2)
    assert test.base == 2
    assert test.num == '1010'
    assert test.floatpart == ''
    assert test.pos == False

def test_basenumlessthanten():
    test = mathematics.basenum('1010.1', 3)
    assert test.base == 3
    assert test.num == '1010'
    assert test.floatpart == '1'
    assert test.pos == True


