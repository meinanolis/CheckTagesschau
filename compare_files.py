import glob
import os
from bs4 import BeautifulSoup
import difflib
import webbrowser
import MySQLdb

os.chdir('//RASPBERRYPI/PiShare/CheckTagesschau/sharefolder/')

connection = MySQLdb.connect(
     host="192.168.2.100",
     port=3307,
     db="Tagesschau",
     user="Tagesschau", passwd="g00gle"
    )

c=connection.cursor()

for wdh in [1,2,3,4,5]:

	c.execute('SELECT `ID`,`Name`,`RockPfad` FROM `Uebersicht`')
	table_rows = c.fetchall()
	table_rows=list(table_rows)
	for row in table_rows[1:]:
		ID,name,pfad=row
		print(wdh,name)
		if wdh ==1:
			c.execute('SELECT `ID` FROM `Vergleich` WHERE `ID`='+str(ID))
			table_rows = c.fetchall()
			table_rows=list(table_rows)
			mybool=bool(table_rows)
		else:
			c.execute('SELECT `'+str(wdh)+'-'+str(wdh+1)+'` FROM `Vergleich` WHERE `ID`='+str(ID))
			table_rows = c.fetchall()
			table_rows=list(table_rows)
			mybool=bool(table_rows[0][0])
		if not mybool:
			try:
				f = open(pfad+'/'+str(wdh-1)+'_'+name)
				sauce=f.read()
				f.close()
				soupe=BeautifulSoup(sauce, 'lxml')
				body=soupe.body
				stand=body.find('span', class_='stand').text
				content=body.find(id='content')
				section=content.find('div',class_='sectionZ')
				ssection=section.find('div',class_='modParagraph')
				textbausteine1=ssection.find_all('p',class_='text')
				h2s1=content.find_all('h2', class_='subtitle')
				head=soupe.head
				browsertitle1=head.title.text
				headline1=body.find('span', class_='headline').text
				dachzeile1=body.find('span', class_='dachzeile').text	
				stand1=body.find('span', class_='stand').text	

				for i in range(len(textbausteine1)):
					if textbausteine1[i].find('a'):
						if '#comment-' in textbausteine1[i].find('a')['href']:
							del textbausteine1[i]


				f = open(pfad+'/'+str(wdh)+'_'+name)
				sauce=f.read()
				f.close()
				soupe=BeautifulSoup(sauce, 'lxml')
				body=soupe.body
				stand=body.find('span', class_='stand').text
				content=body.find(id='content')
				section=content.find('div',class_='sectionZ')
				ssection=section.find('div',class_='modParagraph')
				textbausteine2=ssection.find_all('p',class_='text')
				h2s2=content.find_all('h2', class_='subtitle')
				head=soupe.head
				browsertitle2=head.title.text
				headline2=body.find('span', class_='headline').text
				dachzeile2=body.find('span', class_='dachzeile').text
				stand2=body.find('span', class_='stand').text

				for i in range(len(textbausteine2)):
					if textbausteine2[i].find('a'):
						if '#comment-' in textbausteine2[i].find('a')['href']:
							del textbausteine2[i]

				textbausteine1=[t.text for t in textbausteine1]+[h.text for h in h2s1]+[browsertitle1,headline1,dachzeile1,stand1]
				textbausteine2=[t.text for t in textbausteine2]+[h.text for h in h2s2]+[browsertitle2,headline2,dachzeile2,stand2]


				if 0:
					html = difflib.HtmlDiff().make_table(fromlines=textbausteine1,tolines=textbausteine2)
					path = os.path.abspath('temp.html')
					url = 'file://' + path

					with open(path, 'w') as f:
					    f.write(html)
					webbrowser.open(url)

				idiff=0
				for d in difflib.context_diff(textbausteine1,textbausteine2,n=0):
					print(d)
					idiff+=1

			except:
				idiff=999
			print(idiff)
			if wdh==1:
				try:
					c.execute("INSERT INTO `Vergleich` (`ID`, `Name`, `1-2`) VALUES ('"+str(ID)+"', '"+name+"', '"+str(idiff)+"');")
					connection.commit()
				except:
					pass
			else:
				c.execute('UPDATE `Vergleich` SET `'+str(wdh)+'-'+str(wdh+1)+'` = '+str(idiff)+' WHERE `Vergleich`.`ID` = '+str(ID)+';')

