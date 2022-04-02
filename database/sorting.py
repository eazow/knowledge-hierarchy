from engine import ROW
from table import Table
from utils import _slots


class _SortedResults:
    "_SortedResults(iterable column, desc) -> _SortedResults"

    __slots__ = _slots("iter column direction")

    def __init__(self, iterable, column, desc):
        "Initializes sorting adapter with given data."
        self.__iter = iterable
        self.__column = column
        self.__direction = desc

    def __iter__(self):
        "Iterates over internal data in the order requested."
        title, *rows = tuple(self.__iter)
        index = title.index(self.__column)
        yield title
        for row in sorted(rows, key=ROW[index], reverse=self.__direction):
            yield row

    ########################################################################

    def order_by(self, column, desc=False):
        "Returns results that are sorted on an additional level."
        return type(self)(self, column, desc)

    def table(self):
        "Converts the sorted results into a table object."
        return Table.from_iter(self)