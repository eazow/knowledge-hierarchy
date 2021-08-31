import pytest
from errors import ParserError

from interpreter import Interpreter
from lexer import Lexer
from parser import Parser


template = """
program TestArithmeticExpressions;
var result: integer;
begin
    result := {};
end.
"""


def _get_result(arithmetic_expression):
    interpreter = Interpreter(Parser(Lexer(template.format(arithmetic_expression))))
    interpreter.interpret()

    ar = interpreter.call_stack.peek()
    return ar.get("result")


def test_plus():
    assert _get_result("3+5") == 8
    assert _get_result("3 + 5") == 8


def test_minus():
    assert _get_result("5-2") == 3
    assert _get_result("5 - 2") == 3


def test_multi_digits_plus():
    assert _get_result("126+200") == 326
    assert _get_result("126 + 200") == 326


def test_invalid_syntax():
    with pytest.raises(ParserError) as exec_info:
        _get_result("126+")

    assert (
        exec_info.value.message
        == "ParserError: Invalid syntax -> Token(TokenType.SEMI, ;, position=4:19)"
    )


def test_plus_and_minus():
    assert _get_result("7 - 3 + 2 - 1") == 5
    assert _get_result("12 - 10 + 11 + 15") == 28


def test_multiply_and_divide():
    assert _get_result("2*6/2") == 6
    assert _get_result("2 * 6 / 2") == 6


def test_hybrid_expressions():
    assert _get_result("7 - 3 * 2 - 1") == 0
    assert _get_result("16 + 2 * 3 - 6 / 2") == 19


def test_hybrid_expressions_with_parentheses():
    assert _get_result("7 + 3 * (10 / (12 / (3 + 1) - 1))") == 22
    assert (
        _get_result("7 + 3 * (10 / (12 / (3 + 1) - 1)) / (2 + 3) - 5 - 3 + (8)") == 10
    )
    assert _get_result("7 + (((3 + 2)))") == 12


def test_unary_operators():
    assert _get_result("--6") == 6
    assert _get_result("5--3") == 8
