import pytest
from usefulpy import formatting


def test_compose():
    assert formatting.ComposeNumber(10) == 'ten'
    assert formatting.ComposeNumber(100) == 'one hundred'
    assert formatting.ComposeNumber(12683524647636) == 'twelve trillion six hundred eighty three billion five hundred twenty four million six hundred forty seven thousand six hundred thirty six'