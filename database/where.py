from utils import slots


class _Where:
    """_Where(mode, condition) -> _Where"""

    __slots__ = slots("call rows")

    def __init__(self, mode, condition):
        """Initializes _Where support object for simple selections."""
        self.__call = {"and": all, "or": any}[mode]
        self.__rows = condition

    def __call__(self, row):
        """Runs test on given row and validates against condition."""
        return self.__call(row[k] == v for k, v in self.__rows.items())
