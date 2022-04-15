import sys
import types

from table import Table
from utils import slots


class _View:
    """_View(database, query, *name_changes) -> _View"""

    __slots__ = slots("database query name_changes")

    def __init__(self, database, query, *name_changes):
        """Initializes _View instance with details of saved query."""
        self.__database = database
        self.__query = query
        self.__name_changes = name_changes

    def __getstate__(self):
        """Returns everything needed to pickle _View instance."""
        return self.__database, self.__query.__code__, self.__name_changes

    def __setstate__(self, state):
        """Sets the state of the _View instance when unpickled."""
        database, query, name_changes = state
        self.__database = database
        self.__query = types.LambdaType(query, sys.modules, "", (), ())
        self.__name_changes = name_changes

    @property
    def value(self):
        """Caculates and returns the value of view's query."""
        data = self.__query(self.__database)
        table = data if isinstance(data, Table) else Table.from_iter(data)
        for old, new in self.__name_changes:
            table.alter_name(old, new)
        return table
