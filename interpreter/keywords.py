from tokens import Token, BEGIN, END, VAR, DIV, INTEGER, REAL

RESERVED_KEYWORDS = {
    "PROGRAM": Token(PROGRAM, "PROGRAM"),
    "VAR": Token(VAR, "VAR"),
    "DIV": Token(DIV, "DIV"),
    "INTEGER": Token(INTEGER, "INTEGER"),
    "REAL": Token(REAL, "REAL"),
    "BEGIN": Token(BEGIN, "BEGIN"),
    "END": Token(END, "END"),
}
