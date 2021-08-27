from tokens import Token, TokenType

RESERVED_KEYWORDS = {
    "PROGRAM": TokenType.PROGRAM,
    "VAR": TokenType.VAR,
    "DIV": TokenType.INTEGER_DIV,
    "INTEGER": TokenType.INTEGER,
    "REAL": TokenType.REAL,
    "BEGIN": TokenType.BEGIN,
    "END": TokenType.END,
    "PROCEDURE": TokenType.PROCEDURE
}
