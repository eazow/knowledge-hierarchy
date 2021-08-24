import pytest
from interpreter import Interpreter
from lexer import Lexer
from parser import Parser


@pytest.mark.skip()
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


def test_program():
    text = """
PROGRAM Test;
VAR
   number     : INTEGER;
   a, b, c, x : INTEGER;
   y          : REAL;

BEGIN {Test}
   BEGIN
      number := 2;
      a := number;
      b := 10 * a + 10 * number DIV 4;
      c := a - - b
   END;
   x := 11;
   y := 20 / 7 + 3.14;
   { writeln('a = ', a); }
   { writeln('b = ', b); }
   { writeln('c = ', c); }
   { writeln('number = ', number); }
   { writeln('x = ', x); }
   { writeln('y = ', y); }
END.  {Part10}
"""

    interpreter = Interpreter(Parser(Lexer(text)))
    interpreter.interpret()

    results = interpreter.semantic_analyzer.GLOBAL_SCOPE
    assert 2 == results.get("a")
    assert 11 == results.get("x")
    assert 27 == results.get("c")
    assert 25 == results.get("b")
    assert 2 == results.get("number")
    assert 5.997 == round(results.get("y"), 3)


def test_empty_program():
    text = """
PROGRAM Empty;

BEGIN {Empty}
   BEGIN
   END;
END.  {Empty}
"""
    interpreter = Interpreter(Parser(Lexer(text)))
    interpreter.interpret()

    results = interpreter.semantic_analyzer.GLOBAL_SCOPE
    assert results == {}


def test_undeclared_variable():
    text = """
PROGRAM NameError;
VAR
   a : INTEGER;

BEGIN
   a := 2 + b;
END.
"""
    with pytest.raises(Exception) as exec_info:
        Interpreter(Parser(Lexer(text))).interpret()

    assert exec_info.typename == "NameError"
    assert exec_info.value.args[0] == "Error: Symbol(identifier) not found 'b'"


def test_duplicate_identifier():
    text = """
PROGRAM DuplicateIdentifier;
VAR
    x, y: INTEGER;
    y: REAL;

BEGIN
x := x + y;
END.
"""
    with pytest.raises(Exception) as exec_info:
        Interpreter(Parser(Lexer(text))).interpret()

    assert exec_info.typename == "NameError"
    assert exec_info.value.args[0] == "Error: Duplicate identifier 'y' found"


def test_case_insensitive():
    text = """
program CaseInsensitive;
var
   a : INTEGER;

begin
   a := 2 * 6 - 2;
end.
"""
    interpreter = Interpreter(Parser(Lexer(text)))
    interpreter.interpret()

    results = interpreter.semantic_analyzer.GLOBAL_SCOPE
    assert 10 == results.get("a")
