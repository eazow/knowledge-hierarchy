from row import ROW


def test_create(persons):
    assert persons == """\
P_ID LASTNAME  FIRSTNAME ADDRESS      CITY     
---- --------- --------- ------------ ---------
   1 Hansen    Ola       Timoteivn 10 Sandnes  
   2 Svendson  Tove      Borgvn 23    Sandnes  
   3 Pettersen Kari      Storgt 20    Stavanger\
"""


def test_repr(persons):  # persons.print()
    assert (
        repr(persons)
        == """\
'ROW_ID' | 'P_Id' | 'LastName'  | 'FirstName' | 'Address'      | 'City'     
---------+--------+-------------+-------------+----------------+------------
1        | 1      | 'Hansen'    | 'Ola'       | 'Timoteivn 10' | 'Sandnes'  
2        | 2      | 'Svendson'  | 'Tove'      | 'Borgvn 23'    | 'Sandnes'  
3        | 3      | 'Pettersen' | 'Kari'      | 'Storgt 20'    | 'Stavanger'\
"""
    )


def test_select(persons):
    assert persons.select("LastName", "FirstName") == """\
LASTNAME  FIRSTNAME
--------- ---------
Hansen    Ola      
Svendson  Tove     
Pettersen Kari     \
"""

    assert persons.select() == """\
P_ID LASTNAME  FIRSTNAME ADDRESS      CITY     
---- --------- --------- ------------ ---------
   1 Hansen    Ola       Timoteivn 10 Sandnes  
   2 Svendson  Tove      Borgvn 23    Sandnes  
   3 Pettersen Kari      Storgt 20    Stavanger\
"""


def test_distinct(persons):
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
