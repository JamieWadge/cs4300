from src import task4

#Tests if two integers is correct
def test_integer_price_integer_discount():
    assert task4.calculate_discount(100, 10) == 90

#Tests if one integer and one float is correct
def test_integer_price_float_discount():
    assert task4.calculate_discount(100, 33.3) == 66.7

#Tests if one float and one integer is correct
def test_float_price_integer_dicsount():
    assert task4.calculate_discount(50.5, 10) == 45.45

#Tests if two floats is correct
def test_float_price_float_discount():
    assert task4.calculate_discount(50.5, 33.3) == 33.6835