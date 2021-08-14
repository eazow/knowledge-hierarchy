from tokens import (
    PLUS,
    EOF,
    BEGIN,
    ID,
    ASSIGN,
    SEMI,
    END,
    DOT,
    Token,
    INTEGER_CONST,
    COMMA,
    COLON,
    VAR,
    INTEGER,
    FLOAT_DIV,
    INTEGER_DIV, REAL, PROGRAM,
)
from lexer import Lexer


def test_tokens():
    lexer = Lexer("3+5")

    assert lexer.get_next_token() == Token(INTEGER_CONST, 3)
    assert lexer.get_next_token() == Token(PLUS, "+")
    assert lexer.get_next_token() == Token(INTEGER_CONST, 5)
    assert lexer.get_next_token() == Token(EOF, None)


def test_tokens_with_whitespaces():
    lexer = Lexer("3 + 5")

    assert lexer.get_next_token() == Token(INTEGER_CONST, 3)
    assert lexer.get_next_token() == Token(PLUS, "+")
    assert lexer.get_next_token() == Token(INTEGER_CONST, 5)
    assert lexer.get_next_token() == Token(EOF, None)


def test_statement():
    lexer = Lexer("BEGIN a := 2; END.")

    assert lexer.get_next_token() == Token(BEGIN, "BEGIN")
    assert lexer.get_next_token() == Token(ID, "a")
    assert lexer.get_next_token() == Token(ASSIGN, ":=")
    assert lexer.get_next_token() == Token(INTEGER_CONST, 2)
    assert lexer.get_next_token() == Token(SEMI, ";")
    assert lexer.get_next_token() == Token(END, "END")
    assert lexer.get_next_token() == Token(DOT, ".")
    assert lexer.get_next_token() == Token(EOF, None)


def test_symbol_tokens():
    assert Lexer(",").get_next_token() == Token(COMMA, ",")
    assert Lexer(";").get_next_token() == Token(SEMI, ";")
    assert Lexer(".").get_next_token() == Token(DOT, ".")
    assert Lexer(":").get_next_token() == Token(COLON, ":")
    assert Lexer("+").get_next_token() == Token(PLUS, "+")
    assert Lexer("/").get_next_token() == Token(FLOAT_DIV, "/")


def test_keyword_tokens():
    assert Lexer("VAR").get_next_token() == Token(VAR, "VAR")
    assert Lexer("INTEGER").get_next_token() == Token(INTEGER, "INTEGER")
    assert Lexer("DIV").get_next_token() == Token(INTEGER_DIV, "DIV")
    assert Lexer("REAL").get_next_token() == Token(REAL, "REAL")
    assert Lexer("PROGRAM").get_next_token() == Token(PROGRAM, "PROGRAM")
    assert Lexer("BEGIN").get_next_token() == Token(BEGIN, "BEGIN")
    assert Lexer("END").get_next_token() == Token(END, "END")
