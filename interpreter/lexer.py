from keywords import RESERVED_KEYWORDS
from tokens import (
    ID,
    ASSIGN,
    SEMI,
    DOT,
    INTEGER,
    PLUS,
    MINUS,
    MUL,
    DIV,
    LPAREN,
    RPAREN,
    EOF,
    Token,
    REAL_CONST,
    INTEGER_CONST, COLON,
)


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception("Invalid character")

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def advance(self):
        """Advance the 'pos' pointer and set the 'current_char' variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def number(self):
        """Return a (multidigit) integer or float consumed from the input."""
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        if self.current_char == ".":
            result += self.current_char
            self.advance()

            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()
            token = Token(REAL_CONST, float(result))
        else:
            token = Token(INTEGER_CONST, int(result))

        return token

    def _id(self):
        """Handle identifiers and reserved keywords"""
        result = ""
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()

        return RESERVED_KEYWORDS.get(result, Token(ID, result))

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isalpha():
                return self._id()

            if self.current_char == "{":
                self.advance()
                self.skip_comment()
                continue

            if self.current_char == ":" and self.peek() == "=":
                self.advance()
                self.advance()
                return Token(ASSIGN, ":=")

            if self.current_char == ";":
                self.advance()
                return Token(SEMI, ";")

            if self.current_char == ".":
                self.advance()
                return Token(DOT, ".")

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return self.number()

            if self.current_char == "+":
                self.advance()
                return Token(PLUS, "+")

            if self.current_char == "-":
                self.advance()
                return Token(MINUS, "-")

            if self.current_char == "*":
                self.advance()
                return Token(MUL, "*")

            if self.current_char == "/":
                self.advance()
                return Token(DIV, "/")

            if self.current_char == "(":
                self.advance()
                return Token(LPAREN, "(")

            if self.current_char == ")":
                self.advance()
                return Token(RPAREN, ")")

            if self.current_char == ":":
                self.advance()
                return Token(COLON, ":")

            self.error()

        return Token(EOF, None)

    def skip_comment(self):
        while self.current_char is not None and self.current_char != "}":
            self.advance()

        self.advance()
