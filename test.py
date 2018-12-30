import glob
import os
from bs4 import BeautifulSoup
import difflib
#import webbrowser
import MySQLdb
import sys

f=open('2018-11/migranten-us-grenze-101.html/0_migranten-us-grenze-101.html')
sauce=f.read()
f.close()
soupe=BeautifulSoup(sauce, 'lxml')
body=soupe.body
content=body.find(id='content')
contentlist=[]
h1=content.h1
contentlist.append(h1)
stand=content.find('span', class_='stand')
contentlist.append(stand)

section=content.find('div',class_='sectionZ').find('div',class_='modParagraph')
for child in section.contents:
	if 'class="text small' in str(child):
		contentlist.append(child)
	elif '<h2 class="subtitle' in str(child):
		contentlist.append(child)
	elif 'image">' in str(child):
		image=child.find('img')
		contentlist.append(image)
		infotext=child.find('p', class_="infotext")
		contentlist.append(infotext)
print(len(contentlist))

f=open('test2.html','wb')
f.write(b'<html><body>')
f.write(h1.prettify("utf-8"))
f.write(b'</body></html>')
f.close()