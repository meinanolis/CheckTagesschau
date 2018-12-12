#{system("python /home/pi/share/CheckTagesschau/sharefolder/doit1.py &")}
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from time import localtime, strftime
import re

os.chdir('/home/pi/share/CheckTagesschau/sharefolder')

day_now=strftime("%Y-%m-%d", localtime())
month_now=strftime("%Y-%m", localtime())
time_now=strftime("%H:%M:%S", localtime())

def load_url(url):
	source_code=requests.get(url)
	plain_text=source_code.text
	soup=BeautifulSoup(plain_text, 'lxml')
	return soup

if os.path.isfile(month_now+'/list_of_all_Article.xlsx'):
	df_all_article=pd.read_excel(month_now+'/list_of_all_Article.xlsx')
else:
	df_all_article=pd.DataFrame([],columns=['link','erstveroeffentlihung','startseite','position'])

url='http://www.tagesschau.de'
main_page_soup=load_url(url)
content=main_page_soup.find(id='content')
sections=content.find_all('div',class_='section')
i=0
alllinks=[]
for section in sections[1:]:
	links=section.find_all('a')
	links2=[]
	for link in links:
		href=link.get('href')
		if (not ('multimedia' in href or '//' in href or '#' in href or 'tsvorzwanzigjahren100' in href or 'rssfeeds' in href)) and '.html'in href:
			links2.append(href)
	alllinks=alllinks+links2

alllinks,position=np.unique(np.array(alllinks),return_index=True)

neue_artikel=0
for i,href in zip(position,alllinks):
	print(i,href)
	liste = np.array(df_all_article[['link']].values)[:,0]
	if not href in liste:
		df_temp=pd.DataFrame([[href,day_now+' '+time_now,day_now+' '+time_now,'\''+str(int(i))]],columns=['link','erstveroeffentlihung','startseite','position'])
		df_all_article=pd.concat([df_all_article,df_temp],ignore_index=True)
		filename=href.split('/')[-1]
		url2='http://www.tagesschau.de'+href
		article_soup=load_url(url2)
		if not os.path.exists(month_now):
		    os.makedirs(month_now)
		with open(month_now+'/'+filename, "w") as file:
		    file.write(str(article_soup.encode("UTF-8")))
		neue_artikel+=1
	else:
		indexx=df_all_article.loc[df_all_article['link']==href].index
		#print(indexx)
		iloc=df_all_article['position'].loc[indexx].values
		iloc=str(iloc[0])+', '+str(i)
		df_all_article['position'].loc[indexx]=iloc

		iloc=df_all_article['startseite'].loc[indexx].values
		iloc=str(iloc[0])+', '+day_now+' '+time_now
		df_all_article['startseite'].loc[indexx]=iloc
				

df_all_article.to_excel(month_now+'/list_of_all_Article.xlsx')



f=open('veroeffentlichungsverlauf.txt', 'a')
f.write(day_now+' '+time_now+'\t'+str(len(alllinks))+'\t'+str(neue_artikel)+'\n')
f.close()


import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime



df=pd.read_csv('veroeffentlichungsverlauf.txt',sep='\t')
neu=df['Neue seit letztem Check'].values
alle=df['Artikel auf Startseite'].values
dates= [datetime.strptime(d, '%Y-%m-%d %H:%M:%S') for d in df['Zeit'].values]
hours= [datetime.strftime(d, '%H:%M') for d in dates]
dates = matplotlib.dates.date2num(dates)


plt.plot_date(dates,alle,'.-',label='Artikel auf Startseite')
plt.plot_date(dates,neu,'.-',label='Neue Artikel')
plt.ylim(-1,np.max(alle)+2)
divider=np.round(len(dates)/6)
plt.xticks(dates[::divider],hours[::divider])
plt.title('Aktuallisierungen Heute CheckTagesschau\n'+day_now+' '+time_now)
plt.xlabel('Zeit')
plt.legend()
plt.grid()
plt.gcf().autofmt_xdate()
plt.tight_layout()
plt.savefig('Artikel_auf_Startseite.png')
plt.savefig('/opt/fhem/www/images/default/Artikel_auf_Startseite.png')