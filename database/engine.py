"""Module written to learn and understand more about databases.

The code in this module provides support for running a simple database engine
that runs completely in memory and allows usage of various concepts available
in a structured query language to get and set data that may be saved to file."""


import bz2
import copy
import datetime
import pickle
import sys
import types
import _thread

from table import Table
from utils import _slots


class Database:
    __slots__ = _slots("path data type view")

    @classmethod
    def load(cls, path):
        """Loads database from path and tests identity."""
        with open(path, "rb") as file:
            obj = pickle.loads(bz2.decompress(file.read()))
        assert isinstance(obj, cls), "Could not load a database object!"
        obj.__path = path
        return obj

    def __init__(self):
        """Initializes database object void of tables or views."""
        self.__path = None
        self.__setstate__(
            Table(("name", str), ("type", type), ("data", (Table, _View)))
        )

    def __repr__(self):
        """Returns the representation of the database."""
        return repr(self.__view.value)

    def __iter__(self):
        """Iterates over the names of the tables and views in the database."""
        for row in rows(self.__data("name")):
            yield self[row[0]]

    def __getattr__(self, name):
        "Allows getting table or view via attribute lookup or index notation."
        t = tuple(self.__data.where(ROW.name == name)("data"))
        assert len(t) < 3, "Name is ambiguous!"
        assert len(t) > 1, "Object was not found!"
        data = t[1][0]
        if isinstance(data, _View):
            return data.value
        return data

    __getitem__ = __getattr__

    def __getstate__(self):
        "Provides support for pickling and saving the database."
        return self.__data

    def __setstate__(self, state):
        "Helps with unpickling and adding needed instance variables."
        self.__data = state
        self.__type = Table(("type", type), ("name", str))
        self.__type.insert(Table, "table")
        self.__type.insert(_View, "view")
        self.__view = _View(
            None,
            lambda _: self.__data.left_join(
                self.__type, "Types", ROW.type == ROW.Types.type
            ).select(
                "name",
                "Types.name",
                (
                    lambda obj: float(len(obj) if isinstance(obj, Table) else "nan"),
                    "data",
                ),
            ),
            ("Types.name", "type"),
            ("<lambda>(data)", "size"),
        )

    def save(self, path=None):
        """Saves the database to path or most recently known path."""
        if path is None:
            assert self.__path is not None, "Path must be provided!"
            path = self.__path
        with open(path, "wb") as file:
            file.write(bz2.compress(pickle.dumps(self)))
        self.__path = path

    def create(self, name, schema_or_table_or_query, *name_changes):
        """Creates either a table or view for use in the database."""
        assert not self.__data.where(
            ROW.name == name
        ), "Name is already used and may not be overloaded!"
        if isinstance(schema_or_table_or_query, (tuple, list)):
            assert not name_changes, "Name changes not allowed with schema!"
            data = Table(*schema_or_table_or_query)
        elif isinstance(schema_or_table_or_query, Table):
            assert not name_changes, "Name changes not allowed with table!"
            data = schema_or_table_or_query
        else:
            data = _View(self, schema_or_table_or_query, *name_changes)
        self.__data.insert(name=name, type=type(data), data=data)
        return data

    def drop(self, name):
        "Deletes a table or view from the database."
        self.__data.delete(ROW.name == name)

    def print(self, end="\n\n", file=None):
        "Provides a simple way of showing a representation of the database."
        self.__view.value.print(end, file)

    def create_or_replace(self, name, schema_or_table_or_query, *name_changes):
        "Drops table or view before creating one with the same name."
        self.drop(name)
        self.create(name, schema_or_table_or_query, *name_changes)

    def inner_join(self, table_a, table_b, test):
        "Inner joins tables and views by name using test."
        return inner_join(test, **{table_a: self[table_a], table_b: self[table_b]})

    def full_join(self, table_a, table_b, test):
        "Full joins tables and views by name using test."
        return full_join(test, **{table_a: self[table_a], table_b: self[table_b]})


################################################################################


