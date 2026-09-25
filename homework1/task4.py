def calculate_discount(price, discount):
    return price - (price * discount / 100)

def test_integer_price_integer_discount():
    assert calculate_discount(100, 10) == 90

def test_integer_price_float_discount():
    assert calculate_discount(100, 33.3) == 66.7

def test_float_price_integer_dicsount():
    assert calculate_discount(50.5, 10) == 45.45

def test_float_price_float_discount():
    assert calculate_discount(50.5, 33.3) == 33.6835