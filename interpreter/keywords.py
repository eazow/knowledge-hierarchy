from tokens import Token, TokenType

RESERVED_KEYWORDS = {
    "PROGRAM": Token(TokenType.PROGRAM, "PROGRAM"),
    "VAR": Token(TokenType.VAR, "VAR"),
    "DIV": Token(TokenType.INTEGER_DIV, "DIV"),
    "INTEGER": Token(TokenType.INTEGER, "INTEGER"),
    "REAL": Token(TokenType.REAL, "REAL"),
    "BEGIN": Token(TokenType.BEGIN, "BEGIN"),
    "END": Token(TokenType.END, "END"),
    "PROCEDURE": Token(TokenType.PROCEDURE, "PROCEDURE")
}
