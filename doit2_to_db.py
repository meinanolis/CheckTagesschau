import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from time import gmtime, strftime
import os
import re
import MySQLdb

os.chdir('/home/pi/share/CheckTagesschau/sharefolder')

flog=open('log.txt','a')
flog.write('1')
flog.close()

connection = MySQLdb.connect(
     host="192.168.2.3",
     port=3307,
     db="Tagesschau",
     user="Tagesschau", passwd="g00gle"
    )

c=connection.cursor()

c.execute('SELECT `ID` FROM `Uebersicht`')
table_rows = c.fetchall()
table_rows=list(table_rows)
ID=np.max(table_rows)

c.execute('SELECT * FROM `Uebersicht` ORDER BY `ID` DESC LIMIT 500')
table_rows = c.fetchall()
table_rows=list(table_rows)
all_article=[t[1] for t in table_rows]
all_ID=[t[0] for t in table_rows]



def load_url(url):
	source_code=requests.get(url)
	plain_text=source_code.text
	soup=BeautifulSoup(plain_text, 'lxml')
	return soup


day_now=strftime("%d", gmtime())
month_now=strftime("%m", gmtime())
year_now=strftime("%Y", gmtime())
hour_now=strftime("%H", gmtime())
min_now=strftime("%M", gmtime())
timestemp=strftime("%Y-%M-%d - %H:%M", gmtime())

with open('log.txt','a') as file:
	file.write(timestemp+'\n')

