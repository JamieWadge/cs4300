from src import task3

#Tests if number is positive
def test_positive():
    assert task3.number_sign(10) == "positive"

#Tests if number is negative
def test_negative():
    assert task3.number_sign(-10) == "negative"

#Tests if number is zero
def test_zero():
    assert task3.number_sign(0) == "zero"

#Tests if first ten prime numbers are correct
def test_prime():
    assert task3.ten_prime() == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

#Tests if the sum of 1 to 100 is correct
def test_100():
    assert task3.sum_100() == 5050