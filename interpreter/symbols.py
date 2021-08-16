from tokens import PLUS, MINUS, MUL, INTEGER_DIV, FLOAT_DIV, INTEGER, REAL


class Symbol:
    def __init__(self, name, type=None):
        self.name = name
        self.type = type


class BuiltInSymbol(Symbol):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    __repr__ = __str__


class VarSymbol(Symbol):
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __str__(self):
        return "<{name}:{type}>".format(name=self.name, type=self.type)

    __repr__ = __str__


class SymbolTable:
    def __init__(self):
        self._symbols = {}

    def __str__(self):
        return "Symbols: {}".format(self._symbols.values())

    __repr__ = __str__

    def define(self, symbol):
        print("Define: {}".format(symbol))
        self._symbols[symbol.name] = symbol

    def lookup(self, name):
        print("Lookup: {}".format(name))
        return self._symbols.get(name)


class NodeVisitor:
    def visit(self, node):
        method_name = "visit_{}".format(type(node).__name__)
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception("No visit_{} method".format(type(node).__name__))


class SymbolTableBuilder(NodeVisitor):
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.GLOBAL_SCOPE = {}
        self._init_builtins()

    def _init_builtins(self):
        self.symbol_table.define(BuiltInSymbol(INTEGER))
        self.symbol_table.define(BuiltInSymbol(REAL))

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

    def visit_VarDecl(self, node):
        type_name = node.type_node.value
        type_symbol = self.symbol_table.lookup(type_name)
        var_name = node.var_node.value
        self.symbol_table.define(VarSymbol(var_name, type_symbol))

    def visit_Type(self, node):
        pass