#if 1:
try:
	url='http://www.tagesschau.de'
	main_page_soup=load_url(url)
	content=main_page_soup.find(id='content')
	sections=content.find_all('div',class_='section')
	i=0
	alllinks=[]
	with open('log.txt','a') as file:
		file.write('titlepage heruntergeladen\n')
	for section in sections[1:]:
		links=section.find_all('a')
		links2=[]
		for link in links:
			href=link.get('href')
			try:
				if (not ('multimedia' in href or '//' in href or '#' in href or 'tsvorzwanzigjahren100' in href or 'rssfeeds' in href)) and '.html'in href:
					links2.append(href)
					
			except:
				print(href)
				with open('log.txt','a') as file:
					file.write('fehler 1001\n')
		alllinks=alllinks+links2
	alllinks,position=np.unique(np.array(alllinks),return_index=True)
	with open('log.txt','a') as file:
		file.write('alle links extrahiert\n')


	neue_artikel=0
	alte_artikel=0
	c.execute("INSERT INTO Homepage (Pos1) VALUES (1)")
	connection.commit()
	for i,href in zip(position,alllinks):
		filename=href.split('/')[-1]
		if not filename in all_article:
			print(i,href)
			with open('log.txt','a') as file:
				file.write('--neu geladen '+href+'\n')
			ID+=1
			Rubrik=href.split('/')[-2]
			RockPfad=year_now+'-'+month_now+'/'+filename
			url2='http://www.tagesschau.de'+href
			article_soup=load_url(url2)
			Seiteninhalt=str(article_soup.encode("UTF-8"), "utf-8")
			c.execute("INSERT INTO `Uebersicht` (`ID`, `Name`, `Jahr`, `Monat`, `Tag`, `Stunde`, `Minute`, `Rubrik`, `TagesschauPfad`, `RockPfad`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",
				(ID,filename,year_now,month_now,day_now,hour_now,min_now,Rubrik,url2,RockPfad))
			connection.commit()

			if not os.path.exists(year_now+'-'+month_now):
			    os.makedirs(year_now+'-'+month_now)
			os.makedirs(RockPfad)
			with open(RockPfad+'/0_'+filename, "w") as file:
			    file.write(Seiteninhalt)
			neue_artikel+=1
			if i < 99:
				c.execute("UPDATE Homepage SET Pos"+str(i+1)+" = "+str(ID)+" ORDER BY HP_ID DESC LIMIT 1")
				connection.commit()
		else:
			alte_artikel+=1
			if i < 99:
				ii=np.argwhere(np.array(all_article)==filename)[0][0]
				#print(ii)
				ID2=all_ID[ii]
				c.execute("UPDATE Homepage SET Pos"+str(i+1)+" = "+str(ID2)+" ORDER BY HP_ID DESC LIMIT 1")
				connection.commit()

	c.execute("INSERT INTO `n_neue_Artikel` (`neu`, `total`) VALUES ('"+str(neue_artikel)+"', '"+str(neue_artikel+alte_artikel)+"');")
	connection.commit()


	#---------------------------------------------------#
	#                mehrfach herunterladen             #
	#---------------------------------------------------#

	#-------------1h			

	c.execute("SELECT * FROM Uebersicht WHERE date <= NOW() - INTERVAL 1 HOUR AND 1h = 0 ORDER BY `ID` DESC LIMIT 100")
	table_rows = c.fetchall()
	table_rows=list(table_rows)
	#print(table_rows)
	reload_article_pfad=[t[8] for t in table_rows]
	reload_article_id=[t[0] for t in table_rows]
	reload_article_rockpfad=[t[9] for t in table_rows]
	for i,p,rp in zip(reload_article_id,reload_article_pfad,reload_article_rockpfad):
		#print(i,p)
		article_soup=load_url(p)
		Seiteninhalt=str(article_soup.encode("UTF-8"), "utf-8")
		filename=p.split('/')[-1]
		with open(rp+'/1_'+filename, "w") as file:
		    file.write(Seiteninhalt)
		c.execute("UPDATE `Uebersicht` SET `1h` = '1' WHERE `Uebersicht`.`ID` = "+str(i)+";")
		connection.commit()
	print(len(reload_article_id), 'artikel in der kathegorie 1h reloadet')
	with open('log.txt','a') as file:
		file.write(str(len(reload_article_id))+'artikel in der kathegorie 1h reloadet'+'\n')

	#-------------6h			

	c.execute("SELECT * FROM Uebersicht WHERE date <= NOW() - INTERVAL 6 HOUR AND 6h = 0 ORDER BY `ID` DESC LIMIT 100")
	table_rows = c.fetchall()
	table_rows=list(table_rows)
	#print(table_rows)
	reload_article_pfad=[t[8] for t in table_rows]
	reload_article_id=[t[0] for t in table_rows]
	reload_article_rockpfad=[t[9] for t in table_rows]
	for i,p,rp in zip(reload_article_id,reload_article_pfad,reload_article_rockpfad):
		#print(i,p)
		article_soup=load_url(p)
		Seiteninhalt=str(article_soup.encode("UTF-8"), "utf-8")
		filename=p.split('/')[-1]
		with open(rp+'/2_'+filename, "w") as file:
		    file.write(Seiteninhalt)
		c.execute("UPDATE `Uebersicht` SET `6h` = '1' WHERE `Uebersicht`.`ID` = "+str(i)+";")
		connection.commit()
	print(len(reload_article_id), 'artikel in der kathegorie 6h reloadet')
	with open('log.txt','a') as file:
		file.write(str(len(reload_article_id))+'artikel in der kathegorie 6h reloadet'+'\n')


	#-------------1tag			

	c.execute("SELECT * FROM Uebersicht WHERE date <= NOW() - INTERVAL 24 HOUR AND 1tag = 0 ORDER BY `ID` DESC LIMIT 100")
	table_rows = c.fetchall()
	table_rows=list(table_rows)
	#print(table_rows)
	reload_article_pfad=[t[8] for t in table_rows]
	reload_article_id=[t[0] for t in table_rows]
	reload_article_rockpfad=[t[9] for t in table_rows]
	for i,p,rp in zip(reload_article_id,reload_article_pfad,reload_article_rockpfad):
		#print(i,p)
		article_soup=load_url(p)
		Seiteninhalt=str(article_soup.encode("UTF-8"), "utf-8")
		filename=p.split('/')[-1]
		with open(rp+'/3_'+filename, "w") as file:
		    file.write(Seiteninhalt)
		c.execute("UPDATE `Uebersicht` SET `1tag` = '1' WHERE `Uebersicht`.`ID` = "+str(i)+";")
		connection.commit()
	print(len(reload_article_id), 'artikel in der kathegorie 1tag reloadet')
	with open('log.txt','a') as file:
		file.write(str(len(reload_article_id))+'artikel in der kathegorie 1tag reloadet'+'\n')

	#-------------3tage			

	c.execute("SELECT * FROM Uebersicht WHERE date <= NOW() - INTERVAL 3 DAY AND 3tage = 0 ORDER BY `ID` DESC LIMIT 100")
	table_rows = c.fetchall()
	table_rows=list(table_rows)
	#print(table_rows)
	reload_article_pfad=[t[8] for t in table_rows]
	reload_article_id=[t[0] for t in table_rows]
	reload_article_rockpfad=[t[9] for t in table_rows]
	for i,p,rp in zip(reload_article_id,reload_article_pfad,reload_article_rockpfad):
		#print(i,p)
		article_soup=load_url(p)
		Seiteninhalt=str(article_soup.encode("UTF-8"), "utf-8")
		filename=p.split('/')[-1]
		with open(rp+'/4_'+filename, "w") as file:
		    file.write(Seiteninhalt)
		c.execute("UPDATE `Uebersicht` SET `3tage` = '1' WHERE `Uebersicht`.`ID` = "+str(i)+";")
		connection.commit()
	print(len(reload_article_id), 'artikel in der kathegorie 3tage reloadet')
	with open('log.txt','a') as file:
		file.write(str(len(reload_article_id))+'artikel in der kathegorie 3tage reloadet'+'\n')


	#-------------7tage			

	c.execute("SELECT * FROM Uebersicht WHERE date <= NOW() - INTERVAL 7 DAY AND 7tage = 0 ORDER BY `ID` DESC LIMIT 100")
	table_rows = c.fetchall()
	table_rows=list(table_rows)
	#print(table_rows)
	reload_article_pfad=[t[8] for t in table_rows]
	reload_article_id=[t[0] for t in table_rows]
	reload_article_rockpfad=[t[9] for t in table_rows]
	for i,p,rp in zip(reload_article_id,reload_article_pfad,reload_article_rockpfad):
		#print(i,p)
		article_soup=load_url(p)
		Seiteninhalt=str(article_soup.encode("UTF-8"), "utf-8")
		filename=p.split('/')[-1]
		with open(rp+'/5_'+filename, "w") as file:
		    file.write(Seiteninhalt)
		c.execute("UPDATE `Uebersicht` SET `7tage` = '1' WHERE `Uebersicht`.`ID` = "+str(i)+";")
		connection.commit()
	print(len(reload_article_id), 'artikel in der kathegorie 7tage reloadet')
	with open('log.txt','a') as file:
		file.write(str(len(reload_article_id))+'artikel in der kathegorie 7tage reloadet'+'\n')


	#-------------1monat			

	c.execute("SELECT * FROM Uebersicht WHERE date <= NOW() - INTERVAL 30 DAY AND 1monat = 0 ORDER BY `ID` DESC LIMIT 100")
	table_rows = c.fetchall()
	table_rows=list(table_rows)
	#print(table_rows)
	reload_article_pfad=[t[8] for t in table_rows]
	reload_article_id=[t[0] for t in table_rows]
	reload_article_rockpfad=[t[9] for t in table_rows]
	for i,p,rp in zip(reload_article_id,reload_article_pfad,reload_article_rockpfad):
		#print(i,p)
		article_soup=load_url(p)
		Seiteninhalt=str(article_soup.encode("UTF-8"), "utf-8")
		filename=p.split('/')[-1]
		with open(rp+'/6_'+filename, "w") as file:
		    file.write(Seiteninhalt)
		c.execute("UPDATE `Uebersicht` SET `1monat` = '1' WHERE `Uebersicht`.`ID` = "+str(i)+";")
		connection.commit()
	print(len(reload_article_id), 'artikel in der kathegorie 1monat reloadet')
	with open('log.txt','a') as file:
		file.write(str(len(reload_article_id))+'artikel in der kathegorie 1monat reloadet'+'\n')




	#--------------------------------------#
	#              Plots                   #
	#--------------------------------------#


	import matplotlib
	# Force matplotlib to not use any Xwindows backend.
	matplotlib.use('Agg')
	import matplotlib.pyplot as plt
	from datetime import datetime




	c.execute("SELECT * FROM `n_neue_Artikel` WHERE `date` >= NOW() - INTERVAL 7 DAY")
	table_rows = c.fetchall()
	connection.close()
	table_rows=list(table_rows)
	dates=[t[1] for t in table_rows]
	neu=[t[2] for t in table_rows]
	alle=[t[3] for t in table_rows]

	hours= [datetime.strftime(d, '%H:%M') for d in dates]
	dates = matplotlib.dates.date2num(dates)


	plt.plot_date(dates,alle,'.-',label='Artikel auf Startseite')
	plt.plot_date(dates,neu,'.-',label='Neue Artikel')
	plt.ylim(-1,np.max(alle)+2)
	divider=np.round(len(dates)/6)
	#plt.xticks(dates[::divider],hours[::divider])
	plt.title('Aktuallisierungen Heute CheckTagesschau\n'+day_now+' '+hour_now+':'+min_now)
	plt.xlabel('Zeit')
	plt.legend()
	plt.grid()
	plt.gcf().autofmt_xdate()
	plt.tight_layout()
	plt.savefig('Artikel_auf_Startseite.png')
	plt.savefig('/opt/fhem/www/images/default/Artikel_auf_Startseite.png')
	with open('log.txt','a') as file:
		file.write('Plot erstellt'+'\n\n\n\n-------------------------------------\n')
except Exception as e: 
	with open('log.txt','a') as file:
		file.write(str(e)+'\n')
		print(e)