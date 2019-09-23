from geopy.geocoders import Nominatim
from geopy.geocoders import GoogleV3
import geopy.distance
import json
import sys
from os import path
 
def compare_lots(lot_names, osm_dict):
    '''
    checks to make sure all lots are
    being read from osm to the json file
    '''
    print('\n****************************************************')
    print('********** Begin Test: Checking Lot Names **********\n')
    found = set()
    print('Found\t\t\tMissing\n')

    for lot in osm_dict['lots']:
        if lot['name'] in lot_names:
            print(lot['name'])
            found.add(lot['name'])
        else:
            print('\t\t\t' + lot['name']) 

    if len(lot_names.difference(found)) == 0:
        print('All lots accounted for\n')
    else:
        print('\nIncluded in txt file but not osm file (update openstreetmap.org):')
        print('\n'.join(lot_names.difference(found)))
    print('\n*********** End Test: Checking Lot Names ***********')
    print('****************************************************\n')

def compare_buildings(building_names, osm_dict):
    '''
    checks to make sure all buildings
    are being read from osm to the json file
    '''
    found = set()
    print('\n****************************************************')
    print('******** Begin Test: Checking Building Names *******\n')
    print('Found\t\t\tMissing\n')

    for building in osm_dict['buildings']:
        if building['name'] in building_names:
            print(building['name'])
            found.add(building['name'])
        else:
            print('\t\t\t' + building['name']) 

    if len(building_names.difference(found)) == 0:
        print('All buildings accounted for\n')
    else:
        print('\nIncluded in txt file but not osm file (update openstreetmap.org):')
        print('\n'.join(building_names.difference(found)))
    print('\n****************************************************')
    print('********* End Test: Checking Building Names ********\n')

def check_perim_lot_coord(osm_data, geolocator, google_key):
    '''
    checks to make sure all perimeter
    coordinates are within half a mile of
    center of parking lot
    '''
    print('\n*****************************************************')
    print('******* Begin Test: Perimeter Lot Coordinates *******\n')
    google_geolocator = None
    if google_key != "":
        try:
            google_geolocator = GoogleV3(api_key = google_key)
        except Exception:
            print("google api key incorrect - may not find lot")
    # max distance between coordinates (in miles)
    max_dist = .5
    print('maximum difference between center point and perimeter is ' + str(max_dist) + ' miles')
    print('Accurate\t\t\tInaccurate\t\t\tMissing')
    for lot in osm_data['lots']:
        location = geolocator.geocode(lot['name'] + ' Lot, University at Buffalo')
        if location == None:
            location = geolocator.geocode(lot['name'] + ' Lot')
        if location == None or not ('Buffalo' in location.address \
            or 'Amherst' in location.address) or 'South Campus' in location.address:
            if google_geolocator != None:
                try:
                    location = google_geolocator.geocode(lot['name'] + ' Lot, University at Buffalo')
                except Exception:
                    print("NOTE: google api key did not work")
                    print(str(len('Accurate') * ' ') + '\t\t\t' + str(len('Inaccurate') * ' ') + '\t\t\t' + lot['name'])
                    continue
        if location == None:
            print(str(len('Accurate') * ' ') + '\t\t\t' + str(len('Inaccurate') * ' ') + '\t\t\t' + lot['name'])
            continue

        correct = True
        for lat, lon in zip(lot['boundary_lat'], lot['boundary_long']):
            diff = geopy.distance.geodesic((lat, lon), (location.latitude, location.longitude)).miles
            if diff > max_dist:
                try:
                    location = google_geolocator.geocode(lot['name'] + ' Lot, University at Buffalo')
                except Exception:
                    correct = False
                    break

                diff = geopy.distance.geodesic((lat, lon), (location.latitude, location.longitude)).miles
                if diff > max_dist:
                    correct = False
                    break
        if correct:
            print(lot['name'])
        else:
            print(str(len('Accurate') * ' ') + '\t\t\t' + lot['name'])

    print('\n*****************************************************')
    print('******** End Test: Perimeter Lot Coordinates ********\n')

