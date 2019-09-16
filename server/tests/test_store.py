import pytest
from store import *

@pytest.fixture(scope="module", autouse=True)
def setup():
    """
    :return:
    """
    pass

def test_add_parking_lot():

    parking_store = Store()
    assert len(parking_store) == 0

    parking_store.add_lot("fronczak", 100)
    assert len(parking_store) == 1
    assert "fronczak" in parking_store

    parking_store.add_lot("hochstetter", 50)
    assert len(parking_store) == 2
    assert  "hochstetter" in parking_store

    parking_store.add_lot("hochstetter", 50)
    assert len(parking_store) == 2
    assert "hochstetter" in parking_store

def test_remove_parking_lot():

    parking_store = Store()

    parking_store.add_lot("fronczak", 100)
    parking_store.remove_lot("fronczak")
    assert len(parking_store) == 0
    assert "fronczak" not in parking_store

    parking_store.add_lot("hochstetter", 50)
    parking_store.remove_lot("hochstetter")
    assert len(parking_store) == 0
    assert "hochstetter" not in parking_store

    parking_store.add_lot("hochstetter", 50)
    parking_store.add_lot("fronczak", 100)
    parking_store.remove_lot("hochstetter")
    assert len(parking_store) == 1
    assert "hochstetter" not in parking_store
    parking_store.remove_lot("fronczak")
    assert len(parking_store) == 0
    assert "fronczak" not in parking_store

def test_add_spot():

    parking_store = Store()
    lot = "fronczak"
    capacity = 100
    parking_store.add_lot(lot, capacity)

    parking_store.increase_spots(lot)
    assert parking_store.get_spots(lot) == capacity

    parking_store.get_store()[lot].spots = capacity // 2
    parking_store.increase_spots(lot)
    assert parking_store.get_spots(lot) == (capacity // 2) + 1
    parking_store.increase_spots(lot)
    assert parking_store.get_spots(lot) == (capacity // 2) + 2

    parking_store.get_store()[lot].spots = 0
    parking_store.increase_spots(lot)
    assert parking_store.get_spots(lot) == 1

def test_remove_spot():

    parking_store = Store()
    lot = "fronczak"
    capacity = 100
    parking_store.add_lot(lot, capacity)

    parking_store.decrease_spots(lot)
    assert parking_store.get_spots(lot) == capacity - 1

    for i in range(capacity - 1, 0, -1):
        parking_store.decrease_spots(lot)
        assert parking_store.get_spots(lot) == i - 1

