import copy
import pickle
import sys

from where import _Where
from row import rows, RowAdapter, ROW
from column import _Columns
from utils import slots, _pre_process


class Table:
    """Table(*columns) -> Table"""

    @classmethod
    def from_iter(cls, iterator):
        """Generates a table from a column / rows iterator."""
        title, test_row, *rows = iterator
        table = cls(*zip(title, map(type, test_row)))
        table.insert(*test_row)
        for row in rows:
            table.insert(*row)
        return table

    __slots__ = slots("columns data_area row_index")

    def __init__(self, *columns):
        """Initializes Table with columns and row storage area."""
        self.__columns = _Columns(columns)
        self.__data_area = {}
        self.__row_index = 1

    def __len__(self):
        """Returns the number of rows in the table."""
        return len(self.__data_area)

    def __repr__(self):
        """Creates a complete representation of the table."""
        buffer = [
            list(
                map(
                    repr,
                    ["ROW_ID"] + [name for index, name, data_type in self.__columns],
                )
            )
        ]
        width = [0] * len(buffer[0])
        for row in sorted(self.__data_area):
            buffer.append(
                list(
                    map(
                        repr,
                        [row]
                        + [
                            self.__data_area[row][index]
                            for index, name, data_type in self.__columns
                        ],
                    )
                )
            )
        for row in buffer:
            for index, string in enumerate(row):
                width[index] = max(width[index], len(string))
        string = ""
        for index, value in enumerate(buffer[0]):
            string += value.ljust(width[index]) + " | "
        string = string[:-3] + "\n"
        for index in range(len(buffer[0])):
            string += "-" * width[index] + "-+-"
        string = string[:-3] + "\n"
        for row in buffer[1:]:
            for index, value in enumerate(row):
                string += value.ljust(width[index]) + " | "
            string = string[:-3] + "\n"
        return string[:-1]

    def __str__(self):
        names, *rows = self
        columns = {name: [] for name in names}
        for row in rows:
            for key, value in zip(names, row):
                columns[key].append(value)
        lengths = tuple(
            max(len(str(value)) for value in columns[key] + [key]) for key in names
        )
        template = " ".join(map("{{:{}}}".format, lengths))
        lines = [
            template.format(*map(str.upper, names)),
            " ".join(map("-".__mul__, lengths)),
        ]
        for row in zip(*map(columns.__getitem__, names)):
            lines.append(template.format(*row))
        return "\n".join(lines)

    def __iter__(self):
        """Returns an iterator over the table's columns."""
        return self(*self.columns)

    def __call__(self, *columns):
        """Returns an iterator over the specified columns."""
        indexes = tuple(self.__columns[name][1] for name in columns)
        yield columns
        for row in sorted(self.__data_area):
            yield tuple(self.__data_area[row][index] for index in indexes)

    def __eq__(self, other):
        return str(self) == str(other)

    def first(self, column=None):
        """Returns the first row or column of specified row."""
        return self.__get_location(min, column)

    def last(self, column=None):
        """Returns the last row or column of specified row."""
        return self.__get_location(max, column)

    def print(self, end="\n\n", file=None):
        """Provides a convenient way of printing representation of the table."""
        print(repr(self), end=end, file=sys.stdout if file is None else file)

    def top(self, amount):
        """Iterates over the top rows specified by amount."""
        if amount == -1:
            amount = len(self.__data_area)
        elif 0 <= amount < 1:
            amount = round(amount * len(self.__data_area))
        assert isinstance(amount, int), "Amount was not understood!"
        for row, count in zip(self, range(amount + 1)):
            yield row

    def insert(self, *values, **columns):
        """Inserts provided data into a new row of the database."""
        if values:
            assert len(values) == len(self.__columns), "Bad number of columns!"
            assert not columns, "Mixed syntax is not accepted!"
            row = self.__insert_across(values)
        else:
            assert columns, "There is nothing to insert!"
            row = self.__insert_select(columns)
        self.__data_area[self.__row_index] = row
        self.__row_index += 1

    def alter_add(self, name, data_type):
        """Adds a column to the table and populates it."""
        index = self.__columns.add(name, data_type)
        started = False
        try:
            for row in self.__data_area.values():
                row[index] = data_type()
                started = True
        except TypeError:
            if started:
                raise
            for row in self.__data_area.values():
                row[index] = data_type

    def alter_drop(self, name):
        """Removes a column from the table and frees memory."""
        index = self.__columns.drop(name)
        for row in self.__data_area.values():
            del row[index]

    def alter_column(self, name, data_type):
        """Changes the data-type of a column and refreshes it."""
        index = self.__columns.alter(name, data_type)
        for row in self.__data_area.values():
            row[index] = data_type()

    def alter_name(self, old, new):
        """Renames a column without altering the rows."""
        self.__columns.rename(old, new)

    def as_(self, *pairs):
        """Changes the name of multiple columns at a time."""
        for old, new in pairs:
            self.alter_name(old, new)
        return self

    def copy(self):
        """Copies a table while sharing cell instances."""
        copy = type(self)()
        copy.__columns = self.__columns.copy()
        copy.__data_area = {}
        for key, value in self.__data_area.items():
            copy.__data_area[key] = value.copy()
        copy.__row_index = self.__row_index
        return copy

    def select(self, *column_names):
        """Select columns and process them with any given functions."""
        if not column_names:
            return self
        columns, functions = [], []
        for item in column_names:
            if isinstance(item, str):
                columns.append(item)
            elif isinstance(item, tuple):
                functions.append(item)
            else:
                raise TypeError(type(item))
        original = {name for index, name, data_type in self.__columns}
        excess = original - set(columns)
        if functions:
            return self.__select_with_function(excess, functions)
        copy = type(self)()
        copy.__columns = self.__columns.copy()
        copy.__data_area = self.__data_area
        copy.__row_index = self.__row_index
        for column in excess:
            copy.__columns.drop(column)
        return copy

    def distinct(self):
        """Return copy of table having only distinct rows."""
        copy = type(self)()
        copy.__columns = self.__columns
        copy.__data_area = self.__data_area.copy()
        copy.__row_index = self.__row_index
        valid_indexs = set()
        distinct_rows = set()
        for row in copy.__data_area:
            array = pickle.dumps(
                tuple(
                    copy.__data_area[row][index]
                    for index, name, data_type in self.__columns
                )
            )
            if array not in distinct_rows:
                valid_indexs.add(row)
                distinct_rows.add(array)
        for row in tuple(copy.__data_area):
            if row not in valid_indexs:
                del copy.__data_area[row]
        return copy

    def update(self, **assignments):
        """Changes all present rows with given assignments."""
        assign = []
        for name, value in assignments.items():
            data_type, index = self.__columns[name]
            assert isinstance(
                value, data_type
            ), "Wrong datatype: {} ({!r}, {!r})".format(name, value, data_type)
            assign.append((index, value))
        for row in self.__data_area.values():
            for index, value in assign:
                row[index] = value

    def where(self, test="and", **kw):
        """Select rows that fit criteria given by the test."""
        test = self.__process_test(test, kw)
        copy = type(self)()
        copy.__columns = self.__columns
        copy.__data_area = self.__data_area.copy()
        copy.__row_index = self.__row_index
        self.__remove(copy.__data_area, False, test)
        return copy

    def delete(self, test="and", **kw):
        """Delete rows that fit criteria given by the test."""
        test = self.__process_test(test, kw)
        self.__remove(self.__data_area, True, test)
        return self

    def truncate(self):
        """Deletes all of the rows in the table."""
        self.__data_area.clear()
        return self

    def order_by(self, column, desc=False):
        """Returns a sorted result of the table."""
        return _SortedResults(self, column, desc)

    def into(self, table):
        """Inserts external table into this table by column name."""
        self_iter = iter(self)
        self_colu = next(self_iter)
        for row in self_iter:
            table.insert(**{name: data for name, data in zip(self_colu, row)})

    def left_join(self, table, name, test):
        """Returns result of a left join on the given table using test."""
        return left_join(self, (table, name), test)

    def sum_(self, column):
        """Adds up all of the cells in a particular column of the table."""
        data_type, index = self.__columns[column]
        total = data_type()
        for row in self.__data_area:
            total += self.__data_area[row][index]
        return total

    def avg(self, column):
        """Averages the cells in the given column of the table."""
        size = len(self.__data_area)
        return self.sum_(column) / size if size else size

    def max_(self, column):
        """Finds the largest cell value from the column in the table."""
        index = self.__columns[column][1]
        return max(map(ROW[index], self.__data_area.values()))

    def min_(self, column):
        """Finds the smallest cell value from the column in the table."""
        index = self.__columns[column][1]
        return min(map(ROW[index], self.__data_area.values()))

    def count(self, column=None):
        """Counts the total number of 'non-null' cells in the given column."""
        if column is None:
            return len(self.__data_area)
        data_type, index = self.__columns[column]
        null, total = data_type(), 0
        for row in self.__data_area.values():
            if row[index] != null:
                total += 1
        return total

    def group_by(self, *columns):
        """Creates new tables from this table on matching columns."""
        column_map = {name: index for index, name, data_type in self.__columns}
        index_list = tuple(sorted(column_map.values()))
        schema = list(self.schema)
        tables = {}
        first = True
        for row_dict in self.__data_area.values():
            interest = []
            row = list(row_dict[index] for index in index_list)
            for name in columns:
                if isinstance(name, str):
                    interest.append(row_dict[column_map[name]])
                else:
                    interest.append(name(RowAdapter(row_dict, column_map)))
                    name = name.name
                    if name is not None:
                        data = interest[-1]
                        row.append(data)
                        if first:
                            signature = name, type(data)
                            if signature not in schema:
                                schema.append(signature)
            first = False
            key = tuple(interest)
            if key not in tables:
                tables[key] = type(self)(*schema)
            tables[key].insert(*row)
        return tables.values()

    def __get_location(self, function, column):
        """Returns a row or cell based on function and column."""
        row = self.__data_area[function(self.__data_area)]
        if column is None:
            return tuple(row[index] for index in sorted(row))
        return row[self.__columns[column][1]]

    def __insert_across(self, values):
        """Inserts values into new row while checking data types."""
        row = {}
        for value, (index, name, data_type) in zip(values, self.__columns):
            assert isinstance(
                value, data_type
            ), "Wrong datatype: {} ({!r}, {!r})".format(name, value, data_type)
            row[index] = value
        return row

    def __insert_select(self, values):
        """Inserts values into new row and fills in blank cells."""
        row = {}
        for name, value in values.items():
            data_type, index = self.__columns[name]
            assert isinstance(
                value, data_type
            ), "Wrong datatype: {} ({!r}, {!r})".format(name, value, data_type)
            row[index] = value
        for index, name, data_type in self.__columns:
            if index not in row:
                row[index] = data_type()
        return row

    def __remove(self, data_area, delete, test):
        """Removes rows from data area according to criteria."""
        column_map = {name: index for index, name, data_type in self.__columns}
        for row in tuple(data_area):
            value = test(RowAdapter(data_area[row], column_map))
            assert not isinstance(value, RowAdapter), "Test improperly formed!"
            if bool(value) == delete:
                del data_area[row]

    def __select_with_function(self, excess, functions):
        """Creates virtual rows formed by calling functions on columns."""
        table = self.copy()
        for code, data in functions:
            if data in table.__columns:
                data_name = "{}({})".format(code.__name__, data)
                data_type = type(code(next(rows(table(data)))[0]))
                table.alter_add(data_name, data_type)
                dest = table.__columns[data_name][1]
                sour = table.__columns[data][1]
                for row in table.__data_area.values():
                    row[dest] = code(row[sour])
            else:
                sour = code()
                table.alter_add(data, type(sour))
                dest = table.__columns[data][1]
                for row in table.__data_area.values():
                    row[dest] = copy.deepcopy(sour)
        for column in excess:
            table.alter_drop(column)
        return table

    @staticmethod
    def __process_test(test, kw):
        """Ensures that test has been properly formed as necessary."""
        if kw:
            test = _Where(test, kw)
        else:
            assert callable(test), "Test must be callable!"
        return test

    @property
    def columns(self):
        """Returns a list of column names from the table."""
        columns = sorted(self.__columns, key=lambda info: info[0])
        return tuple(map(lambda info: info[1], columns))

    @property
    def schema(self):
        """Returns table's schema that can be used to create another table."""
        return tuple((name, self.__columns[name][0]) for name in self.columns)


