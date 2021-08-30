from errors import SemanticError, ErrorCode
from inflection import underscore
from stack import CallStack

from symbols import ScopedSymbolTable, VarSymbol, ProcedureSymbol
from tokens import TokenType


class NodeVisitor:
    def visit(self, node):
        method_name = "visit_{}".format(underscore(type(node).__name__))
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception("No visit_{} method".format(type(node).__name__))


class SemanticAnalyzer(NodeVisitor):
    def __init__(self):
        self.current_scoped_symbol_table = None

    def visit_bin_op(self, node):
        if node.op.type == TokenType.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == TokenType.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == TokenType.MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == TokenType.INTEGER_DIV:
            return self.visit(node.left) // self.visit(node.right)
        elif node.op.type == TokenType.FLOAT_DIV:
            return self.visit(node.left) / float(self.visit(node.right))

    def visit_num(self, node):
        return node.value

    def visit_unary_op(self, node):
        op = node.token.type
        if op == TokenType.PLUS:
            return self.visit(node.node)
        elif op == TokenType.MINUS:
            return -self.visit(node.node)

    def visit_compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_no_op(self, node):
        pass

    def visit_assign(self, node):
        var_name = node.left.value
        self.GLOBAL_SCOPE[var_name] = self.visit(node.right)

    def visit_var(self, node):
        var_name = node.value
        var_symbol = self.current_scoped_symbol_table.lookup(var_name)
        if var_symbol is None:
            self.error(error_code=ErrorCode.ID_NOT_FOUND, token=node.token)

        return self.GLOBAL_SCOPE.get(var_name)

    def visit_program(self, node):
        print("Enter scope: global")
        global_scope = ScopedSymbolTable(scope_name="global", scope_level=1)
        self.current_scoped_symbol_table = global_scope

        self.visit(node.block)

        print("Leave scope: global")

    def visit_block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)

        self.visit(node.compound_statement)

    def visit_var_decl(self, node):
        type_name = node.type_node.value
        type_symbol = self.current_scoped_symbol_table.lookup(type_name)
        var_name = node.var_node.value

        if self.current_scoped_symbol_table.lookup(var_name, current_scope_only=True):
            self.error(ErrorCode.DUPLICATE_ID, token=node.var_node.token)

        self.current_scoped_symbol_table.define(VarSymbol(var_name, type_symbol))

    def visit_type(self, node):
        pass

    def visit_procedure_decl(self, node):
        proc_name = node.proc_name
        procedure_symbol = ProcedureSymbol(name=proc_name)
        self.current_scoped_symbol_table.define(procedure_symbol)

        print("Enter scope: {proc_name}".format(proc_name=proc_name))
        procedure_scoped_symbol_table = ScopedSymbolTable(
            scope_name=proc_name,
            scope_level=self.current_scoped_symbol_table.scope_level + 1,
            enclosing_scope=self.current_scoped_symbol_table
        )
        self.current_scoped_symbol_table = procedure_scoped_symbol_table

        for param in node.params:
            param_type_symbol = self.current_scoped_symbol_table.lookup(param.type_node.value)
            param_name = param.var_node.value
            var_symbol = VarSymbol(param_name, param_type_symbol)
            self.current_scoped_symbol_table.define(var_symbol)

        self.visit(node.block_node)

        self.current_scoped_symbol_table = procedure_scoped_symbol_table.enclosing_scope
        print("Leave scope: {proc_name}".format(proc_name=proc_name))

    def visit_procedure_call(self, node):
        for param in node.actual_params:
            self.visit(param)

    def error(self, error_code, token):
        raise SemanticError(error_code=error_code, token=token, message=f"{error_code.value} -> {token}")
