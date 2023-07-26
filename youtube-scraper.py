#!/usr/bin/python
# David Kohreidze
# youtube-scraper.py

# Library documentation
# http://docs.python-requests.org/en/latest/user/quickstart/
# http://www.crummy.com/software/BeautifulSoup/bs4/doc/

import csv
import re
import requests
import time
from bs4 import BeautifulSoup

# scrapes the title 
def get_title():
	d = soup.find_all('h1', 'branded-page-header-title')
	for i in d:
		title = i.text.strip().replace('\n',' ').replace(',','').encode('utf-8') 
		f.write(title+',')
		print('\t%s') % (title)

# scrapes the subscriber count
def get_subs():
	b = soup.find_all('span', 'about-stat')
	for i in b:
		try:			
			value = i.b.text.strip().replace(',','')					
			if len(b) == 3:
				f.write(value+',')
				print('\t%s') %(value)
			elif len(b) == 2:
				f.write('null,'+ value + ',')
				print('\tsubs = null\n\t%s') %(value)
			else:
				f.write('null,null,')
				print('\tsubs = null\nviews = null')
		except AttributeError:
			pass

# scrapes the description
def get_description():
	c = soup.find_all('div', 'about-description')
	if c:
		for i in c:
			description = i.text.strip().replace('\n',' ').replace(',','').encode('utf-8')		
			f.write(description+',')
			print('\t%s') % (description)
			
			regex = re.compile(("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
						        '{|}~-]+)*(@|\sat\s|\[at\])(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|'
						        '\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)'))
			
			email = re.search(regex, description)
			if email:
				if not email.group(0).startswith('//'):
					print('\tEmail = ' + email.group())
					f.write(email.group(0)+',')
					k.write(email.group(0)+',')

			else:
				print('\tEmail = null')
				f.write('null,')
	else:
		print('\tDescription = null\n\tEmail = null')
		f.write('null,null,')

# scrapes all the external links 
def get_links():
	a = soup.find_all('a', 'about-channel-link ') # trailing space is required.
	for i in a:
		url = i.get('href')
		externalLinks.append(url)
		f.write(url+',')
		print('\t%s') % (url)

# scrapes the related channels
def get_related():
	s = soup.find_all('h3', 'yt-lockup-title')
	for i in s:
		t = i.find_all(href=re.compile('user'))
		for i in t:
			url = 'https://www.youtube.com'+i.get('href')
			related.write(url+'\n')
			#print('\t\t%s,%s') % (i.text, url)	

# create output files
f = open('meta-data.csv', 'w+')
k = open('key-data.csv', 'w+')
related = open('related-channels.csv', 'w+')

# empy list to save pages we've already scraped
visited = []

externalLinks = []

# disassemble YouTube search result page URL
base = 'https://www.youtube.com/results?search_query='
page = '&page='
q = ['dog+training', 'dog+behavior'] # enumerate all keywords here
count = 1 # start on page 1
pagesToScrape = 1 # the number of search result pages to scrape
timeToSleep = 3 # the number of seconds between pings to the YouTube server

# set outout csv file column labels
f.write('url, title, subs, views, description, email, external links\n')

for query in q:
	while count <= pagesToScrape:
		# assemble the URL to scrape
		scrapeURL = base + str(query) + page + str(count)
		
		print('\nScraping %s\n') %(scrapeURL)
		
		# ping and retrieve search result page HTML 
		r = requests.get(scrapeURL)

		# create Soup object from HTML 
		soup = BeautifulSoup(r.text)

		# parse channel container
		users = soup.find_all('div', 'yt-lockup-byline')
		
		for each in users:
			# parse all URLs that contain 'user'
			a = each.find_all(href=re.compile('user'))
			for i in a:
				# assemble channel's about page; this is where our data is located
				url = 'https://www.youtube.com'+i.get('href')+'/about'
				
				# check to see if channel has already been scraped
				if url in visited:
					print('\t%s has already been scraped\n\n') %(url)
				else:
					# ping and retreive channel's HTML, store as Soup object
					r = requests.get(url)
					soup = BeautifulSoup(r.text)

					# output channel url to csv file & terminal
					f.write(url + ',')
					k.write(url +',')
					print('\t%s') %(url)

					# scrape the meta data
					get_title()
					get_subs()
					get_description()
					get_links()
					get_related()

					# formatting csv & terminal output
					f.write('\n')	
					print('\n')

					# add url to visited list
					visited.append(url)

					# time delay between pings to YouTube server
					time.sleep(timeToSleep)
		
		# iterate to the next search result page
		count += 1
		print('\n')
	
	# reset page count as we've iterated to next search term
	count = 1
	print('\n')	

print(externalLinks)
f.close()
k.close()
