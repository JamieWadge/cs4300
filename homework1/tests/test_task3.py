from src import task3

def test_positive():
    assert task3.number_sign(10) == "positive"

def test_negative():
    assert task3.number_sign(-10) == "negative"

def test_zero():
    assert task3.number_sign(0) == "zero"

def test_prime():
    assert task3.ten_prime() == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]


def test_100():
    assert task3.sum_100() == 5050