from row import _RowAdapter, rows
from utils import _pre_process
from table import Table


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


def union(table_a, table_b, all_=False):
    "Creates a table from two tables that have been combined."
    table = Table.from_iter(table_a)
    for row in rows(table_b):
        table.insert(*row)
    if all_:
        return table
    return table.distinct()