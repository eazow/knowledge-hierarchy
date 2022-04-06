from row import ROW
from table import Table


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
