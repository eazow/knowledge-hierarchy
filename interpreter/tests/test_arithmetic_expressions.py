import pytest
from interpreter import Interpreter, Token, EOF, INTEGER, PLUS, Lexer


def test_tokens():
    lexer = Lexer("3+5")

    assert lexer.get_next_token() == Token(INTEGER, 3)
    assert lexer.get_next_token() == Token(PLUS, "+")
    assert lexer.get_next_token() == Token(INTEGER, 5)
    assert lexer.get_next_token() == Token(EOF, None)


def test_tokens_with_whitespaces():
    lexer = Lexer("3 + 5")

    assert lexer.get_next_token() == Token(INTEGER, 3)
    assert lexer.get_next_token() == Token(PLUS, "+")
    assert lexer.get_next_token() == Token(INTEGER, 5)
    assert lexer.get_next_token() == Token(EOF, None)


def test_plus():
    assert Interpreter(Lexer("3+5")).expr() == 8
    assert Interpreter(Lexer("3 + 5")).expr() == 8


def test_minus():
    assert Interpreter(Lexer("5-2")).expr() == 3
    assert Interpreter(Lexer("5 - 2")).expr() == 3


def test_multi_digits_plus():
    assert Interpreter(Lexer("126+200")).expr() == 326
    assert Interpreter(Lexer("126 + 200")).expr() == 326


def test_invalid_syntax():
    with pytest.raises(Exception) as exec_info:
        Interpreter(Lexer("126+")).expr()

    assert str(exec_info.value) == "Invalid syntax"


def test_plus_and_minus():
    assert Interpreter(Lexer("7 - 3 + 2 - 1")).expr() == 5
    assert Interpreter(Lexer("12 - 10 + 11 + 15")).expr() == 28


def test_multiply_and_divide():
    assert Interpreter(Lexer("2*6/2")).expr() == 6
    assert Interpreter(Lexer("2 * 6 / 2")).expr() == 6


def test_hybrid_expressions():
    assert Interpreter(Lexer("7 - 3 * 2 - 1")).expr() == 0
    assert Interpreter(Lexer("16 + 2 * 3 - 6 / 2")).expr() == 19


def test_hybrid_expressions_with_parenthesis():
    assert Interpreter(Lexer("7 + 3 * (10 / (12 / (3 + 1) - 1))")) == 22
    assert (
        Interpreter(Lexer("7 + 3 * (10 / (12 / (3 + 1) - 1)) / (2 + 3) - 5 - 3 + (8)"))
        == 10
    )
    assert Interpreter(Lexer("7 + (((3 + 2)))")) == 12
