from src import task2

def test_int():
    assert isinstance(task2.num1, int)

def test_float():
    assert isinstance(task2.num2, float)

def test_string():
    assert isinstance(task2.string, str)

def test_boolean():
    assert isinstance(task2.boolean, bool)