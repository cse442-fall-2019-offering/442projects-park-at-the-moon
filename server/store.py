from json import JSONEncoder
from collections import UserDict


class Store(UserDict):

    def __init__(self):
        #TODO: Initialize from a central store
        self.store = {}
        self.current_id = 0

    def add_lot(self, lot, capacity):
        self.store[lot] = ParkingLot(self.current_id, lot, capacity)
        self.current_id += 1

    def remove_lot(self, lot):
        if lot in self.store:
            del self.store[lot]

    def increase_spots(self, lot):
        if lot in self.store:
            self.store[lot].increase_spots()

    def decrease_spots(self, lot):
        if lot in self.store:
            self.store[lot].decrease_spots()

    def get_capacity(self, lot):
        if lot in self.store:
            return self.store[lot].get_capacity()

    def get_spots(self, lot):
        if lot in self.store:
            return self.store[lot].get_spots()

    def get_store(self):
        return self.store

    def __repr__(self):
        return self.store.__str__()

    def __len__(self):
        return len(self.store)

    def __contains__(self, item):
        return item in self.store


class ParkingLot:

    def __init__(self, id, name, capacity):
        self.id = id
        self.name = name
        self.spots = capacity
        self.capacity = capacity

    def increase_spots(self):
        self.spots = min(self.capacity, self.spots + 1)

    def decrease_spots(self):
        self.spots = max(0, self.spots - 1)

    def get_spots(self):
        return self.spots

    def get_capacity(self):
        return self.capacity

    def reset(self):
        self.spots = self.capacity

    def __repr__(self):
        return "Lot(ID: {}, Name: {}, Spots: {}, Capacity: {})".format(self.id, self.name, self.spots, self.capacity)


class StoreEncoder(JSONEncoder):

    def default(self, o):
        return o.__dict__