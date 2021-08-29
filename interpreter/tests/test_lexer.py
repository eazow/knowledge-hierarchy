import pytest

from errors import LexerError
from lexer import Lexer
from tokens import Token, TokenType


def test_tokens():
    lexer = Lexer("3+5")

    assert lexer.get_next_token() == Token(TokenType.INTEGER_CONST, 3)
    assert lexer.get_next_token() == Token(TokenType.PLUS, "+")
    assert lexer.get_next_token() == Token(TokenType.INTEGER_CONST, 5)
    assert lexer.get_next_token() == Token(TokenType.EOF, TokenType.EOF.value)


def test_tokens_with_whitespaces():
    lexer = Lexer("3 + 5")

    assert lexer.get_next_token() == Token(TokenType.INTEGER_CONST, 3)
    assert lexer.get_next_token() == Token(TokenType.PLUS, "+")
    assert lexer.get_next_token() == Token(TokenType.INTEGER_CONST, 5)
    assert lexer.get_next_token() == Token(TokenType.EOF, TokenType.EOF.value)


def test_statement():
    lexer = Lexer("BEGIN a := 2; END.")

    assert lexer.get_next_token() == Token(TokenType.BEGIN, TokenType.BEGIN.value)
    assert lexer.get_next_token() == Token(TokenType.ID, "a")
    assert lexer.get_next_token() == Token(TokenType.ASSIGN, TokenType.ASSIGN.value)
    assert lexer.get_next_token() == Token(TokenType.INTEGER_CONST, 2)
    assert lexer.get_next_token() == Token(TokenType.SEMI, TokenType.SEMI.value)
    assert lexer.get_next_token() == Token(TokenType.END, TokenType.END.value)
    assert lexer.get_next_token() == Token(TokenType.DOT, TokenType.DOT.value)
    assert lexer.get_next_token() == Token(TokenType.EOF, TokenType.EOF.value)


def test_symbol_tokens():
    assert Lexer(",").get_next_token() == Token(TokenType.COMMA, ",")
    assert Lexer(";").get_next_token() == Token(TokenType.SEMI, ";")
    assert Lexer(".").get_next_token() == Token(TokenType.DOT, ".")
    assert Lexer(":").get_next_token() == Token(TokenType.COLON, ":")
    assert Lexer("+").get_next_token() == Token(TokenType.PLUS, "+")
    assert Lexer("/").get_next_token() == Token(TokenType.FLOAT_DIV, "/")


def test_keyword_tokens():
    assert Lexer("VAR").get_next_token() == Token(TokenType.VAR, "VAR")
    assert Lexer("INTEGER").get_next_token() == Token(TokenType.INTEGER, "INTEGER")
    assert Lexer("DIV").get_next_token() == Token(TokenType.INTEGER_DIV, "DIV")
    assert Lexer("REAL").get_next_token() == Token(TokenType.REAL, "REAL")
    assert Lexer("PROGRAM").get_next_token() == Token(TokenType.PROGRAM, "PROGRAM")
    assert Lexer("BEGIN").get_next_token() == Token(TokenType.BEGIN, "BEGIN")
    assert Lexer("END").get_next_token() == Token(TokenType.END, "END")
    assert Lexer("PROCEDURE").get_next_token() == Token(TokenType.PROCEDURE, "PROCEDURE")


def test_lexer_error():
    with pytest.raises(LexerError) as exec_info:
        Lexer("^").get_next_token()

    # assert exec_info.value.args[0] == "Lexer error on '^' line: 1 column: 1"
    # print(exec_info.value.args[0])
