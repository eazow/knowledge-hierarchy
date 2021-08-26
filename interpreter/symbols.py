from collections import OrderedDict

from tokens import INTEGER, REAL


class Symbol:
    def __init__(self, name, type=None):
        self.name = name
        self.type = type


class BuiltInSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<{class_name}(name='{name}')>".format(
            class_name=self.__class__.__name__, name=self.name
        )


class VarSymbol(Symbol):
    def __init__(self, name, type):
        super().__init__(name, type)

    def __str__(self):
        return "<{class_name}(name='{name}', type='{type}')>".format(
            class_name=self.__class__.__name__, name=self.name, type=self.type
        )

    __repr__ = __str__


class ProcedureSymbol(Symbol):
    def __init__(self, name, params=None):
        super(ProcedureSymbol, self).__init__(name)

        self.params = params if params else []

    def __str__(self):
        return "<{class_name}(name={name}, parameters={params})>".format(
            class_name=self.__class__.__name__, name=self.name, params=self.params
        )

    __repr__ = __str__


class ScopedSymbolTable:
    def __init__(self, scope_name=None, scope_level=0, enclosing_scope=None):
        self._symbols = OrderedDict()
        self.scope_name = scope_name
        self.scope_level = scope_level
        self.enclosing_scope = enclosing_scope
        self._init_builtins()

    def _init_builtins(self):
        self.define(BuiltInSymbol(INTEGER))
        self.define(BuiltInSymbol(REAL))

    def __str__(self):
        return "Symbols: {}".format(self._symbols.values())

    __repr__ = __str__

    def define(self, symbol):
        print("Define: {}".format(symbol))
        self._symbols[symbol.name] = symbol

    def lookup(self, name, current_scope_only=False):
        print("Lookup: {name}. (Scope name: {scope_name})".format(name=name, scope_name=self.scope_name))
        symbol = self._symbols.get(name)

        if symbol:
            return symbol

        if current_scope_only:
            return None

        # recursively go up the chain and lookup the name
        if self.enclosing_scope:
            return self.enclosing_scope.lookup(name)
