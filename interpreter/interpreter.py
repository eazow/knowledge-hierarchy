from analyzer import NodeVisitor, SemanticAnalyzer


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
