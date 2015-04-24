#!/usr/bin/python
# David Kohreidze
# yt_related_channels.py

import csv
import re
import requests
import time
from bs4 import BeautifulSoup

f = open("workFile-channels.csv", "w+")
q = []

with open('list.csv', 'rU') as csvf:
	reader = csv.reader(csvf)
	for row in reader:
		q = q + row

print('\nInitial contents of queue:')
print('--------------------------') 
for each in q:
	print(each)
print('\n')

for each in q:
	current = q.pop(0)
	r = requests.get(current)
	soup = BeautifulSoup(r.text)
	related = soup.find_all("h3", "yt-lockup-title")

	print('Channels related to\n%s') %current
	print('---------------------')
	for each in related:
		a = each.find_all(href=re.compile("user"))
		for i in a:
			url = 'https://www.youtube.com'+i.get('href')
			print('%s,%s') % (i.text, url)
			if url not in q:
				q.append(url)
				f.write(url+'\n')
		
	print('\nUpdated queue')
	print('-------------')
	for each in q:
		print(each)

	print('\n\n')	
	
	time.sleep(10)

f.close()	


