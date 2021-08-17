from tokens import Token, BEGIN, END, VAR, INTEGER, REAL, PROGRAM, INTEGER_DIV, PROCEDURE

RESERVED_KEYWORDS = {
    "PROGRAM": Token(PROGRAM, "PROGRAM"),
    "VAR": Token(VAR, "VAR"),
    "DIV": Token(INTEGER_DIV, "DIV"),
    "INTEGER": Token(INTEGER, "INTEGER"),
    "REAL": Token(REAL, "REAL"),
    "BEGIN": Token(BEGIN, "BEGIN"),
    "END": Token(END, "END"),
    "PROCEDURE": Token(PROCEDURE, "PROCEDURE")
}
