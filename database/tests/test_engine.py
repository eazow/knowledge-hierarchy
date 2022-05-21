import sys

from engine import Database
from row import ROW
from table import Table, inner_join, union
from utils import date, datetime


def test_table_addition(persons, orders):
    """Tests unstructured ways of joining tables together."""
    employees_norway = Table(("E_ID", str), ("E_Name", str))
    employees_norway.insert("01", "Hansen, Ola")
    employees_norway.insert("02", "Svendson, Tove")
    employees_norway.insert("03", "Svendson, Stephen")
    employees_norway.insert("04", "Pettersen, Kari")
    employees_usa = Table(("E_ID", str), ("E_Name", str))
    employees_usa.insert("01", "Turner, Sally")
    employees_usa.insert("02", "Kent, Clark")
    employees_usa.insert("03", "Svendson, Stephen")
    employees_usa.insert("04", "Scott, Stephen")
    # Test union function on tables.
    union(employees_norway("E_Name"), employees_usa("E_Name")).print()
    union(employees_norway("E_Name"), employees_usa("E_Name"), True).print()
    # Test select into functionality.
    backup = Table(*persons.schema)
    persons.into(backup)
    backup.print()
    backup.truncate()
    persons.select("LastName", "FirstName").into(backup)
    backup.print()
    # Test select into with where and join clauses.
    backup = Table(("LastName", str), ("FirstName", str))
    persons.where(ROW.City == "Sandnes").select("LastName", "FirstName").into(backup)
    backup.print()
    person_orders = Table(("Persons.LastName", str), ("Orders.OrderNo", int))
    inner_join(
        ROW.Persons.P_Id == ROW.Orders.P_Id, Persons=persons, Orders=orders
    ).select("Persons.LastName", "Orders.OrderNo").into(person_orders)
    person_orders.print()


def test_database_support():
    """Tests creation and manipulation of databases."""
    db = Database()

    db.create("persons", Table(("Name", str), ("Credit", int)))
    db.create("map_data", (("time", float), ("place", complex)))

    db.persons.insert("Marty", 7 ** 4)
    db.persons.insert(Name="Haddock")

    assert len(db.persons) == 2
    assert len(db.map_data) == 0


def test_date_functionality():
    """Tests different date operations that can be performed."""
    orders = Table(("OrderId", int), ("ProductName", str), ("OrderDate", date))
    orders.insert(1, "Geitost", date(2008, 11, 11))
    orders.insert(2, "Camembert Pierrot", date(2008, 11, 9))
    orders.insert(3, "Mozzarella di Giovanni", date(2008, 11, 11))
    orders.insert(4, "Mascarpone Fabioloi", date(2008, 10, 29))

    assert len(orders.where(ROW.OrderDate == date(2008, 11, 11))) == 2


    orders.alter_column("OrderDate", datetime)
    orders.where(ROW.OrderId == 1).update(OrderDate=datetime(2008, 11, 11, 13, 23, 44))
    orders.where(ROW.OrderId == 2).update(OrderDate=datetime(2008, 11, 9, 15, 45, 21))
    orders.where(ROW.OrderId == 3).update(OrderDate=datetime(2008, 11, 11, 11, 12, 1))
    orders.where(ROW.OrderId == 4).update(OrderDate=datetime(2008, 10, 29, 14, 56, 59))

    assert len(orders.where(ROW.OrderDate == datetime(2008, 11, 11))) == 0
    assert len(orders.where(ROW.OrderDate == datetime(2008, 11, 11, 13, 23, 44))) == 1


def test_column_functions():
    """Tests various functions that operate on specified column."""
    orders = Table(
        ("O_Id", int), ("OrderDate", date), ("OrderPrice", int), ("Customer", str)
    )
    orders.insert(1, date(2008, 11, 12), 1000, "Hansen")
    orders.insert(2, date(2008, 10, 23), 1600, "Nilsen")
    orders.insert(3, date(2008, 9, 2), 700, "Hansen")
    orders.insert(4, date(2008, 9, 3), 300, "Hansen")
    orders.insert(5, date(2008, 9, 30), 2000, "Jensen")
    orders.insert(6, date(2008, 10, 4), 100, "Nilsen")

    order_average = orders.avg("OrderPrice")
    assert order_average == 950
    assert len(orders.where(ROW.OrderPrice > order_average)) == 3

    # Test the "count" function.
    assert orders.where(ROW.Customer == "Nilsen").count("Customer") == 2
    assert orders.count() == 6
    assert orders.select("Customer").distinct().count("Customer") == 3

    # Test the "first" function.
    print("FirstOrderPrice =", orders.first("OrderPrice"))
    # Test the "last" function.
    print("LastOrderPrice =", orders.last("OrderPrice"))
    # Test the "max_" function.
    print("LargestOrderPrice =", orders.max_("OrderPrice"))
    # Test the "min_" function.
    print("SmallestOrderPrice =", orders.min_("OrderPrice"))
    # Test the "sum_" function.
    print("OrderTotal =", orders.sum_("OrderPrice"), "\n")
    # Test the "group_by" statement.
    result = Table(("Customer", str), ("OrderPrice", int))
    for table in orders.group_by("Customer"):
        result.insert(table.first("Customer"), table.sum_("OrderPrice"))
    result.print()
    # Add some more orders to the table.
    orders.insert(7, date(2008, 11, 12), 950, "Hansen")
    orders.insert(8, date(2008, 10, 23), 1900, "Nilsen")
    orders.insert(9, date(2008, 9, 2), 2850, "Hansen")
    orders.insert(10, date(2008, 9, 3), 3800, "Hansen")
    orders.insert(11, date(2008, 9, 30), 4750, "Jensen")
    orders.insert(12, date(2008, 10, 4), 5700, "Nilsen")
    # Test ability to group by several columns.
    result.truncate().alter_add("OrderDate", date)
    for table in orders.group_by("Customer", "OrderDate"):
        result.insert(
            table.first("Customer"), table.sum_("OrderPrice"), table.first("OrderDate")
        )
    result.print()