class Database2(Database):
    "Database2() -> Database2"

    @classmethod
    def upgrade(cls, db_old):
        "Upgrades the base version of a database into the child version."
        assert isinstance(db_old, cls.__base__), "Can only upgrade Database objects!"
        db_new = cls()
        db_new.__setstate__(db_old.__getstate__())
        db_new.save(db_old._Database__path)
        db_old.__init__()
        return db_new

    ########################################################################

    __slots__ = _slots("lock locked view")

    def __repr__(self):
        "Returns an updated representation of the database."
        return repr(self.__view.value)

    def __setstate__(self, state):
        "Sets up remaining attributes and prepares for transactions."
        super().__setstate__(state)
        self.__add_transaction_support()

    def __getstate__(self):
        "Reduces internal table to required columns and returns copy."
        self.__del_transaction_support()
        data = self.__data.copy()
        self.__extend_data()
        return data

    def __getattr__(self, name):
        "Allows contents to be accessed only if not in transaction."
        table = self.__data.where(name=name)
        assert len(table) < 2, "Name is abmiguous!"
        assert len(table) > 0, "Object was not found!"
        assert not table.first("lock").locked, "A transaction is in place!"
        if table.first("type") is _View:
            return table.first("data").value
        return table.first("data")

    __getitem__ = __getattr__

    ########################################################################

    def begin_transaction(self, table, wait=False):
        "Locks and copies table while optionally waiting for unlock."
        table = self.__data.where(name=table)
        assert table.first("type") is not _View, "Views are not supported!"
        lock = table.first("lock")
        if wait:
            lock.acquire()
            with self.__lock:  # Protects Critical Section
                data = table.first("data")
                table.update(copy=copy.deepcopy(data))
        else:
            with self.__lock:
                assert lock.acquire(False), "Table is locked in a transaction!"
                data = table.first("data")
                table.update(copy=copy.deepcopy(data))
        return data

    def commit_transaction(self, table):
        "Deletes reserve copy and unlocks the table."
        self.__close_transaction(table, self.__commit)

    def rollback_transaction(self, table):
        "Restores table with copy, removes copy, and unlocks the table."
        self.__close_transaction(table, self.__rollback)

    ########################################################################

    def __add_transaction_support(self):
        "Add attributes so database can support transactions."
        self.__lock = _thread.allocate_lock()
        self.__extend_data()
        self.__locked = _View(
            None,
            lambda _: self.__data.select(
                "name", (lambda lock: lock.locked, "lock")
            ).as_(("<lambda>(lock)", "locked")),
        )
        self.__view = _View(
            None,
            lambda _: self._Database__view.value.left_join(
                self.__locked.value, "Lock", ROW.name == ROW.Lock.name
            ).select("name", "type", "size", "Lock.locked"),
            ("Lock.locked", "locked"),
        )

    def __extend_data(self):
        "Adds columns to internal table as necessary."
        if ("type", type) not in self.__data.schema:
            self.__data.alter_add("type", type)
            for name, data in rows(self.__data("name", "data")):
                self.__data.where(name=name).update(type=type(data))
        self.__data.alter_add("lock", _Lock)
        self.__data.alter_add("copy", object)

    def __del_transaction_support(self):
        "Ensures no pending transactions and removes unsaved columns."
        assert not self.__locked.value.where(
            locked=True
        ), "You must commit all transactions before pickling!"
        self.__data.alter_drop("type")
        self.__data.alter_drop("lock")
        self.__data.alter_drop("copy")

    def __close_transaction(self, table, action):
        "Finishes taking care of a transaction's end."
        table = self.__data.where(name=table)
        assert table.first("type") is not _View, "Views are not supported!"
        lock = table.first("lock")
        # Begin Critical Section
        with self.__lock:
            try:
                lock.release()
            except _thread.error:
                raise ValueError("Table was not in a transaction!")
            action(table)
        # End Critical Section

    ########################################################################

    @staticmethod
    def __commit(table):
        "Deletes the reserve copy of a table."
        table.update(copy=object())

    @staticmethod
    def __rollback(table):
        "Restores table from copy and deletes the copy."
        table.update(data=table.first("copy"), copy=object())

    ########################################################################

    @property
    def __data(self):
        "Aliases internal table from Database class."
        return self._Database__data


