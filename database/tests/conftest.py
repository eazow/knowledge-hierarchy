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
    # Populate the table with rows.
    persons.insert(1, "Hansen", "Ola", "Timoteivn 10", "Sandnes")
    persons.insert(2, "Svendson", "Tove", "Borgvn 23", "Sandnes")
    persons.insert(3, "Pettersen", "Kari", "Storgt 20", "Stavanger")

    return persons
