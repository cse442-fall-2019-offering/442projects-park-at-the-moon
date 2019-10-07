import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest
import sys
import json

def get_lot_names():

    lot_names = []
    types = []

    url = 'http://www.buffalo.edu/parking/parking-places.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    for row in soup.findAll('tr')[1:]:

        if (len(row.findAll('p')) == 0):
            break

        tempType = 0
        # 0 for student, 1 for faculty/staff, 2 for both
        if 'X' in row.findAll('p')[1].get_text() and 'X' in row.findAll('p')[2].get_text():
            tempType = 2
        elif 'X' in row.findAll('p')[1].get_text():
            tempType = 1

        lot_str = row.findAll('p')[0].get_text().split('(')[0]
        lot_name = ""

        # weird fix for now
        if ' & ' in lot_str and ',' in lot_str:
            lot_name = ''.join(lot_str.split(',')[0][0:-1])
#           print(lot_name)
            lot_names.append(lot_name + lot_str.split(',')[0][-1])
            types.append(tempType)
            lot_names.append(lot_name + lot_str.split(',')[1].split()[0])
            types.append(tempType)
            lot_names.append(lot_name + lot_str.split(' & ')[1])
            types.append(tempType)
            
        elif ' & ' in lot_str:
            lot_name = ''.join(lot_str.split(' & ')[0][0:-1])
            lot_names.append(lot_name + lot_str.split(' & ')[0][-1])
            types.append(tempType)
            lot_names.append(lot_name + lot_str.split(' & ')[1])
            types.append(tempType)
        else:       
            lot_names.append(lot_str)
            types.append(tempType)
    data = None
    with open('../data/manual_additions.json') as j_file:
        data = json.load(j_file)
    
    for lot in data["lots"]:
        lot_names.append(lot["name"])
        types.append(lot["type"])

    return lot_names, types

def get_building_names():

    building_names = []

    url = 'http://www.buffalo.edu/administrative-services/managing-facilities/planning-designing-and-construction/building-profiles.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    buildingsRaw = soup.find("div", {"id":"page"})\
    .find("div", {"id" :"columns"})\
    .find("div",{"id":"center"}).\
    find("div", {"class":"par parsys"})\
    .find("div", {"class":"tabs section"})\
    .find(class_="tabs-component")\
    .find(class_="tabs-component-box-wrapper")\
    .find(class_="par parsys")\
    .findAll(class_="teaser-title")
    for name in buildingsRaw:
        building_names.append(name.text)    

    data = None
    with open('../data/manual_additions.json') as j_file:
        data = json.load(j_file)
    
    for building in data["buildings"]:
        building_names.append(building["name"])

    return building_names


def write_2_csv_lot_building(lot_names, types, building_names):
    fullData = [lot_names, types, building_names]
    with open('../data/lot_building_names.csv', 'w') as f:
        writer = csv.writer(f)
        for vals in zip_longest(*fullData):
            writer.writerow(vals)

def write_2_csv_lot(lot_names, types):
    fullData = [lot_names, types]
    with open('../data/lot_names.csv', 'w') as f:
        writer = csv.writer(f)
        for vals in zip_longest(*fullData):
            writer.writerow(vals)

def write_2_csv_building(building_names):
    fullData = [building_names]
    with open('../data/building_names.csv', 'w') as f:
        writer = csv.writer(f)
        for vals in zip_longest(*fullData):
            writer.writerow(vals)

if len(sys.argv) == 1:
    print ('Invocation:')
    print ('\tpython get_lot_building_names.py [ -lot | -building | -both ]')
    exit()
else:   
    if sys.argv[1] == '-lot':  
        lot_names, types = get_lot_names()
        write_2_csv_lot(lot_names, types)
    elif sys.argv[1] == '-building':
        building_names = get_building_names()
        write_2_csv_building(building_names)
    elif sys.argv[1] == '-both':
        lot_names, types = get_lot_names()
        building_names = get_building_names()
        write_2_csv_lot_building(lot_names, types, building_names)
    else:
        print ('Invocation:')
        print ('\tpython get_lot_building_names.py [ -lot | -building | -both ]')
        exit()
        