################################################################################


class _Lock:
    "_Lock(immediate=False, silent=False) -> _Lock"

    __slots__ = _slots("lock verbose")

    def __init__(self, immediate=False, silent=False):
        "Initializes _Lock instance with internal mechanism."
        self.__lock = _thread.allocate_lock()
        self.__verbose = silent
        if immediate:
            self.acquire()

    ########################################################################

    def acquire(self, wait=True):
        "Acquires lock with an optional wait."
        return self.__lock.acquire(wait)

    def release(self, exc_type=None, exc_value=None, traceback=None):
        "Release lock if locked or possibly throws error."
        try:
            self.__lock.release()
        except _thread.error:
            if self.__verbose:
                raise

    ########################################################################

    __enter__ = acquire

    __exit__ = release

    ########################################################################

    @property
    def locked(self):
        "Returns whether or not lock is currently locked."
        return self.__lock.locked()


################################################################################


################################################################################


class _Columns:
    "_Columns(columns) -> _Columns"

    __slots__ = _slots("column_index column_names")

    def __init__(self, columns):
        "Initializes Columns instance with names and data types."
        self.__column_index = 1
        self.__column_names = UniqueDict()
        for name, data_type in columns:
            self.add(name, data_type)

    def __contains__(self, name):
        "Checks if the named column already exists."
        return name in self.__column_names

    def __len__(self):
        "Returns the number of columns recognizes."
        return len(self.__column_names)

    def __iter__(self):
        "Iterates over columns in sorted order."
        cache = []
        for name, (data_type, index) in self.__column_names.items():
            cache.append((index, name, data_type))
        for item in sorted(cache):
            yield item

    def __getitem__(self, name):
        "Returns requested information on the given column name."
        return self.__column_names[name]

    def __getstate__(self):
        "Provides support for class instances to be pickled."
        return self.__column_index, self.__column_names

    def __setstate__(self, state):
        "Sets the state while object in being unpickled."
        self.__column_index, self.__column_names = state

    ########################################################################

    def copy(self):
        "Creates a copy of the known columns."
        copy = type(self)([])
        copy.__column_index = self.__column_index
        copy.__column_names = self.__column_names.copy()
        return copy

    def add(self, name, data_type):
        "Adds a column name with data type and assigns an index."
        index = self.__column_index
        self.__column_names[name] = data_type, index
        self.__column_index += 1
        return index

    def drop(self, name):
        "Removes all information regarding the named column."
        index = self.__column_names[name][1]
        del self.__column_names[name]
        return index

    def alter(self, name, data_type):
        "Changes the data type of the named column."
        index = self.__column_names[name][1]
        self.__column_names.replace(name, (data_type, index))
        return index

    def rename(self, old, new):
        "Renames a column from old name to new name."
        self.__column_names[new] = self.__column_names[old]
        del self.__column_names[old]


################################################################################


class UniqueDict(dict):
    "UniqueDict(iterable=None, **kwargs) -> UniqueDict"

    __slots__ = ()

    def __setitem__(self, key, value):
        "Sets key with value if key does not exist."
        assert key not in self, "Key already exists!"
        super().__setitem__(key, value)

    def replace(self, key, value):
        "Sets key with value if key already exists."
        assert key in self, "Key does not exist!"
        super().__setitem__(key, value)


################################################################################


class _RowAdapter:
    "_RowAdapter(row, column_map=None) -> _RowAdapter"

    __slots__ = _slots("row map")

    def __init__(self, row, column_map=None):
        "Initializes _RowAdapter with data and mapping information."
        self.__row = row
        self.__map = column_map

    def __getattr__(self, column):
        "Returns a column from the row this instance in adapting."
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

    ########################################################################

    def __unmapped(self, column):
        "Processes a row with column names already filled in."
        if column in self.__row:
            return self.__row[column]
        row = {}
        column += "."
        for name in self.__row:
            if name.startswith(column):
                row[name[len(column) :]] = self.__row[name]
        assert row, "Name did not match any known column: " + repr(column)
        return type(self)(row)


