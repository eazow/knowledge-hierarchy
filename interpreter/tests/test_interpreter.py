from interpreter import Interpreter, Token, EOF, INTEGER, PLUS


def test_interpreter():
    interpreter = Interpreter("3+5")

    assert interpreter.get_next_token() == Token(INTEGER, 3)
    assert interpreter.get_next_token() == Token(PLUS, "+")
    assert interpreter.get_next_token() == Token(INTEGER, 5)
    assert interpreter.get_next_token() == Token(EOF, None)
