import pytest
from src import task2

#Tests whether variable is int float str and bool for corresponding variable

@pytest.mark.parametrize("value, type", [
        (task2.num1, int),
        (task2.num2, float),
        (task2.string, str),
        (task2.boolean, bool),
    ],
)
def test_variable_has_expected_type(value, type):
    assert isinstance(value, type)