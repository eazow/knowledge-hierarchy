from like import Like, NotLike
from row import ROW
from table import Table


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
P_ID LASTNAME FIRSTNAME ADDRESS   CITY   
---- -------- --------- --------- -------
   2 Svendson Tove      Borgvn 23 Sandnes\
"""
    )


def test_or(persons):
    assert (
        persons.where((ROW.FirstName == "Tove") | (ROW.FirstName == "Ola"))
        == """\
P_ID LASTNAME FIRSTNAME ADDRESS      CITY   
---- -------- --------- ------------ -------
   1 Hansen   Ola       Timoteivn 10 Sandnes
   2 Svendson Tove      Borgvn 23    Sandnes\
"""
    )


def test_and_or(persons):
    assert (
        persons.where(
            (ROW.LastName == "Svendson")
            & ((ROW.FirstName == "Tove") | (ROW.FirstName == "Ola"))
        )
        == """\
P_ID LASTNAME FIRSTNAME ADDRESS   CITY   
---- -------- --------- --------- -------
   2 Svendson Tove      Borgvn 23 Sandnes\
"""
    )


def test_order_by(persons):
    persons.insert(4, "Nilsen", "Tom", "Vingvn 23", "Stavanger")

    assert (
        persons.order_by("LastName").table()
        == """\
P_ID LASTNAME  FIRSTNAME ADDRESS      CITY     
---- --------- --------- ------------ ---------
   1 Hansen    Ola       Timoteivn 10 Sandnes  
   4 Nilsen    Tom       Vingvn 23    Stavanger
   3 Pettersen Kari      Storgt 20    Stavanger
   2 Svendson  Tove      Borgvn 23    Sandnes  \
"""
    )

    assert (
        persons.order_by("LastName", True).table()
        == """\
P_ID LASTNAME  FIRSTNAME ADDRESS      CITY     
---- --------- --------- ------------ ---------
   2 Svendson  Tove      Borgvn 23    Sandnes  
   3 Pettersen Kari      Storgt 20    Stavanger
   4 Nilsen    Tom       Vingvn 23    Stavanger
   1 Hansen    Ola       Timoteivn 10 Sandnes  \
"""
    )


def test_insert(persons):
    persons.insert(5, "Nilsen", "Johan", "Bakken 2", "Stavanger")
    persons.insert(P_Id=6, LastName="Tjessem", FirstName="Jakob")

    assert (
        persons
        == """\
P_ID LASTNAME  FIRSTNAME ADDRESS      CITY     
---- --------- --------- ------------ ---------
   1 Hansen    Ola       Timoteivn 10 Sandnes  
   2 Svendson  Tove      Borgvn 23    Sandnes  
   3 Pettersen Kari      Storgt 20    Stavanger
   5 Nilsen    Johan     Bakken 2     Stavanger
   6 Tjessem   Jakob                           \
"""
    )


def test_update(persons):
    persons.insert(P_Id=6, LastName="Tjessem", FirstName="Jakob")

    persons.where((ROW.LastName == "Tjessem") & (ROW.FirstName == "Jakob")).update(
        Address="Nissestien 67", City="Sandnes"
    )
    assert (
        persons
        == """\
P_ID LASTNAME  FIRSTNAME ADDRESS       CITY     
---- --------- --------- ------------- ---------
   1 Hansen    Ola       Timoteivn 10  Sandnes  
   2 Svendson  Tove      Borgvn 23     Sandnes  
   3 Pettersen Kari      Storgt 20     Stavanger
   6 Tjessem   Jakob     Nissestien 67 Sandnes  \
"""
    )

    copy = persons.order_by("P_Id").table()
    copy.update(Address="Nissestien 67", City="Sandnes")

    assert (
        copy
        == """\
P_ID LASTNAME  FIRSTNAME ADDRESS       CITY   
---- --------- --------- ------------- -------
   1 Hansen    Ola       Nissestien 67 Sandnes
   2 Svendson  Tove      Nissestien 67 Sandnes
   3 Pettersen Kari      Nissestien 67 Sandnes
   6 Tjessem   Jakob     Nissestien 67 Sandnes\
"""
    )


def test_delete(persons):
    persons.insert(P_Id=6, LastName="Tjessem", FirstName="Jakob")
    copy = persons.order_by("P_Id").table()
    assert (
        copy.delete((ROW.LastName == "Tjessem") & (ROW.FirstName == "Jakob"))
        == """\
P_ID LASTNAME  FIRSTNAME ADDRESS      CITY     
---- --------- --------- ------------ ---------
   1 Hansen    Ola       Timoteivn 10 Sandnes  
   2 Svendson  Tove      Borgvn 23    Sandnes  
   3 Pettersen Kari      Storgt 20    Stavanger\
"""
    )

    assert (
        copy.truncate()
        == """\
P_ID LASTNAME FIRSTNAME ADDRESS CITY
---- -------- --------- ------- ----\
"""
    )


def test_top(persons):
    assert (
        Table.from_iter(persons.top(2))
        == """\
P_ID LASTNAME FIRSTNAME ADDRESS      CITY   
---- -------- --------- ------------ -------
   1 Hansen   Ola       Timoteivn 10 Sandnes
   2 Svendson Tove      Borgvn 23    Sandnes\
"""
    )

    assert (
        Table.from_iter(persons.top(0.3))
        == """\
P_ID LASTNAME FIRSTNAME ADDRESS      CITY   
---- -------- --------- ------------ -------
   1 Hansen   Ola       Timoteivn 10 Sandnes\
"""
    )


def test_like(persons):
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


def test_in(persons):
    persons.where(ROW.LastName.in_("Hansen", "Pettersen")).print()


def test_between(persons):
    persons.where(("Hansen" < ROW.LastName) < "Pettersen").print()
    persons.where(("Hansen" <= ROW.LastName) < "Pettersen").print()
    persons.where(("Hansen" <= ROW.LastName) <= "Pettersen").print()
    persons.where(("Hansen" < ROW.LastName) <= "Pettersen").print()
