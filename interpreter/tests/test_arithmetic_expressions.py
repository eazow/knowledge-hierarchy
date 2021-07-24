import pytest
from interpreter import Parser, Token, EOF, INTEGER, PLUS, Lexer, Interpreter


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
    assert Interpreter(Parser(Lexer("3+5"))).interpret() == 8
    assert Interpreter(Parser(Lexer("3 + 5"))).interpret() == 8


def test_minus():
    assert Interpreter(Parser(Lexer("5-2"))).interpret() == 3
    assert Interpreter(Parser(Lexer("5 - 2"))).interpret() == 3


def test_multi_digits_plus():
    assert Interpreter(Parser(Lexer("126+200"))).interpret() == 326
    assert Interpreter(Parser(Lexer("126 + 200"))).interpret() == 326


def test_invalid_syntax():
    with pytest.raises(Exception) as exec_info:
        Interpreter(Parser(Lexer("126+"))).interpret()

    assert str(exec_info.value) == "Invalid syntax"


def test_plus_and_minus():
    assert Interpreter(Parser(Lexer("7 - 3 + 2 - 1"))).interpret() == 5
    assert Interpreter(Parser(Lexer("12 - 10 + 11 + 15"))).interpret() == 28


def test_multiply_and_divide():
    assert Interpreter(Parser(Lexer("2*6/2"))).interpret() == 6
    assert Interpreter(Parser(Lexer("2 * 6 / 2"))).interpret() == 6


def test_hybrid_expressions():
    assert Interpreter(Parser(Lexer("7 - 3 * 2 - 1"))).interpret() == 0
    assert Interpreter(Parser(Lexer("16 + 2 * 3 - 6 / 2"))).interpret() == 19


def test_hybrid_expressions_with_parentheses():
    assert (
        Interpreter(Parser(Lexer("7 + 3 * (10 / (12 / (3 + 1) - 1))"))).interpret()
        == 22
    )
    assert (
        Interpreter(
            Parser(Lexer("7 + 3 * (10 / (12 / (3 + 1) - 1)) / (2 + 3) - 5 - 3 + (8)"))
        ).interpret()
        == 10
    )
    assert Interpreter(Parser(Lexer("7 + (((3 + 2)))"))).interpret() == 12


def test_unary_operators():
    assert Interpreter(Parser(Lexer("--6"))).interpret() == 6
    assert Interpreter(Parser(Lexer("5--3"))).interpret() == 8


