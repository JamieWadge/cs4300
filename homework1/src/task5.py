#Creates list of books and splice first 3. Creates database of students

favorite_books = [
    ("The Way of Kings", "Brandon Sanderson"),
    ("Words of Radiance", "Brandon Sanderson"),
    ("Oathbringer", "Brandon Sanderson"),
    ("Rythm of War", "Brandon Sanderson")
]

first_three_books = favorite_books[:3]
print(first_three_books)

student_database = {
    "John": "9012",
    "Bob": "9000",
    "Alex": "1922"
}

print(student_database)