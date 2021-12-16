import pytest
from usefulpy import validation


def test_checks():
    assert validation.is_integer('1')
    assert validation.is_integer('1.0')
    assert validation.is_integer(1)
    assert validation.is_integer(1.0)
    assert not validation.is_integer(1.1)
    assert not validation.is_integer('hello')
    assert not validation.is_integer('1.2')
    assert validation.is_float('1')
    assert validation.is_float('1.0')
    assert validation.is_float(1)
    assert validation.is_float(1.0)
    assert validation.is_float(1.1)
    assert not validation.is_float('hello')
    assert validation.is_float('1.2')