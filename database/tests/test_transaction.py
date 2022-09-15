import _thread

from engine import TransactionalDatabase
from table import Table


def test_transactional_database():
    # Create a test database, tables, and dummy data.
    t_db = TransactionalDatabase()
    t_db.create("test", Table(("id", int), ("name", str)))
    t_db.test.insert(100, "Adam")
    t_db.test.print()
    # Test the rollback transaction support added in Database2.
    test = t_db.begin_transaction("test")
    test.insert(101, "Eve")
    assert len(test) == 2
    t_db.rollback_transaction("test")
    assert len(t_db.test) == 1

    # Test the commit transaction support added in Database2.
    test = t_db.begin_transaction("test")
    test.insert(102, "Seth")
    assert len(test) == 2
    t_db.commit_transaction("test")
    assert len(t_db.test) == 2
    assert t_db.test == test

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
        nw2 = TransactionalDatabase.load("northwind2.db")
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
