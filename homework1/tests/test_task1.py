from src import task1

#Tests stdout of task1
def test(capsys):
    task1.hello_world()
    captured = capsys.readouterr()
    assert captured.out == "Hello, World!\n"