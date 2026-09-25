from src import task6

#Tests if expected word count is correct
def test_count():
    assert task6.word_count("task6_read_me.txt") == 104