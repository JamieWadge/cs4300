from src import task5

def test_books():
    assert isinstance(task5.favorite_books, list)

def test_three_books():
    assert isinstance(task5.favorite_books, list)
    assert len(task5.first_three_books) == 3

def test_database():
    assert isinstance(task5.student_database, dict)