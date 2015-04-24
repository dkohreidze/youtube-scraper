#!/usr/bin/python
# David Kohreidze
# about-data.py

# http://docs.python-requests.org/en/latest/user/quickstart/
# http://www.crummy.com/software/BeautifulSoup/bs4/doc/

import csv
import re
import requests
import time
from bs4 import BeautifulSoup

# create csv file in working directory
f = open("about-scrape-output.csv", "w+")

# list of URLs to scrape
l = [] 

# input file must contain 1 column of about page URLs
# ex: https://www.youtube.com/user/example/about
with open('inputURLs.csv', 'rU') as cf:
	reader = csv.reader(cf)
	for row in reader:
		l = l + row			

for current in l:
	# retrieves the resources from webpage
	r = requests.get(current)

	# parses HTML document
	soup = BeautifulSoup(r.text)

	# print the webpage we're scraping to output file
	f.write(current+',')
	print(current)

	# scrapes the subscriber and view count
	b = soup.find_all("li", "about-stat ") #trailing space is required.
	for i in b:
		value = i.b.text.strip().replace(',','')
		name = i.b.next_sibling.strip().replace(',','')
		f.write(value+',')
		print('%s = %s') % (name, value)

	# scrapes the description
	c = soup.find_all("div", "about-description")
	for i in c:
		description = i.text.strip().replace('\n',' ').replace(',','').encode("utf-8")
		f.write(description+',')
		print(description)

	# scrapes all the external links 
	a = soup.find_all("a", "about-channel-link ") #trailing space is required.
	for i in a:
		title = i.get('title').strip().replace(',','').encode("utf-8")
		url = i.get('href')
		f.write(title+','+url+',')
		print(url)

	f.write('\n')	
	print('\n')

	time.sleep(3)

cf.close()
f.close()
