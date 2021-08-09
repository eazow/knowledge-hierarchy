from tokens import INTEGER, PLUS, EOF, BEGIN, ID, ASSIGN, SEMI, END, DOT, Token
from lexer import Lexer


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


def test_statement():
    lexer = Lexer("BEGIN a := 2; END.")

    assert lexer.get_next_token() == Token(BEGIN, "BEGIN")
    assert lexer.get_next_token() == Token(ID, "a")
    assert lexer.get_next_token() == Token(ASSIGN, ":=")
    assert lexer.get_next_token() == Token(INTEGER, 2)
    assert lexer.get_next_token() == Token(SEMI, ";")
    assert lexer.get_next_token() == Token(END, "END")
    assert lexer.get_next_token() == Token(DOT, ".")
    assert lexer.get_next_token() == Token(EOF, None)
