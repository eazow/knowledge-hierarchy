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


def test_inner_join(persons, orders):
    # Test inner join with alias.
    inner_join(ROW.p.P_Id == ROW.po.P_Id, p=persons, po=orders).select(
        "po.OrderNo", "p.LastName", "p.FirstName"
    ).where((ROW.p.LastName == "Hansen") & (ROW.p.FirstName == "Ola")).print()


def test_left_join(persons, orders):
    left_join(
        (persons, "Persons"), (orders, "Orders"), ROW.Persons.P_Id == ROW.Orders.P_Id
    ).select("Persons.LastName", "Persons.FirstName", "Orders.OrderNo").order_by(
        "Persons.LastName"
    ).table().print()
    left_join((persons, "p"), (orders, "o"), ROW.p.P_Id == ROW.o.P_Id).select(
        "p.LastName", "p.FirstName", "o.OrderNo"
    ).order_by("p.LastName").table().print()


def test_right_join(persons, orders):
    right_join(
        (persons, "Persons"), (orders, "Orders"), ROW.Persons.P_Id == ROW.Orders.P_Id
    ).select("Persons.LastName", "Persons.FirstName", "Orders.OrderNo").order_by(
        "Persons.LastName"
    ).table().print()
    right_join((persons, "p"), (orders, "o"), ROW.p.P_Id == ROW.o.P_Id).select(
        "p.LastName", "p.FirstName", "o.OrderNo"
    ).order_by("p.LastName").table().print()


def test_full_join(persons, orders):
    full_join(
        ROW.Persons.P_Id == ROW.Orders.P_Id, Persons=persons, Orders=orders
    ).order_by("Persons.LastName").table().print()
    full_join(ROW.p.P_Id == ROW.o.P_Id, p=persons, o=orders).select(
        "p.LastName", "p.FirstName", "o.OrderNo"
    ).order_by("p.LastName").table().print()
