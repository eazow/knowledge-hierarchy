# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF, BEGIN, END, ID, ASSIGN, SEMI, DOT, PROGRAM, VAR, REAL = (
    "INTEGER",
    "PLUS",
    "MINUS",
    "MUL",
    "DIV",
    "(",
    ")",
    "EOF",
    "BEGIN",
    "END",
    "ID",
    "ASSIGN",
    "SEMI",
    "DOT",
    "PROGRAM",
    "VAR",
    "REAL"
)


class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS, '+')
            Token(MUL, '*')
        """
        return "Token({type}, {value})".format(type=self.type, value=repr(self.value))

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.type == other.type and self.value == other.value