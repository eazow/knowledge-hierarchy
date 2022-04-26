import sys

from engine import Database, NOW
from row import ROW
from table import Table, inner_join, left_join, right_join, full_join, union
from utils import MID, date, datetime, FORMAT

"""
def test(persons):
    Runs several groups of tests of the database engine."
    # Test simple statements in SQL.
    # persons = test_basic_sql()
    # Test various ways to select rows.
    test_row_selection(persons)
    # Test the four different types of joins in SQL.
    orders = test_all_joins(persons)
    # Test unstructured ways of joining tables together.
    test_table_addition(persons, orders)
    # Test creation and manipulation of databases.
    test_database_support()
    # Load and run some test on the sample Northwind database.
    northwind = test_northwind()
    # Test different date operations that can be performed.
    test_date_functionality()
    # Test various functions that operate on specified column.
    test_column_functions()
    if northwind:
        # Test ability to select columns with function processing.
        test_generic_column_functions(persons, northwind)
    # Test Database2 instances that support transactions.
    nw2 = test_transactional_database()
    # Allow for interaction at the end of the test.
    globals().update(locals())
"""


def test_inner_join(persons, orders):
    assert (
        inner_join(ROW.Persons.P_Id == ROW.Orders.P_Id, Persons=persons, Orders=orders)
        .select("Persons.LastName", "Persons.FirstName", "Orders.OrderNo")
        .order_by("Persons.LastName")
        .table()
        == """\
PERSONS.LASTNAME PERSONS.FIRSTNAME ORDERS.ORDERNO
---------------- ----------------- --------------
Hansen           Ola                        22456
Hansen           Ola                        24562
Pettersen        Kari                       77895
Pettersen        Kari                       44678\
"""
    )


def test_all_joins(persons, orders):
    """Tests the four different types of joins in SQL."""

    # Test inner join with alias.
    inner_join(ROW.p.P_Id == ROW.po.P_Id, p=persons, po=orders).select(
        "po.OrderNo", "p.LastName", "p.FirstName"
    ).where((ROW.p.LastName == "Hansen") & (ROW.p.FirstName == "Ola")).print()
    # Test left join with and without alias.
    left_join(
        (persons, "Persons"), (orders, "Orders"), ROW.Persons.P_Id == ROW.Orders.P_Id
    ).select("Persons.LastName", "Persons.FirstName", "Orders.OrderNo").order_by(
        "Persons.LastName"
    ).table().print()
    left_join((persons, "p"), (orders, "o"), ROW.p.P_Id == ROW.o.P_Id).select(
        "p.LastName", "p.FirstName", "o.OrderNo"
    ).order_by("p.LastName").table().print()
    # Test right join with and without alias.
    right_join(
        (persons, "Persons"), (orders, "Orders"), ROW.Persons.P_Id == ROW.Orders.P_Id
    ).select("Persons.LastName", "Persons.FirstName", "Orders.OrderNo").order_by(
        "Persons.LastName"
    ).table().print()
    right_join((persons, "p"), (orders, "o"), ROW.p.P_Id == ROW.o.P_Id).select(
        "p.LastName", "p.FirstName", "o.OrderNo"
    ).order_by("p.LastName").table().print()
    # Test full join with and without alias.
    full_join(
        ROW.Persons.P_Id == ROW.Orders.P_Id, Persons=persons, Orders=orders
    ).order_by("Persons.LastName").table().print()
    full_join(ROW.p.P_Id == ROW.o.P_Id, p=persons, o=orders).select(
        "p.LastName", "p.FirstName", "o.OrderNo"
    ).order_by("p.LastName").table().print()


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
    # Test creating and retrieving database tables.
    db.create("persons", Table(("Name", str), ("Credit", int)))
    db.create("map_data", (("time", float), ("place", complex)))

    db.persons.insert("Marty", 7 ** 4)
    db.persons.insert(Name="Haddock")

    assert len(db.persons) == 2
    assert len(db.map_data) == 0


def test_northwind():
    "Loads and runs some test on the sample Northwind database."
    import os, imp

    # Patch the module namespace to recognize this file.
    name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    module = imp.new_module(name)
    vars(module).update(globals())
    sys.modules[name] = module
    # Load a Northwind database for various testing purposes.
    try:
        northwind = Database.load("northwind.db")
    except IOError:
        return
    # Create and test a current product list view.
    northwind.create(
        "Current Product List",
        lambda db: db.Products.where(ROW.Discontinued.NOT).select(
            "ProductID", "ProductName"
        ),
    )
    northwind["Current Product List"].print()

    # Find all products having an above-average price.
    def above_average_price(db):
        return db.Products.where(ROW.UnitPrice > db.Products.avg("UnitPrice")).select(
            "ProductName", "UnitPrice"
        )

    northwind.create("Products Above Average Price", above_average_price)
    northwind["Products Above Average Price"].print()

    # Calculate total sale per category in 1997.
    def category_sales_for_1997(db):
        result = Table(("CategoryName", str), ("CategorySales", decimal.Decimal))
        for table in db["Product Sales For 1997"].group_by("Categories.CategoryName"):
            name = next(rows(table.select("Categories.CategoryName")))[0]
            total = table.sum_("ProductSales")
            result.insert(name, total)
        return result

    northwind.create("Category Sales For 1997", category_sales_for_1997)
    northwind["Category Sales For 1997"].print()
    # Show just the Beverages Category from the previous view.
    northwind["Category Sales For 1997"].where(ROW.CategoryName == "Beverages").print()
    # Add the Category column to the Current Product List view.
    northwind.create_or_replace(
        "Current Product List",
        lambda db: db["Products View"]
        .where(ROW.Discontinued.NOT)
        .select("ProductID", "ProductName", "Category"),
    )
    northwind["Current Product List"].print()
    # Drop the Category Sales For 1997 view.
    northwind.drop("Category Sales For 1997")
    return northwind


