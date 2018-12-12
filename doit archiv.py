import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from time import gmtime, strftime
import os


def load_url(url):
	source_code=requests.get(url)
	plain_text=source_code.text
	soup=BeautifulSoup(plain_text, 'lxml')
	return soup

df_all_article=pd.read_excel('list_of_all_Article.xlsx')
#df_all_article=pd.DataFrame([],columns=['link','date'])
day_now=strftime("%Y-%m-%d", gmtime())
time_now=strftime("%H:%M:%S", gmtime())
day_now='alt'





url='http://www.tagesschau.de/archiv/meldungsarchiv100~_date-201802.html'
main_page_soup=load_url(url)
content=main_page_soup.find(id='content')
sections=content.find_all('div',class_='sectionZ')
for section in sections:
	links=section.find_all('a')
	for link in links:
		href=link.get('href')
		print(href)
		if not ('multimedia' in href or '//' in href or '#' in href):
			#print(link.h4)
			
			liste = np.array(df_all_article[['link']].values)[:,0]
			if not href in liste:
				df_temp=pd.DataFrame([[href,day_now+' '+time_now]],columns=['link','date'])
				df_all_article=pd.concat([df_all_article,df_temp],ignore_index=True)
				filename=href.split('/')[-1]
				url2='http://www.tagesschau.de'+href
				article_soup=load_url(url2)
				if not os.path.exists(day_now):
				    os.makedirs(day_now)
				with open(day_now+'/'+filename, "w") as file:
					try:
					    file.write(str(article_soup))
					except:
						print('----fehler-----')

				df_all_article.to_excel('list_of_all_Article.xlsx')
