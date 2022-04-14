import pytest

from table import Table


@pytest.fixture
def persons():
    persons = Table(
        ("P_Id", int),
        ("LastName", str),
        ("FirstName", str),
        ("Address", str),
        ("City", str),
    )

    persons.insert(1, "Hansen", "Ola", "Timoteivn 10", "Sandnes")
    persons.insert(2, "Svendson", "Tove", "Borgvn 23", "Sandnes")
    persons.insert(3, "Pettersen", "Kari", "Storgt 20", "Stavanger")

    return persons


@pytest.fixture
def orders():
    orders = Table(("O_Id", int), ("OrderNo", int), ("P_Id", int))
    
    orders.insert(1, 77895, 3)
    orders.insert(2, 44678, 3)
    orders.insert(3, 22456, 1)
    orders.insert(4, 24562, 1)
    orders.insert(5, 34764, 15)

    return orders
