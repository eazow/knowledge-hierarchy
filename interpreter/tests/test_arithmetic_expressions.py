import pytest
from errors import ParserError

from interpreter import Interpreter
from lexer import Lexer
from parser import Parser


template = """
program TestArithmeticExpressions;
var result: integer;
begin
    result = {};
end.
"""


def test_plus():
    assert Interpreter(Parser(Lexer("3+5"))).expr() == 8
    assert Interpreter(Parser(Lexer("3 + 5"))).expr() == 8


def test_minus():
    assert Interpreter(Parser(Lexer("5-2"))).expr() == 3
    assert Interpreter(Parser(Lexer("5 - 2"))).expr() == 3


def test_multi_digits_plus():
    assert Interpreter(Parser(Lexer("126+200"))).expr() == 326
    assert Interpreter(Parser(Lexer("126 + 200"))).expr() == 326


def test_invalid_syntax():
    with pytest.raises(ParserError) as exec_info:
        Interpreter(Parser(Lexer("126+"))).expr()

    assert exec_info.value.message == "ParserError: Invalid syntax -> Token(TokenType.EOF, EOF, position=1:4)"


def test_plus_and_minus():
    assert Interpreter(Parser(Lexer("7 - 3 + 2 - 1"))).expr() == 5
    assert Interpreter(Parser(Lexer("12 - 10 + 11 + 15"))).expr() == 28


def test_multiply_and_divide():
    assert Interpreter(Parser(Lexer("2*6/2"))).expr() == 6
    assert Interpreter(Parser(Lexer("2 * 6 / 2"))).expr() == 6


def test_hybrid_expressions():
    assert Interpreter(Parser(Lexer("7 - 3 * 2 - 1"))).expr() == 0
    assert Interpreter(Parser(Lexer("16 + 2 * 3 - 6 / 2"))).expr() == 19


def test_hybrid_expressions_with_parentheses():
    assert (
        Interpreter(Parser(Lexer("7 + 3 * (10 / (12 / (3 + 1) - 1))"))).expr()
        == 22
    )
    assert (
        Interpreter(
            Parser(Lexer("7 + 3 * (10 / (12 / (3 + 1) - 1)) / (2 + 3) - 5 - 3 + (8)"))
        ).expr()
        == 10
    )
    assert Interpreter(Parser(Lexer("7 + (((3 + 2)))"))).expr() == 12


def test_unary_operators():
    assert Interpreter(Parser(Lexer("--6"))).expr() == 6
    assert Interpreter(Parser(Lexer("5--3"))).expr() == 8


