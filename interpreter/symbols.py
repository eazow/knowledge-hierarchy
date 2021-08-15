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

    __repr__ = __str__()


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
