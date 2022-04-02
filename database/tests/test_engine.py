from engine import ROW
from table import Table


def test():
    "Runs several groups of tests of the database engine."
    # Test simple statements in SQL.
    persons = test_basic_sql()
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


def test_basic_sql():
    """Tests simple statements in SQL."""
    # Test create table statement.
    persons = Table(
        ("P_Id", int),
        ("LastName", str),
        ("FirstName", str),
        ("Address", str),
        ("City", str),
    )
    # Populate the table with rows.
    persons.insert(1, "Hansen", "Ola", "Timoteivn 10", "Sandnes")
    persons.insert(2, "Svendson", "Tove", "Borgvn 23", "Sandnes")
    persons.insert(3, "Pettersen", "Kari", "Storgt 20", "Stavanger")
    persons.print()
    # Test the select statement.
    persons.select("LastName", "FirstName").print()
    persons.select().print()
    # Test the distinct statement.
    persons.select("City").distinct().print()
    # Test the where clause.
    persons.where(ROW.City == "Sandnes").print()
    # Test the and operator.
    persons.where((ROW.FirstName == "Tove") & (ROW.LastName == "Svendson")).print()
    # Test the or operator.
    persons.where((ROW.FirstName == "Tove") | (ROW.FirstName == "Ola")).print()
    # Test both and & or operators.
    persons.where(
        (ROW.LastName == "Svendson")
        & ((ROW.FirstName == "Tove") | (ROW.FirstName == "Ola"))
    ).print()
    # Test order by statement.
    persons.insert(4, "Nilsen", "Tom", "Vingvn 23", "Stavanger")
    persons.order_by("LastName").table().print()
    persons.order_by("LastName", True).table().print()
    # Test insert statement.
    persons.insert(5, "Nilsen", "Johan", "Bakken 2", "Stavanger")
    persons.print()
    persons.insert(P_Id=6, LastName="Tjessem", FirstName="Jakob")
    persons.print()
    # Test update statement.
    persons.where((ROW.LastName == "Tjessem") & (ROW.FirstName == "Jakob")).update(
        Address="Nissestien 67", City="Sandnes"
    )
    persons.print()
    copy = persons.order_by("P_Id").table()
    copy.update(Address="Nissestien 67", City="Sandnes")
    copy.print()
    # Test delete statement.
    copy = persons.order_by("P_Id").table()
    copy.delete((ROW.LastName == "Tjessem") & (ROW.FirstName == "Jakob")).print()
    copy.truncate().print()
    return persons


def test_row_selection(persons):
    "Tests various ways to select rows."
    # Test top clause.
    Table.from_iter(persons.top(2)).print()
    Table.from_iter(persons.top(0.5)).print()
    # Test like operator.
    persons.where(Like("City", "s.*")).print()
    persons.where(Like("City", ".*s")).print()
    persons.where(Like("City", ".*tav.*")).print()
    persons.where(NotLike("City", ".*tav.*")).print()
    # Test wildcard patterns.
    persons.where(Like("City", "sa.*")).print()
    persons.where(Like("City", ".*nes.*")).print()
    persons.where(Like("FirstName", ".la")).print()
    persons.where(Like("LastName", "S.end.on")).print()
    persons.where(Like("LastName", "[bsp].*")).print()
    persons.where(Like("LastName", "[^bsp].*")).print()
    # Test in operator.
    persons.where(ROW.LastName.in_("Hansen", "Pettersen")).print()
    # Test manual between syntax.
    persons.where(("Hansen" < ROW.LastName) < "Pettersen").print()
    persons.where(("Hansen" <= ROW.LastName) < "Pettersen").print()
    persons.where(("Hansen" <= ROW.LastName) <= "Pettersen").print()
    persons.where(("Hansen" < ROW.LastName) <= "Pettersen").print()


def test_all_joins(persons):
    "Tests the four different types of joins in SQL."
    # Create and populate the Orders table.
    orders = Table(("O_Id", int), ("OrderNo", int), ("P_Id", int))
    orders.insert(1, 77895, 3)
    orders.insert(2, 44678, 3)
    orders.insert(3, 22456, 1)
    orders.insert(4, 24562, 1)
    orders.insert(5, 34764, 15)
    # Test the inner join function.
    inner_join(
        ROW.Persons.P_Id == ROW.Orders.P_Id, Persons=persons, Orders=orders
    ).select("Persons.LastName", "Persons.FirstName", "Orders.OrderNo").order_by(
        "Persons.LastName"
    ).table().print()
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
    return orders


def test_table_addition(persons, orders):
    "Tests unstructured ways of joining tables together."
    # Create two tables to union together.
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
    "Tests creation and manipulation of databases."
    # Test ability to create database.
    db = Database()
    # Test creating and retrieving database tables.
    db.create("persons", Table(("Name", str), ("Credit", int)))
    db.create("mapdata", (("time", float), ("place", complex)))
    db.print()
    db.persons.insert("Marty", 7 ** 4)
    db.persons.insert(Name="Haddock")
    db.persons.print()


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


def test_generic_column_functions(persons, northwind):
    "Tests ability to select columns with function processing."
    # Test as_ and select with functions run on columns.
    persons.select((str.upper, "LastName"), "FirstName").as_(
        ("upper(LastName)", "LastName")
    ).print()
    persons.select((str.lower, "LastName"), "FirstName").as_(
        ("lower(LastName)", "LastName")
    ).print()
    persons.select((MID(1, 4), "City")).as_(("MID(City)", "SmallCity")).print()
    persons.select((len, "Address")).as_(("len(Address)", "LengthOfAddress")).print()
    northwind["Products"].select("ProductName", (round, "UnitPrice")).as_(
        ("round(UnitPrice)", "UnitPrice")
    ).print()
    current_products = northwind["Products"].select(
        "ProductName", "UnitPrice", (NOW, "PerDate")
    )
    current_products.print()
    current_products.select(
        "ProductName", "UnitPrice", (FORMAT("%Y-%m-%d"), "PerDate")
    ).as_(("FORMAT(PerDate)", "PerDate")).print()


def test_transactional_database():
    "Tests Database2 instances that support transactions."
    # Create a test database, tables, and dummy data.
    db2 = Database2()
    db2.create("test", Table(("id", int), ("name", str)))
    db2.test.insert(100, "Adam")
    db2.test.print()
    # Test the rollback transaction support added in Database2.
    test = db2.begin_transaction("test")
    test.insert(101, "Eve")
    test.print()
    db2.rollback_transaction("test")
    db2.test.print()
    # Test the commit transaction support added in Database2.
    test = db2.begin_transaction("test")
    test.insert(102, "Seth")
    test.print()
    db2.commit_transaction("test")
    db2.test.print()
    # Prepare some supports for the test that follows.
    import time

    def delay(seconds, handler, table):
        time.sleep(seconds)
        handler(table)

    def async_commit(db, action, table, wait):
        _thread.start_new_thread(
            delay, (wait, getattr(db, action + "_transaction"), table)
        )

    try:
        nw2 = Database2.load("northwind2.db")
    except IOError:
        return
    # Test waiting on a locked table before transaction.
    print("Starting transaction ...")
    categories = nw2.begin_transaction("Categories")
    print("Simulating processing ...")
    async_commit(nw2, "commit", "Categories", 2)
    print("Holding for release ...")
    categories = nw2.begin_transaction("Categories", True)
    print("Rolling back the table ...")
    nw2.rollback_transaction("Categories")
    return nw2
