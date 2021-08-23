from parser import Parser
from symbols import NodeVisitor, SemanticAnalyzer
from lexer import Lexer


class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser

        self.semantic_analyzer = SemanticAnalyzer()

    def interpret(self):
        tree = self.parser.parse()
        return self.semantic_analyzer.visit(tree)

    def expr(self):  # deprecated
        tree = self.parser.expr()
        return self.semantic_analyzer.visit(tree)


def main():
    while True:
        try:
            text = input("calc> ")
        except EOFError:
            break
        if not text:
            continue

        interpreter = Interpreter(Parser(Lexer(text)))
        result = interpreter.interpret()
        print(result)


if __name__ == "__main__":
    main()
