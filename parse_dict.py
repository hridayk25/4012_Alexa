import csv
with open('ChickfilAmenuitems - Sheet1.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		print(row['Menu Item'], row['Category'], row['Price'], row['Calories'])
print(row)			
#(row)
#OrderedDict([('first_name', 'John'), ('last_name', 'Cleese')])
