import datetime


def _slots(names=""):
    """Returns the private version of names for __slots__ on a class."""
    return tuple("__" + name for name in names.split())


class _NamedInstance:
    "_NamedInstance(*args, **kwargs) -> _NamedInstance"

    __slots__ = _slots()

    def __init__(self, *args, **kwargs):
        "Raises an error since this is an abstract class."
        raise NotImplementedError("This is an abstract class!")

    @property
    def __name__(self):
        "Provides a way for callable instances to be identified."
        return type(self).__name__


class DatePart(_NamedInstance):
    "DatePart(part, column, name=None) -> DatePart"

    __slots__ = _slots("part column name")

    def __init__(self, part, column, name=None):
        "Initializes DatePart instance usable with 'group_by' method."
        self.__part = part.upper()
        self.__column = column
        self.__name = name

    def __call__(self, row):
        "Extract specified part of date from column in row."
        date = row[self.__column]
        if self.__part == "Y":
            return date.year
        if self.__part == "Q":
            return (date.month - 1) // 3 + 1
        if self.__part == "M":
            return date.month
        if self.__part == "D":
            return date.month
        raise ValueError("DatePart code cannot be processed!")

    ########################################################################

    @property
    def name(self):
        "Provides a name for us in the 'group_by' method."
        return self.__name


class MID(_NamedInstance):
    "MID(start, length=None) -> MID"

    __slots__ = _slots("start stop")

    def __init__(self, start, length=None):
        "Intializes MID instance with data to extract a sub-interval."
        self.__start = start - 1
        self.__stop = None if length is None else self.__start + length

    def __call__(self, data):
        "Returns sub-internal as specified upon instantiation."
        if self.__stop is None:
            return data[self.__start :]
        return data[self.__start : self.__stop]


class FORMAT(_NamedInstance):
    "FORMAT(spec) -> FORMAT"

    __slots__ = _slots("spec")

    def __init__(self, spec):
        "Initializes instance with 'spec' for the format function."
        self.__spec = spec

    def __call__(self, data):
        "Returns result from format function based on data and spec."
        return format(data, self.__spec)


def _pre_process(table, prefix):
    "Creates a table iterator that can cache results with optional prefix."
    iterator = iter(table)
    columns = next(iterator)
    if prefix == "_":
        for row in iterator:
            yield dict(zip(columns, row))
    else:
        for row in iterator:
            yield {
                "{}.{}".format(prefix, column): value
                for column, value in zip(columns, row)
            }


class datetime(datetime.datetime):
    """datetime(year=None, month=None, day=None, hour=0,
    minute=0, second=0, microsecond=0, tzinfo=None) -> datetime"""

    __slots__ = _slots()

    def __new__(
        cls,
        year=None,
        month=None,
        day=None,
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
        tzinfo=None,
    ):
        "Creates a customized datetime object that does not require arguments."
        if year is None:
            year, month, day = cls.max.year, cls.max.month, cls.max.day
        elif isinstance(year, bytes):
            year_high, year_low, _month, day, hour, minute, second, a, b, c = year
            year = (year_high << 8) + year_low
            microsecond = (((a << 8) | b) << 8) | c
            if month is None or isinstance(month, datetime._tzinfo_class):
                tzinfo = month
            else:
                raise TypeError("bad tzinfo state arg {!r}".format(month))
            month = _month
        return super().__new__(
            cls, year, month, day, hour, minute, second, microsecond, tzinfo
        )

    def date(self):
        d = super().date()
        return date(d.year, d.month, d.day)


class date(datetime.date):
    "date(year=None, month=None, day=None) -> date"

    __slots__ = _slots()

    def __new__(cls, year=None, month=None, day=None):
        "Creates a customized date object that does not require arguments."
        if year is None:
            year, month, day = cls.max.year, cls.max.month, cls.max.day
        elif isinstance(year, bytes):
            year_high, year_low, month, day = year
            year = (year_high << 8) + year_low
        return super().__new__(cls, year, month, day)

    def __str__(self):
        return self.strftime("%d-%b-%Y").upper()

    def __format__(self, length):
        return str(self).ljust(int(length))