from parser import Parser
from symbols import NodeVisitor, SymbolTableBuilder
from lexer import Lexer


class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser

        self.symbol_table_builder = SymbolTableBuilder()

    def interpret(self):
        tree = self.parser.parse()
        return self.symbol_table_builder.visit(tree)

    def expr(self):  # deprecated
        tree = self.parser.expr()
        return self.symbol_table_builder.visit(tree)


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
