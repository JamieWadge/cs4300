from src import task2

#Tests if int
def test_int():
    assert isinstance(task2.num1, int)

#Tests if float
def test_float():
    assert isinstance(task2.num2, float)

#Tests if string
def test_string():
    assert isinstance(task2.string, str)

#Tests if boolean
def test_boolean():
    assert isinstance(task2.boolean, bool)