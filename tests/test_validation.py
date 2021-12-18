import pytest
from usefulpy import validation

def test_YesOrNo_true():
    assert validation.YesOrNo('y')
    assert validation.YesOrNo('yes')
    assert validation.YesOrNo('yeah')
    assert validation.YesOrNo('of course')
    assert validation.YesOrNo('Why not')
    assert validation.YesOrNo('sure')

def test_YesOrNo_false():
    assert not validation.YesOrNo('n')
    assert not validation.YesOrNo('no')
    assert not validation.YesOrNo('nope')

def test_are_floats():
    assert validation.are_floats(1, '1.0', 1.1, 1.0)
    assert not validation.are_floats(1, '1.0', 1.1, 1.0, 'hello')

def test_are_integers():
    assert validation.are_integers(1, '1.0', 1.0)
    assert not validation.are_integers(1.1, 1, 2)

def test_is_integer():
    assert validation.is_integer('1')
    assert validation.is_integer('1.0')
    assert validation.is_integer(1)
    assert validation.is_integer(1.0)
    assert not validation.is_integer(1.1)
    assert not validation.is_integer('hello')
    assert not validation.is_integer('1.2')

def test_is_float():
    assert validation.is_float('1')
    assert validation.is_float('1.0')
    assert validation.is_float(1)
    assert validation.is_float(1.0)
    assert validation.is_float(1.1)
    assert not validation.is_float('hello')
    assert validation.is_float('1.2')