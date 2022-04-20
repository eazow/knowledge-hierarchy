import itertools
import operator

from utils import slots


def rows(iterable):
    """Skips the first row (column names) from a table-style iterator."""
    iterator = iter(iterable)
    next(iterator)
    return iterator


class _RowAdapter:
    """_RowAdapter(row, column_map=None) -> _RowAdapter"""

    __slots__ = slots("row map")

    def __init__(self, row, column_map=None):
        """Initializes _RowAdapter with data and mapping information."""
        self.__row = row
        self.__map = column_map

    def __getattr__(self, column):
        """Returns a column from the row this instance in adapting."""
        if self.__map is None:
            return self.__unmapped(column)
        if column in self.__map:
            return self.__row[self.__map[column]]
        new_map = {}
        column += "."
        for name in self.__map:
            if name.startswith(column):
                new_map[name[len(column) :]] = self.__map[name]
        assert new_map, "Name did not match any known column: " + repr(column)
        return type(self)(self.__row, new_map)

    __getitem__ = __getattr__

    def __unmapped(self, column):
        """Processes a row with column names already filled in."""
        if column in self.__row:
            return self.__row[column]
        row = {}
        column += "."
        for name in self.__row:
            if name.startswith(column):
                row[name[len(column) :]] = self.__row[name]
        assert row, "Name did not match any known column: " + repr(column)
        return type(self)(row)


class _Repr:
    def __repr__(self):
        return "{}({})".format(
            type(self).__name__,
            ", ".join(
                itertools.starmap("{!s}={!r}".format, sorted(vars(self).items()))
            ),
        )


class _Row(_Repr):
    def __getattr__(self, name):
        return _Column(name)

    def __getitem__(self, key):
        return lambda row: row[key]


class _Column(_Row):
    def __init__(self, name):
        self.__name = name

    def __call__(self, row):
        return row[self.__name]

    def __getattr__(self, name):
        if name == "NOT":
            return Comparison(self, lambda a, b: (not a, b)[0], None)
        return super().__getattr__(self.__name + "." + name)

    def __lt__(self, other):
        return Comparison(self, operator.lt, other)

    def __le__(self, other):
        return Comparison(self, operator.le, other)

    def __eq__(self, other):
        return Comparison(self, operator.eq, other)

    def __ne__(self, other):
        return Comparison(self, operator.ne, other)

    def __gt__(self, other):
        return Comparison(self, operator.gt, other)

    def __ge__(self, other):
        return Comparison(self, operator.ge, other)

    def in_(self, *items):
        return Comparison(self, lambda a, b: a in b, items)


class Comparison(_Repr):
    def __init__(self, column, op, other):
        self.__column, self.__op, self.__other = column, op, other

    def __call__(self, row):
        if isinstance(self.__other, _Column):
            return self.__op(self.__column(row), self.__other(row))
        return self.__op(self.__column(row), self.__other)

    def __lt__(self, other):
        return self & (self.__column < other)

    def __le__(self, other):
        return self & (self.__column <= other)

    def __eq__(self, other):
        return self & (self.__column == other)

    def __ne__(self, other):
        return self & (self.__column != other)

    def __gt__(self, other):
        return self & (self.__column > other)

    def __ge__(self, other):
        return self & (self.__column >= other)

    def __and__(self, other):
        return Comparison(self, lambda a, b: a and b, other)

    def __or__(self, other):
        return Comparison(self, lambda a, b: a or b, other)


ROW = _Row()
