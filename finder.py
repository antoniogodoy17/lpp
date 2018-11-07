import codecs
import os
import sys

def search():
	directory = 'tests/'
	catalog = []
	selected = ''
	answer = False
	counter = 1

	for base, dirs, files in os.walk(directory):
		catalog.append(files)
		for file in files:
			print(str(counter)+". "+file)
			counter = counter + 1

	while answer == False:
	    selected = input('\nTest Number: ')
	    for file in files:
	        if file == files[int(selected)-1]:
	            answer = True
	            break

	test = directory + files[int(selected)-1]
	fp = codecs.open(test, "r","utf-8")
	content = fp.read()
	fp.close()

	return content