################################################################################


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


################################################################################


class _View:
    "_View(database, query, *name_changes) -> _View"

    __slots__ = _slots("database query name_changes")

    def __init__(self, database, query, *name_changes):
        "Initializes _View instance with details of saved query."
        self.__database = database
        self.__query = query
        self.__name_changes = name_changes

    def __getstate__(self):
        "Returns everything needed to pickle _View instance."
        return self.__database, self.__query.__code__, self.__name_changes

    def __setstate__(self, state):
        "Sets the state of the _View instance when unpickled."
        database, query, name_changes = state
        self.__database = database
        self.__query = types.LambdaType(query, sys.modules, "", (), ())
        self.__name_changes = name_changes

    ########################################################################

    @property
    def value(self):
        "Caculates and returns the value of view's query."
        data = self.__query(self.__database)
        table = data if isinstance(data, Table) else Table.from_iter(data)
        for old, new in self.__name_changes:
            table.alter_name(old, new)
        return table


################################################################################


class _Where:
    "_Where(mode, condition) -> _Where"

    __slots__ = _slots("call rows")

    def __init__(self, mode, condition):
        "Initializes _Where support object for simple selections."
        self.__call = {"and": all, "or": any}[mode]
        self.__rows = condition

    def __call__(self, row):
        "Runs test on given row and validates against condition."
        return self.__call(row[k] == v for k, v in self.__rows.items())


################################################################################


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


################################################################################


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


################################################################################


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


################################################################################


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


################################################################################


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


################################################################################


class FORMAT(_NamedInstance):
    "FORMAT(spec) -> FORMAT"

    __slots__ = _slots("spec")

    def __init__(self, spec):
        "Initializes instance with 'spec' for the format function."
        self.__spec = spec

    def __call__(self, data):
        "Returns result from format function based on data and spec."
        return format(data, self.__spec)


################################################################################

del _slots
types.StringType = str
next_ = next
NOW = datetime.now


################################################################################


def inner_join(test, *table_arg, **table_kwarg):
    "Runs and returns result from inner joining two tables together."
    pa, pb, ta, tb = _join_args(table_arg, table_kwarg)
    table = _composite_table(pa, pb, ta, tb)
    _join_loop(table, test, pa, pb, ta, tb, True, False)
    return table


def full_join(test, *table_arg, **table_kwarg):
    "Runs and returns result from full joining two tables together."
    pa, pb, ta, tb = _join_args(table_arg, table_kwarg)
    table = _composite_table(pa, pb, ta, tb)
    _join_loop(table, test, pa, pb, ta, tb, False, True)
    return table


def left_join(table_a, table_b, test):
    "Runs and returns result from left joining two tables together."
    assert (
        sum(isinstance(table, tuple) for table in (table_a, table_b)) > 0
    ), "At least one table must be given a name!"
    ta, pa = table_a if isinstance(table_a, tuple) else (table_a, "_")
    tb, pb = table_b if isinstance(table_b, tuple) else (table_b, "_")
    table = _composite_table(pa, pb, ta, tb)
    _join_loop(table, test, pa, pb, ta, tb, False, False)
    return table


def right_join(table_a, table_b, test):
    "Runs and returns result from right joining two tables together."
    return left_join(table_b, table_a, test)


def union(table_a, table_b, all_=False):
    "Creates a table from two tables that have been combined."
    table = Table.from_iter(table_a)
    for row in rows(table_b):
        table.insert(*row)
    if all_:
        return table
    return table.distinct()


def rows(iterable):
    "Skips the first row (column names) from a table-style iterator."
    iterator = iter(iterable)
    next(iterator)
    return iterator


################################################################################


def _join_args(table_arg, table_kwarg):
    "Determines tables and prefixes from given arguments."
    assert len(table_kwarg) > 0, "At least one table name must be given!"
    assert (
        sum(map(len, (table_arg, table_kwarg))) == 2
    ), "Two tables must be provided to join!"
    if len(table_kwarg) == 2:
        (pa, pb), (ta, tb) = zip(*table_kwarg.items())
    else:
        pa, ta = next(iter(table_kwarg.items()))
        pb, tb = "_", table_arg[0]
    return pa, pb, ta, tb


