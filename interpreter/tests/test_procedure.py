from interpreter import Interpreter
from lexer import Lexer
from parser import Parser


def test_procedure():
    text = """
PROGRAM TestProcedure;
VAR
   a : INTEGER;

PROCEDURE P1;
VAR
   a : REAL;
   k : INTEGER;

   PROCEDURE P2;
   VAR
      a, z : INTEGER;
   BEGIN {P2}
      z := 777;
   END;  {P2}

BEGIN {P1}

END;  {P1}

BEGIN {TestProcedure}
   a := 10;
END.  {TestProcedure}
"""
    interpreter = Interpreter(Parser(Lexer(text)))
    interpreter.interpret()

    results = interpreter.semantic_analyzer.GLOBAL_SCOPE
    assert 10 == results.get("a")


def test_procedure_with_parameters():
    text = """
program Main;
   var x, y: real;

   procedure Alpha(a : integer);
      var y : integer;
   begin
      x := a + x + y;
   end;

begin { Main }

end.  { Main }
"""
    interpreter = Interpreter(Parser(Lexer(text)))
    interpreter.interpret()
