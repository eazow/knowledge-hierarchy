from parser import Parser
from tokens import PLUS, MINUS, MUL, DIV, INTEGER_DIV, FLOAT_DIV
from lexer import Lexer


class NodeVisitor:
    def visit(self, node):
        method_name = "visit_{}".format(type(node).__name__)
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception("No visit_{} method".format(type(node).__name__))


class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.GLOBAL_SCOPE = {}

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)

    def visit_BinOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == INTEGER_DIV:
            return self.visit(node.left) // self.visit(node.right)
        elif node.op.type == FLOAT_DIV:
            return self.visit(node.left) / float(self.visit(node.right))

    def visit_Num(self, node):
        return node.value

    def visit_UnaryOp(self, node):
        op = node.token.type
        if op == PLUS:
            return self.visit(node.node)
        elif op == MINUS:
            return -self.visit(node.node)

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_NoOp(self, node):
        pass

    def visit_Assign(self, node):
        var_name = node.left.value
        self.GLOBAL_SCOPE[var_name] = self.visit(node.right)

    def visit_Var(self, node):
        var_name = node.value
        val = self.GLOBAL_SCOPE.get(var_name)
        if val is None:
            raise NameError(repr(var_name))
        return val

    def visit_Program(self, node):
        self.visit(node.block)

    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)

        self.visit(node.compound_statement)

    def visit_ValDecl(self, node):
        pass

    def visit_Type(self, node):
        pass


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
