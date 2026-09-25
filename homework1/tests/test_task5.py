from src import task5

#Tests if favorite_books is a list
def test_books():
    assert isinstance(task5.favorite_books, list)

#Tests if first_three_books is a list and has if spliced is only 3
def test_three_books():
    assert isinstance(task5.first_three_books, list)
    assert len(task5.first_three_books) == 3


def test_database():
    assert isinstance(task5.student_database, dict)