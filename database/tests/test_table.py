from row import ROW


def test_create(persons):
    assert (
        persons
        == """\
P_ID LASTNAME  FIRSTNAME ADDRESS      CITY     
---- --------- --------- ------------ ---------
   1 Hansen    Ola       Timoteivn 10 Sandnes  
   2 Svendson  Tove      Borgvn 23    Sandnes  
   3 Pettersen Kari      Storgt 20    Stavanger\
"""
    )


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
    assert (
        persons.select("LastName", "FirstName")
        == """\
LASTNAME  FIRSTNAME
--------- ---------
Hansen    Ola      
Svendson  Tove     
Pettersen Kari     \
"""
    )

    assert (
        persons.select()
        == """\
P_ID LASTNAME  FIRSTNAME ADDRESS      CITY     
---- --------- --------- ------------ ---------
   1 Hansen    Ola       Timoteivn 10 Sandnes  
   2 Svendson  Tove      Borgvn 23    Sandnes  
   3 Pettersen Kari      Storgt 20    Stavanger\
"""
    )


def test_distinct(persons):
    assert (
        persons.select("City").distinct()
        == """\
CITY     
---------
Sandnes  
Stavanger\
"""
    )


def test_where(persons):
    assert (
        persons.where(ROW.City == "Sandnes")
        == """\
P_ID LASTNAME FIRSTNAME ADDRESS      CITY   
---- -------- --------- ------------ -------
   1 Hansen   Ola       Timoteivn 10 Sandnes
   2 Svendson Tove      Borgvn 23    Sandnes\
"""
    )


def test_and(persons):
    assert (
        persons.where((ROW.FirstName == "Tove") & (ROW.LastName == "Svendson"))
        == """\
P_ID LASTNAME FIRSTNAME ADDRESS      CITY
---- -------- --------- ------------ -------
   2 Svendson Tove      Borgvn 23    Sandnes\
"""
    )

    # Test the or operator.
    persons.where((ROW.FirstName == "Tove") | (ROW.FirstName == "Ola")).print()
    # Test both and & or operators.
    persons.where(
        (ROW.LastName == "Svendson")
        & ((ROW.FirstName == "Tove") | (ROW.FirstName == "Ola"))
    ).print()


def test_order_by(persons):
    persons.insert(4, "Nilsen", "Tom", "Vingvn 23", "Stavanger")
    persons.order_by("LastName").table().print()
    persons.order_by("LastName", True).table().print()


def test_insert(persons):
    persons.insert(5, "Nilsen", "Johan", "Bakken 2", "Stavanger")
    persons.print()
    persons.insert(P_Id=6, LastName="Tjessem", FirstName="Jakob")
    persons.print()


def test_update(persons):
    persons.where((ROW.LastName == "Tjessem") & (ROW.FirstName == "Jakob")).update(
        Address="Nissestien 67", City="Sandnes"
    )
    persons.print()
    copy = persons.order_by("P_Id").table()
    copy.update(Address="Nissestien 67", City="Sandnes")
    copy.print()


def test_delete(persons):
    copy = persons.order_by("P_Id").table()
    copy.delete((ROW.LastName == "Tjessem") & (ROW.FirstName == "Jakob")).print()
    copy.truncate().print()
