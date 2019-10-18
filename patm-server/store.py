import copy
from json import JSONEncoder
from collections import UserDict
from datetime import datetime, timedelta
#from bisect import bisect, insort

class Store(UserDict):

    def __init__(self):
        #TODO: Initialize from a central store
        self.store = {"lots" : {}, "buildings": {}, "users": {}}
        self.bname_to_bid = {}
        self.current_id = 0
        self.building_id = 0


    def add_lot(self, lot, capacity):
        self.store['lots'][lot] = ParkingLot(self.current_id, lot, capacity)
        self.current_id += 1

    def add_building(self, building):
        self.store['buildings'][building['name']] = Building(self.building_id, building['name'], building['entrances_lat'], building['entrances_lon'], building['boundary_lat'], building['boundary_long'], self)
        self.building_id += 1

    def register_user(self, uid):
        if uid not in self.store['users']:
            self.store['users'][uid] = User(uid)

    def get_recommendation(self, uid):
        if uid in self.store['users']:
            return self.store['users'][uid].get_parking_recommendation()

    def remove_lot(self, lot):
        if lot in self.store['lots']:
            del self.store['lots'][lot]

    def increase_spots(self, lot):
        if lot in self.store['lots']:
            self.store['lots'][lot].increase_spots()

    def decrease_spots(self, lot):
        if lot in self.store['lots']:
            self.store['lots'][lot].decrease_spots()

    def get_capacity(self, lot):
        if lot in self.store['lots']:
            return self.store['lots'][lot].get_capacity()

    def get_spots(self, lot):
        if lot in self.store['lots']:
            return self.store['lots'][lot].get_spots()

    def set_boundary_lat(self, lot, coordinates):
        self.store['lots'][lot].set_boundary_lat(coordinates)

    def set_boundary_lon(self, lot, coordinates):
        self.store['lots'][lot].set_boundary_lon(coordinates)

    def set_available_times(self, lot, available_times):
        self.store['lots'][lot].set_available_times(available_times)

    def set_type(self, lot, type):
        self.store['lots'][lot].set_type(type)

    def set_center(self, lot):
        self.store['lots'][lot].set_center()

    def get_store(self):
        return self.store

    def get_bstore(self):
        return self.bname_to_bid

    def __repr__(self):
        return self.store.__str__()

    def __len__(self):
        return len(self.store['lots']) + len(self.store['buildings'])

    def __contains__(self, item):
        return item in self.store['lots'] or item in self.store['buildings']

class User:

    def __init__(self, id):
        self.id = id
        self.history = []

    def add_history(self, ts, bid):
        def insort(a, x, lo=0, hi=None):
            key = x[0]
            if lo < 0:
                raise ValueError('lo must be non-negative')
            if hi is None:
                hi = len(a)
            while lo < hi:
                mid = (lo + hi) // 2
                if a[mid][0] < key:
                    lo = mid + 1
                else:
                    hi = mid
            a.insert(lo, x)

        insort(self.history, (ts, bid))

    def get_history(self):
        return self.history

    def get_parking_recommendation(self):
        """
        Binary search on the timestamps and return a recommendation only if the timestamp is within 30 minutes
        :return:
        """
        # Credits: https://gist.github.com/ericremoreynolds/2d80300dabc70eebc790
        class KeyifyList(object):
            def __init__(self, inner, key):
                self.inner = inner
                self.key = key

            def __len__(self):
                return len(self.inner)

            def __getitem__(self, k):
                return self.key(self.inner[k])

        from bisect import bisect_left, bisect_right
        from datetime import datetime

        ls = KeyifyList(self.history, lambda x: x[0])
        left = bisect_left(ls, datetime.now() - timedelta(minutes=30))
        right = bisect_right(ls, datetime.now())

        return self.history[left][1]


class History:

    def __init__(self, ts, bid):
        """

        :param ts: Timestamp
        :param bid: Building ID
        """
        self.ts = ts
        self.bid = bid

class Building:

    def __init__(self, id, name, entrance_lat, entrance_lon, boundary_lat, boundary_lon, store):
        self.id = id
        self.name = name
        self.entrance_lat = entrance_lat
        self.entrance_lon = entrance_lon
        self.boundary_lat = boundary_lat
        self.boundary_lon = boundary_lon
        self.center = (sum(self.boundary_lat)/len(self.boundary_lat), \
                       sum(self.boundary_lon)/len(self.boundary_lon))
        self.closest_lot = self.compute_closest_lot(store.get_store())
        store.get_bstore()[id] = name
        store.get_bstore()[name] = id

    def compute_closest_lot(self, store):
        min_distance = float("inf")
        closest_lot = None
        for name, object in store["lots"].items():
            lot = object
            distance = ((lot.get_center()[0] - self.center[0])**2 + (lot.get_center()[1] - self.center[1])**2)**(0.5)
            if distance < min_distance:
                min_distance = distance
                closest_lot = lot

        return closest_lot

    def get_closest_lot(self):
        return self.closest_lot

class ParkingLot:

    def __init__(self, id, name, capacity):
        self.id = id
        self.name = name
        self.spots = capacity
        self.capacity = capacity
        self.boundary_lat = []
        self.boundary_lon = []
        self.available_times = []
        self.type = -1
        self.center = ()

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

    def set_boundary_lat(self, coordinates):
        self.boundary_lat = coordinates

    def set_boundary_lon(self, coordinates):
        self.boundary_lon = coordinates

    def set_available_times(self, available_times):
        self.available_times = available_times

    def set_type(self, type):
        self.type = type

    def set_center(self):
        self.center =  (sum(self.boundary_lat)/len(self.boundary_lat), \
                       sum(self.boundary_lon)/len(self.boundary_lon))

    def get_center(self):
        return self.center

    def __repr__(self):
        return "Lot(ID: {}, Name: {}, Spots: {}, Capacity: {})".format(self.id, self.name, self.spots, self.capacity)


class StoreEncoder(JSONEncoder):

    def default(self, o):
        return o.__dict__