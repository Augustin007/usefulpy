import pytest
from usefulpy import mathematics, formatting, validation

def test_sieve():
    assert mathematics.Prime(99999989)
    assert mathematics.Composite(999999899)

def test_factors():
    assert mathematics.Factor(88359991)==(9397, 9403)