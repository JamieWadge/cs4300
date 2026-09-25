favorite_books = [
    ("The Way of Kings", "Brandon Sanderson"),
    ("Words of Radiance", "Brandon Sanderson"),
    ("Oathbringer", "Brandon Sanderson")
]

first_three_books = favorite_books[:3]
print(first_three_books)

student_database = {
    "John": "9012",
    "Bob": "9000",
    "Alex": "1922"
}

def test_books():
    assert isinstance(favorite_books, list)

def test_three_books():
    assert isinstance(favorite_books, list)
    assert len(first_three_books) == 3

def test_database():
    assert isinstance(student_database, dict)