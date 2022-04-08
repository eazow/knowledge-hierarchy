from utils import _slots, UniqueDict


class _Columns:
    """_Columns(columns) -> _Columns"""

    __slots__ = _slots("column_index column_names")

    def __init__(self, columns):
        """Initializes Columns instance with names and data types."""
        self.__column_index = 1
        self.__column_names = UniqueDict()
        for name, data_type in columns:
            self.add(name, data_type)

    def __contains__(self, name):
        """Checks if the named column already exists."""
        return name in self.__column_names

    def __len__(self):
        """Returns the number of columns recognizes."""
        return len(self.__column_names)

    def __iter__(self):
        """Iterates over columns in sorted order."""
        cache = []
        for name, (data_type, index) in self.__column_names.items():
            cache.append((index, name, data_type))
        for item in sorted(cache):
            yield item

    def __getitem__(self, name):
        """Returns requested information on the given column name."""
        return self.__column_names[name]

    def __getstate__(self):
        """Provides support for class instances to be pickled."""
        return self.__column_index, self.__column_names

    def __setstate__(self, state):
        """Sets the state while object in being unpickled."""
        self.__column_index, self.__column_names = state

    def copy(self):
        """Creates a copy of the known columns."""
        copy = type(self)([])
        copy.__column_index = self.__column_index
        copy.__column_names = self.__column_names.copy()
        return copy

    def add(self, name, data_type):
        """Adds a column name with data type and assigns an index."""
        index = self.__column_index
        self.__column_names[name] = data_type, index
        self.__column_index += 1
        return index

    def drop(self, name):
        """Removes all information regarding the named column."""
        index = self.__column_names[name][1]
        del self.__column_names[name]
        return index

    def alter(self, name, data_type):
        """Changes the data type of the named column."""
        index = self.__column_names[name][1]
        self.__column_names.replace(name, (data_type, index))
        return index

    def rename(self, old, new):
        """Renames a column from old name to new name."""
        self.__column_names[new] = self.__column_names[old]
        del self.__column_names[old]