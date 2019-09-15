from json import JSONEncoder


class Store:

    def __init__(self):
        #TODO: Initialize from a central store
        self.store = {"hochstetter": 190}
        self.current_id = 0

    def add_lot(self, name, capacity):
        self.store[name] = ParkingLot(self.current_id, name, capacity)
        self.current_id += 1

    def remove_lot(self, name):
        del self.store[name]

    def __repr__(self):
        return self.store.__str__()


class ParkingLot:

    def __init__(self, id, name, capacity):
        self.id = id
        self.name = name
        self.slots = capacity
        self.capacity = capacity

    def increase_slots(self):
        self.slots += 1

    def decrease_slots(self):
        self.slots -= 1

    def __repr__(self):
        return "Lot(ID: {}, Name: {}, Slots: {}, Capacity: {})".format(self.id, self.name, self.slots, self.capacity)


class StoreEncoder(JSONEncoder):

    def default(self, o):
        return o.__dict__
