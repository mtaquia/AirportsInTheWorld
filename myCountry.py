import sqlite3

conn = sqlite3.connect('myAirports.sqlite')
conn.text_factory = str  #without this line ,it will be Unicode 
cur = conn.cursor()

while True :
	option = raw_input('\n(1) Discover the Int. Code for a Country\n(2) Make a search if you know the Int.Code\n\n')
	if option not in ['1','2']:
		print '***** Error:Choose 1 or 2 *********'
		continue
	elif int(option) == 2:
		break
	else:
		cname = raw_input('Write some initial letters of the country name:')
		cname = cname.upper()
		cname = cname + '%'
		
		cur.execute('''SELECT Country,ISO_3166_2 from IsoCountry WHERE
		Country LIKE ?  ''',(cname,))

		cont = 0
		for line in cur:
			print line
			cont += 1

		if cont == 0 :
			print '*****  Not found!! *****'

country = raw_input('Write the international Code:').upper()

cur.execute('''SELECT Latitude, Longitude, AirportName FROM Airports 
	 	WHERE Country=?''',(country, ))

fullname = ''
with open('myAirports.js','w') as fhand:
	fhand.write("airports = [ ['Latitute','Longitude','Airport_Name'] ")

	for line in cur:
		fhand.write(',\n['+str(line[0])+','+str(line[1])+',"'+line[2]+'"]')
	fhand.write('\n];\n')
	try:
		cur.execute('SELECT Country from IsoCountry WHERE ISO_3166_2 = ?',(country,))
		fullname = cur.fetchone()[0]
	except:
		print '*****  Error : Type a correct Int. Code.  *****'
		exit()
	fhand.write('cname = "'+ fullname +'";')

cur.close()

print '\nWell done! \nCountry:'+fullname+'\nOpen and see myAirports.html'