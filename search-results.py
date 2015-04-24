#!/usr/bin/python
# David Kohreidze
# search-results.py

# http://docs.python-requests.org/en/latest/user/quickstart/
# http://www.crummy.com/software/BeautifulSoup/bs4/doc/

import csv
import re
import requests
import time
from bs4 import BeautifulSoup

f = open("search-scrape-output.csv", "w+")

base = "https://www.youtube.com/results?search_query="
l = ['search+queries+here', 'more'] # queries must be encoded
page = "&page="
count = 1

for query in l:
	while count <= 20: # number of pages to scrape
		scrapeURL = base + str(query) + page + str(count) # build url 
		print('Scraping = %s\n') %(scrapeURL)
		r = requests.get(scrapeURL) # ping and retrieve page resources
		soup = BeautifulSoup(r.text) # parse html assets
		users = soup.find_all("div", "yt-lockup-byline") # filter username container
		for each in users:
			a = each.find_all(href=re.compile("user")) # get only /user/ links 
			for i in a:
				url = 'https://www.youtube.com'+i.get('href') # scrape and build user link
				print('\t%s,%s') % (i.text, url)
				f.write(url+'\n') # write to csv file
		count += 1	
		time.sleep(3) # wait for 3 seconds between pings
		print('\n')
	count = 1
	print('\n')	

print('\nComplete.\n')
f.close()