def test_date_functionality():
    "Tests different date operations that can be performed."
    # Create an orderz table to test the date type.
    orderz = Table(("OrderId", int), ("ProductName", str), ("OrderDate", date))
    orderz.insert(1, "Geitost", date(2008, 11, 11))
    orderz.insert(2, "Camembert Pierrot", date(2008, 11, 9))
    orderz.insert(3, "Mozzarella di Giovanni", date(2008, 11, 11))
    orderz.insert(4, "Mascarpone Fabioloi", date(2008, 10, 29))
    # Query the table for a specific date.
    orderz.where(ROW.OrderDate == date(2008, 11, 11)).print()
    # Update the orderz table so that times are present with the dates.
    orderz.alter_column("OrderDate", datetime)
    orderz.where(ROW.OrderId == 1).update(OrderDate=datetime(2008, 11, 11, 13, 23, 44))
    orderz.where(ROW.OrderId == 2).update(OrderDate=datetime(2008, 11, 9, 15, 45, 21))
    orderz.where(ROW.OrderId == 3).update(OrderDate=datetime(2008, 11, 11, 11, 12, 1))
    orderz.where(ROW.OrderId == 4).update(OrderDate=datetime(2008, 10, 29, 14, 56, 59))
    # Query the table with a datetime object this time.
    orderz.where(ROW.OrderDate == datetime(2008, 11, 11)).print()


def test_column_functions():
    "Tests various functions that operate on specified column."
    # Create an order table to test various functions on.
    order = Table(
        ("O_Id", int), ("OrderDate", date), ("OrderPrice", int), ("Customer", str)
    )
    order.insert(1, date(2008, 11, 12), 1000, "Hansen")
    order.insert(2, date(2008, 10, 23), 1600, "Nilsen")
    order.insert(3, date(2008, 9, 2), 700, "Hansen")
    order.insert(4, date(2008, 9, 3), 300, "Hansen")
    order.insert(5, date(2008, 9, 30), 2000, "Jensen")
    order.insert(6, date(2008, 10, 4), 100, "Nilsen")
    # Test the "avg" function.
    order_average = order.avg("OrderPrice")
    print("OrderAverage =", order_average, "\n")
    order.where(ROW.OrderPrice > order_average).select("Customer").print()
    # Test the "count" function.
    print("CustomerNilsen =", order.where(ROW.Customer == "Nilsen").count("Customer"))
    print("NumberOfOrders =", order.count())
    print("NumberOfCustomers =", order.select("Customer").distinct().count("Customer"))
    # Test the "first" function.
    print("FirstOrderPrice =", order.first("OrderPrice"))
    # Test the "last" function.
    print("LastOrderPrice =", order.last("OrderPrice"))
    # Test the "max_" function.
    print("LargestOrderPrice =", order.max_("OrderPrice"))
    # Test the "min_" function.
    print("SmallestOrderPrice =", order.min_("OrderPrice"))
    # Test the "sum_" function.
    print("OrderTotal =", order.sum_("OrderPrice"), "\n")
    # Test the "group_by" statement.
    result = Table(("Customer", str), ("OrderPrice", int))
    for table in order.group_by("Customer"):
        result.insert(table.first("Customer"), table.sum_("OrderPrice"))
    result.print()
    # Add some more orders to the table.
    order.insert(7, date(2008, 11, 12), 950, "Hansen")
    order.insert(8, date(2008, 10, 23), 1900, "Nilsen")
    order.insert(9, date(2008, 9, 2), 2850, "Hansen")
    order.insert(10, date(2008, 9, 3), 3800, "Hansen")
    order.insert(11, date(2008, 9, 30), 4750, "Jensen")
    order.insert(12, date(2008, 10, 4), 5700, "Nilsen")
    # Test ability to group by several columns.
    result.truncate().alter_add("OrderDate", date)
    for table in order.group_by("Customer", "OrderDate"):
        result.insert(
            table.first("Customer"), table.sum_("OrderPrice"), table.first("OrderDate")
        )
    result.print()


# def test_generic_column_functions(persons, northwind):
#     "Tests ability to select columns with function processing."
#     # Test as_ and select with functions run on columns.
#     persons.select((str.upper, "LastName"), "FirstName").as_(
#         ("upper(LastName)", "LastName")
#     ).print()
#     persons.select((str.lower, "LastName"), "FirstName").as_(
#         ("lower(LastName)", "LastName")
#     ).print()
#     persons.select((MID(1, 4), "City")).as_(("MID(City)", "SmallCity")).print()
#     persons.select((len, "Address")).as_(("len(Address)", "LengthOfAddress")).print()
#     northwind["Products"].select("ProductName", (round, "UnitPrice")).as_(
#         ("round(UnitPrice)", "UnitPrice")
#     ).print()
#     current_products = northwind["Products"].select(
#         "ProductName", "UnitPrice", (NOW, "PerDate")
#     )
#     current_products.print()
#     current_products.select(
#         "ProductName", "UnitPrice", (FORMAT("%Y-%m-%d"), "PerDate")
#     ).as_(("FORMAT(PerDate)", "PerDate")).print()
