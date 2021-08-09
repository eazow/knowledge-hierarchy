from interpreter import Interpreter
from lexer import Lexer
from parser import Parser


def test_compound_statement():
    text = """
BEGIN
     BEGIN
         number := 2;
         a := number;
         b := 10 * a + 10 * number / 4;
         c := a - - b
     END;
     x := 11;
END.
"""
    interpreter = Interpreter(Parser(Lexer(text)))
    interpreter.interpret()

    assert interpreter.GLOBAL_SCOPE == {"a": 2, "x": 11, "c": 27, "b": 25, "number": 2}
