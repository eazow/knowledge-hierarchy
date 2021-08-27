import pytest
from errors import SemanticError
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

  procedure p1(a : integer);
    var y : integer;
    begin
    end;
  procedure p2(a, b : integer; c : real);
    var x : integer;
    begin
    end;
  procedure p3();
    var x : integer; 
    begin
    end;

begin { Main }

end.  { Main }
"""
    interpreter = Interpreter(Parser(Lexer(text)))
    interpreter.interpret()


def test_duplicate_identifier_in_procedure():
    text = """
program Main;
   var x, y: real;

   procedure Alpha(a : integer);
      var y : integer;
          a : real;  { ERROR here! }
   begin
   end;

begin { Main }

end.  { Main }
"""
    with pytest.raises(SemanticError) as exec_info:
        Interpreter(Parser(Lexer(text))).interpret()

    assert (
        exec_info.value.message
        == "SemanticError: Duplicate identifier found -> Token(TokenType.ID, a, position=6:11)"
    )
