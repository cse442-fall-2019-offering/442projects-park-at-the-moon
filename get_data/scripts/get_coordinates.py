import overpy
import csv
import xml.etree.ElementTree as ET
import json
import sys
import os
import shutil
import glob

def read_csv_lot_building():

    lot_names = []
    lot_types = []
    building_names = []

    with open('../data/lot_building_names.csv') as csvfile:

        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            if row[0]:
                lot_names.append(row[0].strip())
            if row[1]:
                lot_types.append(row[1].strip())
            if row[2]:
                building_names.append(row[2].strip())

    return list(zip(lot_names, lot_types)), building_names

def read_csv_lot():

    lot_names = []
    lot_types = []

    with open('../data/lot_names.csv') as csvfile:

        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            if row[0]:
                lot_names.append(row[0].strip())
            if row[1]:
                lot_types.append(row[1].strip())

    return list(zip(lot_names, lot_types))

def read_csv_building():

    building_names = []

    with open('../data/building_names.csv') as csvfile:

        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            if row[0]:
                building_names.append(row[0].strip())

    return building_names

def get_lot_ids(lot_names):
    lot_ids = []

    tree = ET.parse('../data/north_campus.osm')
    root = tree.getroot()
    inc = 0
    for way in root.findall('way'):
        for tag in way.findall('tag'):
            if tag.attrib['k'] == 'name':
                for name, t in lot_names:
                    if name in tag.attrib['v'] and 'Lot' in tag.attrib['v']:
                        lot_ids.append((name, t, way.get('id')))
                        break
                inc += 1
    return lot_ids

def get_building_ids(building_names):
    building_ids = []

    tree = ET.parse('../data/north_campus.osm')
    root = tree.getroot()
    
    for way in root.findall('way'):
        for tag in way.findall('tag'):
            if tag.attrib['k'] == 'name':
                for name in building_names:
                    if name in tag.attrib['v']:
                        building_ids.append((name, way.get('id')))
                        break
    return building_ids

def get_entrance_coords():
    entrance_coords = {}
    
    tree = ET.parse('../data/north_campus.osm')
    root = tree.getroot()
    nodes = root.findall('node')

    for n in nodes:
        tags = n.findall('tag')
        if len(tags) > 1:
            if tags[0].get('k') == 'entrance':
                buildings = tags[1].get('v').split(',')
                for building in buildings:
                    if tags[1].get('v') in entrance_coords.keys():
                        entrance_coords[building]['lat'].append(n.get('lat'))
                        entrance_coords[building]['lon'].append(n.get('lon'))
                    else:
                        coords = {'lat': [n.get('lat')], 'lon': [n.get('lon')]}
                        entrance_coords[building] = coords

    return entrance_coords

def get_lot_coords(lot_ids):
    lot_coords = []
    api = overpy.Overpass()

    for lot, types, id in lot_ids:
        result = api.query('''way('''+ id + ''');out geom;''')
        node = result.ways[0].get_nodes(True)
        lat = []
        lon = []
        for n in node:
            lat.append(float(n.lat))
            lon.append(float(n.lon))
        print(lot + " Lot done")
        lot_coords.append({"name": lot, "type": types, "boundary_lat": lat, "boundary_long": lon, "capacity": 0, "available_spots": 0, "available_times":["0:00"]})
        # troubleshooting (remove break when done)
#       break
    return lot_coords

def get_building_coords(building_ids, entrance_coords):
    building_coords = []
    api = overpy.Overpass()

    for building, id in building_ids:
        result = api.query('''way('''+ id + ''');out geom;''')
        node = result.ways[0].get_nodes(True)
        lat = []
        lon = []
        for n in node:
            lat.append(float(n.lat))
            lon.append(float(n.lon))
        print(building + " done")
        entr_lat = [0.0]
        entr_lon = [0.0]
        if building in entrance_coords.keys():
            entr_lat = entrance_coords[building]['lat']
            entr_lon = entrance_coords[building]['lon']
        building_coords.append({"name": building, "entrances_lat": entr_lat, "entrances_lon": entr_lon, "boundary_lat": lat, "boundary_long": lon})
        # troubleshooting (remove break when done)
#       break

    return building_coords

# pass in just the file name
def mv_old_data(f):
    # avoid rewriting over old data
    filename = f.split('.')[0]
    filetype = f.split('.')[1]
    if os.path.exists('../data/' + f):
        filenames = glob.glob('../data/old_data/' + filename + '*')
        max_version = 0
        if not filenames == []: 
            version = 0
            for fi in filenames:
                try:
                    version = int(''.join(filter(str.isdigit, fi)))
                    if version > max_version:
                        max_version = version
                except:
                    continue
        fname = filename + 'v' + str(max_version+1) + '.csv' 
        os.rename('../data/' + f, '../data/' + fname)
        shutil.move("../data/" + fname, "../data/old_data/" + fname)

def write_2_json_lot_building(lot_data, building_data):

    mv_old_data('lot_building_data.json')

    data = {"lots": lot_data, "buildings": building_data}
    with open('../data/lot_building_data.json', 'w') as f:
        json.dump(data, f, indent=2)

def write_2_json_lot(lot_data):

    mv_old_data('lot_data.json')

    data = {"lots": lot_data}
    with open('../data/lot_data.json', 'w') as f:
        json.dump(data, f, indent=2)

def write_2_json_building(building_data):

    mv_old_data('building_data.json')

    data = {"buildings": building_data}
    with open('../data/building_data.json', 'w') as f:
        json.dump(data, f, indent=2)

if len(sys.argv) == 1:                                                                                                                                                      
    print ('Invocation:')
    print ('\tpython get_coordinates.py [ -lot_coords | -building_coords | -both ]')
    exit()
else:
    if sys.argv[1] == '-lot_coords':
        lot_names = read_csv_lot()
        lot_ids = get_lot_ids(lot_names)
        lot_coords = get_lot_coords(lot_ids)
        write_2_json_lot(lot_coords)
    elif sys.argv[1] == '-building_coords':
        building_names = read_csv_building()
        building_ids = get_building_ids(building_names)
        entrance_coords = get_entrance_coords()
        building_coords = get_building_coords(building_ids, entrance_coords)
        write_2_json_building(building_coords)
    elif sys.argv[1] == '-both':
        lot_names, building_names = read_csv_lot_building()
        lot_ids = get_lot_ids(lot_names)
        building_ids = get_building_ids(building_names)
        lot_coords = get_lot_coords(lot_ids)
        entrance_coords = get_entrance_coords()
        building_coords = get_building_coords(building_ids, entrance_coords)
        write_2_json_lot_building(lot_coords, building_coords)
    else:
        print ('Invocation:')
        print ('\tpython get_coordinates.py [ -lot_coords | -building_coords | -both ]')
        exit()
    
# initial test to get Ketter Lot coordinates

#api = overpy.Overpass()
#result = api.query('''way(640336082);out geom;''')
#w = result.ways[0].get_nodes(True)

#for node in w:
#   print(float(node.lat))
#   print(float(node.lon))

