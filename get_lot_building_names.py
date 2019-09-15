import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest


def getLotNames():

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
#			print(lot_name)
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
	return lot_names, types

def getBuildingNames():

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
	return building_names


def write2CSV(lot_names, types, building_names):
	fullData = [lot_names, types, building_names]
	with open('LotBuildingNames.csv', 'w') as f:
		writer = csv.writer(f)
		for vals in zip_longest(*fullData):
			writer.writerow(vals)

lot_names, types = getLotNames()
building_names = getBuildingNames()
write2CSV(lot_names, types, building_names)

'''
for i in range(len(lot_names)):
	print("Name: " + lot_names[i])
	print("Type: " + str(types[i]) + "\n")

for name in building_names:
	print(name)
'''
