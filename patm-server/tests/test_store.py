import pytest
from store import *
from unittest import TestCase


@pytest.fixture(scope="module", autouse=True)
def setup():
    """
    :return:
    """

    parking_store = Store()

    lot1 = "fronczak"
    lot2 = "hochstetter"


    capacity1 = 100
    capacity2 = 190

    parking_store.add_lot(lot1, capacity1)
    parking_store.add_lot(lot2, capacity2)

    return parking_store

def test_add_building():

    parking_store = Store()
    building1 = {"name": "student union", "entrance_lat": None, "entrance_lon": None, "boundary_lat": [1], "boundary_long": [1]}
    parking_store.add_building(building1)
    assert "student union" in parking_store
    assert len(parking_store) == 1

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
    lot1 = "fronczak"
    capacity1 = 100
    lot2 = "hochstetter"
    capacity2 = 50


    parking_store.add_lot(lot1, capacity1)
    parking_store.remove_lot(lot1)
    assert len(parking_store) == 0
    assert lot1 not in parking_store

    parking_store.add_lot(lot2, capacity2)
    parking_store.remove_lot(lot2)
    assert len(parking_store) == 0
    assert lot2 not in parking_store

    parking_store.add_lot(lot2, capacity2)
    parking_store.add_lot(lot1, capacity1)
    parking_store.remove_lot(lot2)
    assert len(parking_store) == 1
    assert lot2 not in parking_store
    parking_store.remove_lot(lot1)
    assert len(parking_store) == 0
    assert lot1 not in parking_store


def test_get_spots(setup):

    parking_store = setup
    lot = "hochstetter"
    assert parking_store.get_spots(lot) == 190
    assert parking_store.get_spots(lot) == parking_store.get_capacity(lot)


def test_add_spot(setup):

    parking_store = setup

    lot = "hochstetter"
    capacity = parking_store.get_capacity(lot)

    assert parking_store.get_spots(lot) == capacity
    parking_store.increase_spots(lot)

    # Increasing spots beyond capacity should not cause overflow
    assert parking_store.get_spots(lot) == capacity

    parking_store.get_store()['lots'][lot].spots = capacity // 2
    parking_store.increase_spots(lot)
    assert parking_store.get_spots(lot) == (capacity // 2) + 1

    parking_store.increase_spots(lot)
    assert parking_store.get_spots(lot) == (capacity // 2) + 2

    parking_store.get_store()['lots'][lot].spots = 0
    parking_store.increase_spots(lot)
    assert parking_store.get_spots(lot) == 1


def test_remove_spot(setup):

    parking_store = setup
    lot = "fronczak"
    capacity = parking_store.get_capacity(lot)

    parking_store.decrease_spots(lot)
    assert parking_store.get_spots(lot) == capacity - 1

    for i in range(capacity - 1, 0, -1):
        parking_store.decrease_spots(lot)
        assert parking_store.get_spots(lot) == i - 1

    parking_store.decrease_spots(lot)
    assert parking_store.get_spots(lot) == 0

def test_lot_not_present(setup):

    parking_store = setup
    lot = "abcdefghijklmnopqrstuvwxyz"

    try:
        parking_store.increase_spots(lot)
        parking_store.decrease_spots(lot)
        parking_store.get_capacity(lot)
        parking_store.get_spots(lot)
        parking_store.remove_lot(lot)

    except:
        TestCase.fail()