class _SortedResults:
    "_SortedResults(iterable column, desc) -> _SortedResults"

    __slots__ = slots("iter column direction")

    def __init__(self, iterable, column, desc):
        """Initializes sorting adapter with given data."""
        self.__iter = iterable
        self.__column = column
        self.__direction = desc

    def __iter__(self):
        """Iterates over internal data in the order requested."""
        title, *rows = tuple(self.__iter)
        index = title.index(self.__column)
        yield title
        for row in sorted(rows, key=ROW[index], reverse=self.__direction):
            yield row

    def order_by(self, column, desc=False):
        """Returns results that are sorted on an additional level."""
        return type(self)(self, column, desc)

    def table(self):
        """Converts the sorted results into a table object."""
        return Table.from_iter(self)


def inner_join(test, *table_arg, **table_kwarg):
    """Runs and returns result from inner joining two tables together."""
    pa, pb, ta, tb = _join_args(table_arg, table_kwarg)
    table = _composite_table(pa, pb, ta, tb)
    _join_loop(table, test, pa, pb, ta, tb, True, False)
    return table


def full_join(test, *table_arg, **table_kwarg):
    """Runs and returns result from full joining two tables together."""
    pa, pb, ta, tb = _join_args(table_arg, table_kwarg)
    table = _composite_table(pa, pb, ta, tb)
    _join_loop(table, test, pa, pb, ta, tb, False, True)
    return table


