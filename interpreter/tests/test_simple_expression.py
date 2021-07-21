from interpreter import Interpreter, Token, EOF, INTEGER, PLUS


def test_tokens():
    interpreter = Interpreter("3+5")

    assert interpreter.get_next_token() == Token(INTEGER, 3)
    assert interpreter.get_next_token() == Token(PLUS, "+")
    assert interpreter.get_next_token() == Token(INTEGER, 5)
    assert interpreter.get_next_token() == Token(EOF, None)


def test_tokens_with_whitespaces():
    interpreter = Interpreter("3 + 5")

    assert interpreter.get_next_token() == Token(INTEGER, 3)
    assert interpreter.get_next_token() == Token(PLUS, "+")
    assert interpreter.get_next_token() == Token(INTEGER, 5)
    assert interpreter.get_next_token() == Token(EOF, None)


def test_plus():
    assert Interpreter("3+5").expr() == 8
    assert Interpreter("3 + 5").expr() == 8


def test_minus():
    assert Interpreter("5-2").expr() == 3
    assert Interpreter("5 - 2").expr() == 3
