"""Module written to learn and understand more about databases.

The code in this module provides support for running a simple database engine
that runs completely in memory and allows usage of various concepts available
in a structured query language to get and set data that may be saved to file."""


import bz2
import copy
import pickle
import types
import _thread

from join import left_join, inner_join, full_join
from lock import _Lock
from row import rows, ROW
from table import Table
from utils import _slots, datetime
from view import _View


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
            lambda _: left_join(
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


class TransactionalDatabase(Database):

    @classmethod
    def upgrade(cls, db_old):
        "Upgrades the base version of a database into the child version."
        assert isinstance(db_old, cls.__base__), "Can only upgrade Database objects!"
        db_new = cls()
        db_new.__setstate__(db_old.__getstate__())
        db_new.save(db_old._Database__path)
        db_old.__init__()
        return db_new

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
            lambda _: left_join(
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


del _slots
types.StringType = str
next_ = next
NOW = datetime.now

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


