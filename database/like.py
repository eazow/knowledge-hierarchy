import re

from utils import slots


class NotLike:
    """NotLike(column, pattern, flags=IGNORECASE, advanced=False) -> NotLike"""

    __slots__ = slots("column method")

    def __init__(self, column, pattern, flags=re.IGNORECASE, advanced=False):
        "Initializes comparison object for specified column."
        self.__column = column
        if not advanced:
            pattern = "^" + pattern + "$"
        self.__method = re.compile(pattern, flags).search

    def __call__(self, row):
        "Tests if column in row was like the given pattern."
        return self.__method(row[self.__column]) is None


class Like(NotLike):
    "Like(column, pattern, flags=IGNORECASE, advanced=False) -> Like"

    __slots__ = slots()

    def __call__(self, row):
        """Reverses the result from calling a NotLike instance."""
        return not super().__call__(row)
