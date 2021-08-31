from analyzer import NodeVisitor, SemanticAnalyzer
from stack import CallStack
from activation_record import ARType, ActivationRecord


class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.semantic_analyzer = SemanticAnalyzer()
        self.call_stack = CallStack()

    def interpret(self):
        tree = self.parser.parse()
        self.semantic_analyzer.visit(tree)

        self.visit(tree)

    def expr(self):  # deprecated
        tree = self.parser.expr()
        return self.semantic_analyzer.visit(tree)

    def visit_program(self, node):
        prog_name = node.name

        ar = ActivationRecord(name=prog_name, type=ARType.PROGRAM, nesting_level=1)
        self.call_stack.push(ar)

        self.visit(node.block)

        self.call_stack.pop()

    def visit_assign(self, node):
        var_name = node.left.name
        var_value = self.visit(node.right)
        ar = self.call_stack.peek()
        ar[var_name] = var_value

    def visit_var(self, node):
        var_name = node.name
        ar = self.call_stack.peek()
        return ar.get(var_name)

    def visit_procedure_call(self, node):
        proc_name = node.proc_name

        ar = ActivationRecord(name=proc_name, type=ARType.PROCEDURE, nesting_level=2)

        procedure_symbol = node.procedure_symbol

        formal_param_symbols = procedure_symbol.formal_params
        actual_params = node.actual_params

        for formal_param_symbol, actual_param in zip(formal_param_symbols, actual_params):
            ar[formal_param_symbol.name] = self.visit(actual_param)

        self.call_stack.push(ar)

        result = self.visit(procedure_symbol.block_node)

        self.call_stack.pop()

        return result
