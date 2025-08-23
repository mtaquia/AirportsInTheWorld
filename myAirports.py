import csv
import sqlite3
import time
import urllib

initial = time.time()
my_password = abc22!!!ereau
print 'Starting the program ...\n\n'
print 'Downloading airports.csv from the Internet\n'
fhand = urllib.urlopen('http://ourairports.com/data/airports.csv')
texto = ''
count = 0
for line in fhand:
	print line
	texto += line
	count += 1

with open('airports.csv','w') as f:
	f.write(texto)

print '********************************************************'
print 'Finish!!!! . You have downloaded the file airports.csv'
print 'The file has '+ str(count) + ' lines\n'

texto = ''
count = 0
print '\nDownloading iso_3166_2.csv from the Internet'

fhand = urllib.urlopen('https://commondatastorage.googleapis.com/ckannet-storage/2011-11-25T132653/iso_3166_2_countries.csv')
for line in fhand:
	print line
	texto += line
	count += 1

with open('iso_3166_2.csv','w') as f:
	f.write(texto)

print '********************************************************'
print 'Finish!!!! . You have downloaded the file iso_3166_2.csv'
print 'The file has '+ str(count) + ' lines\n'
texto = ''
count = 0

print '\n\nReading CSV files , creating myAirports database\n'


idAir = list()
typeAir = list()
nameAir = list()
latAir = list()
longAir = list()
countryAir = list()

#read  info from countries ,coordinates and names
with open('airports.csv','r') as f:
	reader = csv.reader(f)
	for row in reader:
		if row[0] == 'id' : continue
		#print row #['6523', '00A', 'heliport', 'Total Rf Heliport',...]
		idAir.append(row[0]) 
		typeAir.append(row[2])
		nameAir.append(row[3])
		latAir.append(row[4])
		longAir.append(row[5])
		countryAir.append(row[8])

#Replacing doubles for singles quotes in airports name.Error in myAirports.js
# [39.2831993103,-76.6019973755,"Marriott Parking Garage "Rooftop" Heliport"]
for i in range(len(nameAir)):
	nameAir[i] = nameAir[i].replace('"',"'")

print 'Creating and filling table Airports'

conn = sqlite3.connect('myAirports.sqlite')
cur = conn.cursor()
conn.text_factory = str

cur.execute(''' CREATE TABLE IF NOT EXISTS Airports(id INTEGER UNIQUE,
	Type TEXT,AirportName TEXT,Latitude REAL,Longitude REAL,Country TEXT) ''')

for i in range(len(idAir)):
	cur.execute('''INSERT OR IGNORE INTO Airports(id,Type,AirportName,Latitude,Longitude,Country) 
		VALUES(?,?,?,?,?,?)''',(idAir[i],typeAir[i],nameAir[i],latAir[i],
			longAir[i],countryAir[i]))

	# if i % 5000 == 0 : # I optimized by increasing the number divided
	# 	conn.commit()
conn.commit()
cur.close()

################################################################
#Create and fill table country -> iso_3166_2
print 'Complete!!\n\nCreating and filling table IsoCountry '

cname = list()
isoCountry = list()

with open('iso_3166_2.csv','r') as iso:
	reader = csv.reader(iso)
	for row in reader:
		if row[0] == 'Sort Order':continue
		cname.append(row[1].upper())
		isoCountry.append(row[10])

conn = sqlite3.connect('myAirports.sqlite')
cur = conn.cursor()
conn.text_factory = str

cur.execute(''' CREATE TABLE IF NOT EXISTS IsoCountry(Country TEXT ,
	ISO_3166_2 TEXT) ''')

for i in range(len(cname)):
	cur.execute('''INSERT OR IGNORE INTO IsoCountry(Country,ISO_3166_2) 
		VALUES(?,?)''',(cname[i],isoCountry[i]))

conn.commit()
cur.close()

final = time.time()

print 'Complete!! \n\nContinue with myCountry.py file'
print '\nThis script took '+str(final-initial) +' seconds.'