def _composite_table(pa, pb, ta, tb):
    "Create a new table based on information from tables and prefixes."
    columns = []
    for table_name, table_obj in zip((pa, pb), (ta, tb)):
        iterator = iter(table_obj)
        names = next(iterator)
        types = map(lambda item: item[1], table_obj.schema)
        for column_name, column_type in zip(names, types):
            if table_name != "_":
                column_name = "{}.{}".format(table_name, column_name)
            columns.append((column_name, column_type))
    return Table(*columns)


def _join_loop(table, test, pa, pb, ta, tb, inner, full):
    "Joins two tables together into one table based on criteria."
    first = True
    second = dict()
    table_a = tuple(_pre_process(ta, pa))
    table_b = tuple(_pre_process(tb, pb))
    for row_cache in table_a:
        match = False
        for add in table_b:
            row = row_cache.copy()
            row.update(add)
            if test(_RowAdapter(row)):
                table.insert(**row)
                match = True
                if not first:
                    second.pop(id(add), None)
            elif first:
                second[id(add)] = add
        if not (inner or match):
            table.insert(**row_cache)
        first = False
    if full:
        for row in second.values():
            table.insert(**row)


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


################################################################################

# Unsupported Features:
# =====================
#   Constraints:
#   ------------
#     NOT NULL [forced on all columns]
#     UNIQUE
#     PRIMARY KEY
#     FOREIGN KEY
#     CHECK
#     DEFAULT [constructed from type]
#   Indexes:
#   --------
#     CREATE
#     DROP
#   Increment:
#   ----------
#     AUTO INCREMENT
#     Starting Value
#     Increment by X
#       ["ROW_ID" starts at and increments by 1 but is not accessible]
#   Dates:
#   ------
#     NOW()
#     CURDATE()
#     CURTIME()
#     EXTRACT()
#     DATE_ADD()
#     DATE_SUB()
#     DATEDIFF()
#     DATE_FORMAT()
#     GETDATE()
#     CONVERT()
#       ["DatePart" and "date" are supported and may
#        be supplemented with the "datetime" module]
#   Nulls:
#   ------
#     ISNULL()
#     NVL()
#     IFNULL()
#     COALESCE()
#       [the NOT NULL constraint is forced on all columns]
#   Data Types:
#   -----------
#     Data types that cannot be initialized with a
#     parameterless call are not directly supported.
#   Functions:
#   ----------
#     max() [use "table.max_(column)" instead]
#     min() [use "table.min_(column)" instead]
#     sum() [use "table.sum_(column)" instead]
#     Having Statement
#     ucase() or upper() [use "(str.upper, 'column')" instead]
#     lcase() or lower() [use "(str.lower, 'column')" instead)
#     Virtual Columns [Function Based]
#     Materialized Views [Cached Functions]
#   Transactions:
#   -------------
#     Table Level Transactions
#       [database level transactions are supported;
#        table locks are supported in the same way]

################################################################################

import itertools
import operator


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
            return _Comparison(self, lambda a, b: (not a, b)[0], None)
        return super().__getattr__(self.__name + "." + name)

    def __lt__(self, other):
        return _Comparison(self, operator.lt, other)

    def __le__(self, other):
        return _Comparison(self, operator.le, other)

    def __eq__(self, other):
        return _Comparison(self, operator.eq, other)

    def __ne__(self, other):
        return _Comparison(self, operator.ne, other)

    def __gt__(self, other):
        return _Comparison(self, operator.gt, other)

    def __ge__(self, other):
        return _Comparison(self, operator.ge, other)

    def in_(self, *items):
        return _Comparison(self, lambda a, b: a in b, items)


class _Comparison(_Repr):
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
        return _Comparison(self, lambda a, b: a and b, other)

    def __or__(self, other):
        return _Comparison(self, lambda a, b: a or b, other)


ROW = _Row()
