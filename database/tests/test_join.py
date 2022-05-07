from row import ROW
from table import inner_join, left_join, right_join, full_join


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

    assert (
        inner_join(ROW.p.P_Id == ROW.po.P_Id, p=persons, po=orders)
        .select("po.OrderNo", "p.LastName", "p.FirstName")
        .where((ROW.p.LastName == "Hansen") & (ROW.p.FirstName == "Ola"))
        == """\
P.LASTNAME P.FIRSTNAME PO.ORDERNO
---------- ----------- ----------
Hansen     Ola              22456
Hansen     Ola              24562\
"""
    )


def test_left_join(persons, orders):
    assert (
        left_join(
            (persons, "Persons"),
            (orders, "Orders"),
            ROW.Persons.P_Id == ROW.Orders.P_Id,
        )
        .select("Persons.LastName", "Persons.FirstName", "Orders.OrderNo")
        .order_by("Persons.LastName")
        .table()
        == """\
PERSONS.LASTNAME PERSONS.FIRSTNAME ORDERS.ORDERNO
---------------- ----------------- --------------
Hansen           Ola                        22456
Hansen           Ola                        24562
Pettersen        Kari                       77895
Pettersen        Kari                       44678
Svendson         Tove                           0\
"""
    )
    assert (
        left_join((persons, "p"), (orders, "o"), ROW.p.P_Id == ROW.o.P_Id)
        .select("p.LastName", "p.FirstName", "o.OrderNo")
        .order_by("p.LastName")
        .table()
        == """\
P.LASTNAME P.FIRSTNAME O.ORDERNO
---------- ----------- ---------
Hansen     Ola             22456
Hansen     Ola             24562
Pettersen  Kari            77895
Pettersen  Kari            44678
Svendson   Tove                0\
"""
    )


def test_right_join(persons, orders):
    assert right_join(
        (persons, "Persons"), (orders, "Orders"), ROW.Persons.P_Id == ROW.Orders.P_Id
    ).select("Persons.LastName", "Persons.FirstName", "Orders.OrderNo").order_by(
        "Persons.LastName"
    ).table() == """\
ORDERS.ORDERNO PERSONS.LASTNAME PERSONS.FIRSTNAME
-------------- ---------------- -----------------
         34764                                   
         22456 Hansen           Ola              
         24562 Hansen           Ola              
         77895 Pettersen        Kari             
         44678 Pettersen        Kari             \
"""
    assert len(right_join((persons, "p"), (orders, "o"), ROW.p.P_Id == ROW.o.P_Id).select(
        "p.LastName", "p.FirstName", "o.OrderNo"
    ).order_by("p.LastName").table()) == 5


def test_full_join(persons, orders):
    assert full_join(
        ROW.Persons.P_Id == ROW.Orders.P_Id, Persons=persons, Orders=orders
    ).order_by("Persons.LastName").table() == """\
PERSONS.P_ID PERSONS.LASTNAME PERSONS.FIRSTNAME PERSONS.ADDRESS PERSONS.CITY ORDERS.O_ID ORDERS.ORDERNO ORDERS.P_ID
------------ ---------------- ----------------- --------------- ------------ ----------- -------------- -----------
           0                                                                           5          34764          15
           1 Hansen           Ola               Timoteivn 10    Sandnes                3          22456           1
           1 Hansen           Ola               Timoteivn 10    Sandnes                4          24562           1
           3 Pettersen        Kari              Storgt 20       Stavanger              1          77895           3
           3 Pettersen        Kari              Storgt 20       Stavanger              2          44678           3
           2 Svendson         Tove              Borgvn 23       Sandnes                0              0           0\
"""

    assert len(full_join(ROW.p.P_Id == ROW.o.P_Id, p=persons, o=orders).select(
        "p.LastName", "p.FirstName", "o.OrderNo"
    ).order_by("p.LastName").table()) == 6
