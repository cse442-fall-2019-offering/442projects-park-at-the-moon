import pytest
from unittest import TestCase
from datetime import datetime, timedelta
from store import *


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

def test_add_history():


    parking_store = Store()
    parking_store.register_user(0)
    parking_store.register_user(1)

    time = datetime.now()
    users = parking_store.get_store()['users']
    users[0].add_history(time, 1)
    users[1].add_history(time, 2)

    assert (time, 1) in users[0].get_history()
    assert (time, 1) not in users[1].get_history()
    assert (time, 2) in users[1].get_history()
    assert (time, 2) not in users[0].get_history()

    new_time = datetime.now() + timedelta(hours=4)
    users[0].add_history(new_time, 2)
    users[1].add_history(new_time, 2)

    assert (time, 1) in users[0].get_history()
    assert (time, 2) in users[1].get_history()
    assert (new_time, 2) in users[0].get_history()
    assert (new_time, 2) in users[1].get_history()

    newest_time = datetime.now() + timedelta(hours=-4)
    users[0].add_history(newest_time, 2)

    users[1].add_history(newest_time, 2)

    assert (time, 1) in users[0].get_history()
    assert (newest_time, 2) in users[1].get_history()
    assert (new_time, 2) in users[0].get_history()
    assert (newest_time, 2) in users[0].get_history()

    assert users[0].get_history().index((time, 1)) < users[0].get_history().index((new_time, 2))
    assert users[0].get_history().index((time, 1)) > users[0].get_history().index((newest_time, 2))

    assert users[1].get_history().index((time, 2)) < users[0].get_history().index((new_time, 2))
    assert users[1].get_history().index((time, 2)) > users[0].get_history().index((newest_time, 2))


def test_add_history_next_day():

    parking_store = Store()
    parking_store.register_user(1)

    users = parking_store.get_store()['users']

    time = datetime.now()
    users[1].add_history(time, 2)
    next_day = datetime.now() + timedelta(days=1)
    users[1].add_history(next_day, 1)

    assert users[1].get_history().index((time, 2)) < users[1].get_history().index((next_day, 1))

def test_add_history_next_week():

    parking_store = Store()
    parking_store.register_user(1)

    users = parking_store.get_store()['users']

    time = datetime.now()
    users[1].add_history(time, 2)
    next_week = datetime.now() + timedelta(weeks=1, hours=-1)
    users[1].add_history(next_week, 1)

    assert users[1].get_history().index((time, 2)) > users[1].get_history().index((next_week, 1))

def test_suggestion():

    parking_store = Store()
    parking_store.register_user(0)

    time = datetime.now()
    users = parking_store.get_store()['users']
    users[0].add_history(time, 1)
    new_time = datetime.now() + timedelta(hours=4)
    users[0].add_history(new_time, 2)

    newest_time = datetime.now() + timedelta(hours=-4)
    users[0].add_history(newest_time, 2)
    store = parking_store
    assert store.get_recommendation(0) == 1
    time = datetime.now() + timedelta(hours = 4)
    assert store.get_recommendation(0, time) == 2
    time = datetime.now() + timedelta(hours=-4)
    assert store.get_recommendation(0, time) == 2


def test_add_building():

    parking_store = Store()
    building1 = {"name": "student union", "entrances_lat": None, "entrances_lon": None, "boundary_lat": [1], "boundary_long": [1]}
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


def test_closest_lot():
    parking_store = Store()

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
