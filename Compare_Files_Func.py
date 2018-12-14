import glob
import os
from bs4 import BeautifulSoup
import difflib

def Compare(path,name,version1,version2):
    textbausteine1=get_Textbausteine(path,name,version1)
    textbausteine2=get_Textbausteine(path,name,version2)
    idiff=0
    for d in difflib.context_diff(textbausteine1,textbausteine2,n=0):
        print(d)
        idiff+=1
    print(idiff)

def get_Textbausteine(path,name,version):
    f=open(path+'/'+str(version)+'_'+name)
    sauce=f.read()
    f.close()
    soupe=BeautifulSoup(sauce, 'lxml')
    body=soupe.body
    stand=body.find('span', class_='stand').text
    content=body.find(id='content')
    section=content.find('div',class_='sectionZ')
    ssection=section.find('div',class_='modParagraph')
    textbausteine=ssection.find_all('p',class_='text')
    h2s=content.find_all('h2', class_='subtitle')
    head=soupe.head
    browsertitle=head.title.text
    headline=body.find('span', class_='headline').text
    dachzeile=body.find('span', class_='dachzeile').text	
    stand=body.find('span', class_='stand').text	
    for i in range(len(textbausteine)):
    	if textbausteine[i].find('a'):
    		if '#comment-' in textbausteine[i].find('a')['href']:
    			del textbausteine[i]
    textbausteine=[t.text for t in textbausteine]+[h.text for h in h2s]+[browsertitle,headline,dachzeile,stand]
    return textbausteine

path='2018-11/20-jahre-iss-101.html'
name='20-jahre-iss-101.html'
version1=0
version2=1
Compare(path,name,version1,version2)