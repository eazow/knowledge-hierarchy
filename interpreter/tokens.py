from enum import Enum


class TokenType(Enum):
    PLUS = "+"
    MINUS = "-"
    MUL = "*"
    FLOAT_DIV = "/"
    LPAREN = "("
    RPAREN = ")"
    SEMI = ";"
    DOT = "."
    COLON = ":"
    COMMA = ","
    EOF = "EOF"
    # reserved words
    PROGRAM = "PROGRAM"
    PROCEDURE = "PROCEDURE"
    VAR = "VAR"
    INTEGER = "INTEGER"
    REAL = "REAL"
    BEGIN = "BEGIN"
    END = "END"
    INTEGER_DIV = "DIV"
    # misc
    ID = "ID"
    ASSIGN = ":="
    REAL_CONST = "REAL_CONST"
    INTEGER_CONST = "INTEGER_CONST"


class Token(object):
    def __init__(self, type, value, lineno=None, column=None):
        self.type = type
        self.value = value
        self.lineno = lineno
        self.column = column

    def __str__(self):
        """String representation of the class instance.

        Example:
            >>> Token(TokenType.INTEGER, 7, lineno=5, column=10)
            Token(TokenType.INTEGER, 7, position=5:10)
        """
        return f"Token({self.type}, {self.value}, position={self.lineno}:{self.column})"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.type == other.type and self.value == other.value
