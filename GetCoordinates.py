import overpy
import csv
import xml.etree.ElementTree as ET
import json

def readCSV():

	lot_names = []
	lot_types = []
	building_names = []

	with open('LotBuildingNames.csv') as csvfile:

		readCSV = csv.reader(csvfile, delimiter=',')
		for row in readCSV:
			if row[0]:
				lot_names.append(row[0].strip())
			if row[1]:
				lot_types.append(row[1].strip())
			if row[2]:
				building_names.append(row[2].strip())

	return list(zip(lot_names, lot_types)), building_names

def getLotIDs(lot_names):
	lot_ids = []

	tree = ET.parse('NorthCampus.osm')
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

def getBuildingIDs(building_names):
	building_ids = []

	tree = ET.parse('NorthCampus.osm')
	root = tree.getroot()
	
	for way in root.findall('way'):
		for tag in way.findall('tag'):
			if tag.attrib['k'] == 'name':
				for name in building_names:
					if name in tag.attrib['v']:
						building_ids.append((name, way.get('id')))
						break
	return building_ids

def getLotCoords(lot_ids):
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
#		break
	return lot_coords

def getBuildingCoords(building_ids):
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
		building_coords.append({"name": building, "entrance_lat": [0.0], "entrance_lon": [0.0], "boundary_lat": lat, "boundary_long": lon})
		# troubleshooting (remove break when done)
#		break

	return building_coords

def write2Json(lot_data, building_data):
	data = {"lots": lot_data, "buildings": building_data}
#	print(data)
#	json.dumps(data, indent=4)
	with open('LotData.json', 'w') as f:
		json.dump(data, f, indent=2)

lot_names, building_names = readCSV()

lot_ids = getLotIDs(lot_names)

building_ids = getBuildingIDs(building_names)

lot_coords = getLotCoords(lot_ids)

building_coords = getBuildingCoords(building_ids)

write2Json(lot_coords, building_coords)

# initial test to get Ketter Lot coordinates

#api = overpy.Overpass()
#result = api.query('''way(640336082);out geom;''')
#w = result.ways[0].get_nodes(True)

#for node in w:
#	print(float(node.lat))
#	print(float(node.lon))

