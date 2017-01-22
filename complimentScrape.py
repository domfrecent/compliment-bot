import json
import urllib
import BeautifulSoup
import re
import random

#Create global array of compliments
arr = []

# Connect to webpage with 200+ compliments
def parseCompliments():
	url = urllib.urlopen("http://peoplearenice.blogspot.com/p/compliment-list.html")
	data = url.read()

	#Initial webpage parsing
	soup = BeautifulSoup.BeautifulSoup(data)
	body = soup.find('div', attrs={'class':'post-body entry-content'})
	global arr

	# Populate array of compliments
	for span in body.findAll('span'):
		tempStr = str(span.string)

		try:
			type(int(tempStr[0])) #check if first element of string is a number, if not, skip adding string to the list
			match = re.search('^[0-9]+\.\s(.*)', tempStr)
			if match:
				arr.append(match.group(1))
		except ValueError:
			pass
			#print "Does not start with a number, not saving to array"

	#for i in arr:
		#print i

# Pull random element from compliment array
def getRandCompliment():
	global arr
	random.seed()
	randIndex = random.randint(0, len(arr) - 1)
	randCompliment = arr[randIndex]
	print randCompliment
	return randCompliment