def check_perim_building_coord(osm_data, geolocator, google_key):
    '''
    checks to make sure all perimeter
    coordinates are within half a mile of
    center of buildings
    '''
    print('\n************************************************************')
    print('******** Begin Test: Perimeter Building Coordinates ********\n')
    google_geolocator = None
    if google_key != "":
        try:
            google_geolocator = GoogleV3(api_key = google_key)
        except Exception:
            print("google api key incorrect - may not find building")
    # max distance between coordinates (in miles)
    max_dist = .5
    print('maximum difference between center point and perimeter is ' + str(max_dist) + ' miles')
    print('Accurate\t\t\tInaccurate\t\t\tMissing')
    for building in osm_data['buildings']:
        location = geolocator.geocode(building['name'] + ', University at Buffalo')
        if location == None:
            location = geolocator.geocode(building['name'])
        if location == None or not ('Buffalo' in location.address \
            or 'Amherst' in location.address) or 'South Campus' in location.address:
            if google_geolocator != None:
                try:
                    location = google_geolocator.geocode(building['name'] + ', University at Buffalo')
                except Exception:
                    print("NOTE: google api did not work")
                    print(str(len('Accurate') * ' ') + '\t\t\t' + str(len('Inaccurate') * ' ') + '\t\t\t' + building['name'])
                    continue
        if location == None:
            print(str(len('Accurate') * ' ') + '\t\t\t' + str(len('Inaccurate') * ' ') + '\t\t\t' + building['name'])
            continue

        correct = True
        for lat, lon in zip(building['boundary_lat'], building['boundary_long']):
            diff = geopy.distance.geodesic((lat, lon), (location.latitude, location.longitude)).miles
            if diff > max_dist:
                try:
                    location = google_geolocator.geocode(building['name'] + ', University at Buffalo')
                except Exception:
                    correct = False
                    break

                diff = geopy.distance.geodesic((lat, lon), (location.latitude, location.longitude)).miles
                if diff > max_dist:
                    correct = False
                    break
        if correct:
            print(building['name'])
        else:
            print(str(len('Accurate') * ' ') + '\t\t\t' + building['name'])

    print('\n**********************************************************')
    print('******** End Test: Perimeter Building Coordinates ********\n')
    
if len(sys.argv) == 1:
    print ('Invocation:')
    print ('\tpython osm_tests.py [ -lot_names | -building_names | -lot_coords | -building_coords | -all ]...')
    print ('\tstore optional google maps api key in tests/google_api_key.txt')
    exit()
else:
    google_key = ""
    if path.exists("google_api_key.txt"):
        with open('google_api_key.txt', 'r') as f:
            google_key = (f.readline()).strip()
    else:
        print("\n******* May not account for all lots/buildings due to non-Google API's lack of accuracy *******\n")

    geolocator = Nominatim(user_agent="Park at the Moon")
    osm_dict = None
    if (not path.exists('test_data/parking_lots.txt')):
        print("missing test_data/parking_lots.txt")
        exit()
    if (not path.exists('test_data/buildings.txt')):
        print("missing test_data/buildings.txt")
        exit()

    for arg in sys.argv[1:]:
        if arg == '-lot_names':
            if path.exists('../data/lot_data.json'):
                with open('../data/lot_data.json') as f:
                    osm_dict = json.load(f)
            elif path.exists('../data/lot_building_data.json'):
                with open('../data/lot_building_data.json') as f:
                    osm_dict = json.load(f)
            else:
                print('missing json lot data')
                exit()
            lot_names = set(line.strip() for line in open('test_data/parking_lots.txt'))
            compare_lots(lot_names, osm_dict)

        elif arg == '-building_names':
            if path.exists('../data/building_data.json'):
                with open('../data/building_data.json') as f:
                    osm_dict = json.load(f)
            elif path.exists('../data/lot_building_data.json'):
                with open('../data/lot_building_data.json') as f:
                    osm_dict = json.load(f)
            else:
                print('missing json building data')
                exit()
            building_names = set(line.strip() for line in open('test_data/buildings.txt'))
            compare_buildings(building_names, osm_dict)

        elif sys.argv[1] == '-lot_coords':
            if path.exists('../data/lot_data.json'):
                with open('../data/lot_data.json') as f:
                    osm_dict = json.load(f)
            elif path.exists('../data/lot_building_data.json'):
                with open('../data/lot_building_data.json') as f:
                    osm_dict = json.load(f)
            else:
                print('missing json lot data')
                exit()
            check_perim_lot_coord(osm_dict, geolocator, google_key)

        elif sys.argv[1] == '-building_coords': 
            if path.exists('../data/building_data.json'):
                with open('../data/building_data.json') as f:
                    osm_dict = json.load(f)
            elif path.exists('../data/lot_building_data.json'):
                with open('../data/lot_building_data.json') as f:
                    osm_dict = json.load(f)
            else:
                print('missing json building data')
                exit()
            check_perim_building_coord(osm_dict, geolocator, google_key)

        elif sys.argv[1] == '-all': 
            if path.exists('../data/lot_building_data.json'):
                with open('../data/lot_building_data.json') as f:
                    osm_dict = json.load(f)
            else:
                print('missing json building data')
                exit()
            lot_names = set(line.strip() for line in open('test_data/parking_lots.txt'))
            compare_lots(lot_names, osm_dict)
            building_names = set(line.strip() for line in open('test_data/buildings.txt'))
            compare_buildings(building_names, osm_dict)
            check_perim_lot_coord(osm_dict, geolocator, google_key)
            check_perim_building_coord(osm_dict, geolocator, google_key)
        else:
            print ('Invocation:')
            print ('\tpython osm_tests.py [ -lot_names | -building_names | -lot_coords | -building_coords | -all ]...')
            print ('\tstore optional google maps api key in tests/google_api_key.txt')
            exit()