def left_join(table_a, table_b, test):
    """Runs and returns result from left joining two tables together."""
    assert (
        sum(isinstance(table, tuple) for table in (table_a, table_b)) > 0
    ), "At least one table must be given a name!"
    ta, pa = table_a if isinstance(table_a, tuple) else (table_a, "_")
    tb, pb = table_b if isinstance(table_b, tuple) else (table_b, "_")
    table = _composite_table(pa, pb, ta, tb)
    _join_loop(table, test, pa, pb, ta, tb, False, False)
    return table


def right_join(table_a, table_b, test):
    """Runs and returns result from right joining two tables together."""
    return left_join(table_b, table_a, test)


def _join_args(table_arg, table_kwarg):
    """Determines tables and prefixes from given arguments."""
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


def _join_loop(table, test, pa, pb, ta, tb, inner, full):
    """Joins two tables together into one table based on criteria."""
    first = True
    second = dict()
    table_a = tuple(_pre_process(ta, pa))
    table_b = tuple(_pre_process(tb, pb))
    for row_cache in table_a:
        match = False
        for add in table_b:
            row = row_cache.copy()
            row.update(add)
            if test(RowAdapter(row)):
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


def _composite_table(pa, pb, ta, tb):
    """Create a new table based on information from tables and prefixes."""
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


def union(table_a, table_b, all_=False):
    """Creates a table from two tables that have been combined."""
    table = Table.from_iter(table_a)
    for row in rows(table_b):
        table.insert(*row)
    if all_:
        return table
    return table.distinct()
