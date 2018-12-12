from bs4 import BeautifulSoup
import pandas as pd
#import numpy as np
#from time import gmtime, strftime
#import os
import glob
from datetime import datetime



def get_Features_for_Month(Month):
	df=pd.DataFrame([])
	files= glob.glob(Month+'/*.html')
	for file in files:
		try:
			#print('------------------------'+file)
			values_for_df=[]
			names_for_df=[]

			f = open(file)
			sauce=f.read()
			soupe=BeautifulSoup(sauce, 'lxml')
			
			head=soupe.head
			browsertitle=head.title.text
			#print(browsertitle)
			values_for_df.append(browsertitle)
			names_for_df.append('browsertitle')
			
			body=soupe.body
			stand=body.find('span', class_='stand').text

			dto=datetime.strptime(stand, 'Stand: %d.%m.%Y %H:%M Uhr')
			stand=datetime.strftime(dto, '%Y-%m-%d %H:%M')
			#print(stand)

			values_for_df.append(stand)
			names_for_df.append('stand')
			



			headline=body.find('span', class_='headline').text
			values_for_df.append(headline)
			names_for_df.append('headline')
			print(headline)
			
			dachzeile=body.find('span', class_='dachzeile').text
			values_for_df.append(dachzeile)
			names_for_df.append('dachzeile')
			#print(dachzeile)
			
			bodyclass=body['class']
			values_for_df.append(bodyclass)
			names_for_df.append('bodyclass')
			#print(bodyclass)
			
			####Rubrik
			try:
				div=body.find('div', class_='breadcrumb')
				ul=div.ul
				a=ul.find_all('a')
				rubrik=a[1].text
				title2=a[2].text
			except:
				rubrik=None
				title2=None
			values_for_df.append(rubrik)
			names_for_df.append('rubrik')
			#print(rubrik)
			
			p=body.find('p', class_='autorenzeile')
			if p:
				autorenzeile=p.text
				#print(autorenzeile)
				autor_unter_titel=True
			else:
				autorenzeile=None

			values_for_df.append(autorenzeile)
			names_for_df.append('autorenzeile')
				
			content=body.find(id='content')
			content=content.find('div', class_='storywrapper')

			h2s=content.find_all('h2', class_='subtitle')
			KapitelUberschriften=[]
			if h2s:
				for h2 in h2s:
					KapitelUberschriften.append(h2.text)
			#print(len(KapitelUberschriften),KapitelUberschriften)
			KapitelUberschriftenAnzahl=len(KapitelUberschriften)

			values_for_df.append(KapitelUberschriften)
			names_for_df.append('KapitelUberschriften')
			values_for_df.append(KapitelUberschriftenAnzahl)
			names_for_df.append('KapitelUberschriftenAnzahl')

			section=content.find('div',class_='sectionZ')

			InfoText=section.div.div.div.p.strong.text
			values_for_df.append(InfoText)
			names_for_df.append('InfoText')
			#print(InfoText)

			values_for_df.append(InfoText.count('CDU'))
			names_for_df.append('CDU')
			values_for_df.append(InfoText.count('SPD'))
			names_for_df.append('SPD')

			ssection=section.find('div',class_='modParagraph')
			textbausteine=ssection.find_all('p',class_='text')
			plain_text=''
			for textbaustein in textbausteine:
				plain_text=plain_text+textbaustein.text+'\n'
			#print(plain_text)
			wortAnzahl=len(plain_text.split())
			values_for_df.append(wortAnzahl)
			names_for_df.append('wortAnzahl')
			#print(wortAnzahl)

			links=[]
			for textbaustein in textbausteine:
				linkstags=textbaustein.find_all('a')
				if len(linkstags):
					for link in linkstags:
						links.append(link['href'])
			values_for_df.append(links)
			names_for_df.append('links')
			#print(links)


			tags=[]
			geotags=[]
			linkstags=ssection.find_all('a')
			for l in linkstags:
				if '/thema/' in l['href']:
					tags.append(l.text)
				if '/geo/' in l['href']:
					geotags.append(l.text)
			values_for_df.append(tags)
			names_for_df.append('tags')
			values_for_df.append(geotags)
			names_for_df.append('geotags')
			#print(tags)
			#print(geotags)

			tagsDateinamen=file.split('\\')[-1].split('.')[0].split('-')[:-1]
			values_for_df.append(tagsDateinamen)
			names_for_df.append('tagsDateinamen')
			#print('hier',tagsDateinamen)

			MedienAnzahl=None

			dftemp=pd.DataFrame([[*values_for_df]], columns=names_for_df)
			df=pd.concat((df,dftemp),ignore_index=True)
		except:
			print('--fehler--')

			
	df.to_excel(Month+'/list_of_all_Article_and_Feature_V1-2.xlsx')



for Month in glob.glob('*/'):
	Month=Month[:-1]
	print(Month)
	get_Features_for_Month(Month)
