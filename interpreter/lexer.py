from errors import LexerError
from keywords import RESERVED_KEYWORDS
from tokens import Token, TokenType


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

        self.lineno = 1
        self.column = 1

    def error(self):
        message = f"Lexer error on '{self.current_char}' line: {self.lineno} column: {self.column}"

        raise LexerError(message=message)

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def advance(self):
        """Advance the 'pos' pointer and set the 'current_char' variable."""
        if self.current_char == "\n":
            self.lineno += 1
            self.column = 0

        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]
            self.column += 1

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
            token = Token(TokenType.REAL_CONST, float(result))
        else:
            token = Token(TokenType.INTEGER_CONST, int(result))

        return token

    def _id(self):
        """Handle identifiers and reserved keywords"""
        result = ""
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()

        return RESERVED_KEYWORDS.get(result.upper(), Token(ID, result))

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isalpha():
                return self._id()

            if self.current_char == ":" and self.peek() == "=":
                self.advance()
                self.advance()
                return Token(ASSIGN, ":=")

            if self.current_char == "{":
                self.advance()
                self.skip_comment()
                continue

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return self.number()

            try:
                token_type = TokenType(self.current_char)
            except ValueError:
                self.error()
            else:
                token = Token(type=token_type, value=token_type.value, lineno=self.lineno, column=self.column)
                self.advance()
                return token

        return Token(type=TokenType.EOF, value=TokenType.EOF.value, lineno=self.lineno, column=self.column)

    def skip_comment(self):
        while self.current_char is not None and self.current_char != "}":
            self.advance()

        self.advance()
