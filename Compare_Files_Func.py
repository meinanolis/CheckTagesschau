import glob
import os
from bs4 import BeautifulSoup
import difflib
import MySQLdb
import numpy as np
import webbrowser

connection = MySQLdb.connect(
     host="192.168.2.3",
     port=3307,
     db="Tagesschau",
     user="Tagesschau", passwd="g00gle"
    )


def Compare(path,name,version1,version2):
    textbausteine1=get_Textbausteine(path,name,version1)
    textbausteine2=get_Textbausteine(path,name,version2)
    t1=[t.text for t in textbausteine1]
    t2=[t.text for t in textbausteine2]
    idiff=0
    for d in difflib.context_diff(t1,t2,n=0):
        #print(d)
        idiff+=1
    print(idiff, name)
    if idiff:
        html = difflib.HtmlDiff().make_table(fromlines=t1,tolines=t2)
        soup=BeautifulSoup(html)
        #soup.find('span', class_='diff_chg')['color']='red'
        soup.find('table')['width']='1000'
        soup.find('table')['cellspacing']='10'
        soup.find('table')['cellpadding']='10'
        text=soup.prettify(formatter=lambda s: s.replace(u'\xa0', ' ')).replace('nowrap="nowrap"', 'width="450"')
        text=text.replace('<html>','<html><head><style>span.diff_sub { background-color: red;}\nspan.diff_add {background-color:green;}\nspan.diff_chg {background-color:yellow}</style></head>')
        with open(path+'/diff_'+str(version1)+'-'+str(version2)+'.html', 'w') as f:
            f.write(text)
        #webbrowser.open(url)
        
    return idiff

def get_Textbausteine(path,name,version):
    f=open(path+'/'+str(version)+'_'+name)
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
    return contentlist


def sync_Uebersicht_und_Vergleich():
    c=connection.cursor()

    c.execute('SELECT `ID` FROM `Vergleich`')
    table_rows = c.fetchall()
    table_rows=list(table_rows)
    all_ID_in_Vergleich=[]
    for row in table_rows:
        ID=row[0]
        all_ID_in_Vergleich.append(ID)
    all_ID_in_Vergleich=np.array(all_ID_in_Vergleich)

    c.execute('SELECT `ID`,`Name` FROM `Uebersicht`')
    table_rows = c.fetchall()
    table_rows=list(table_rows)
    for row in table_rows:
        ID, name=row
        if ID not in all_ID_in_Vergleich:
            print(name)
            c.execute("INSERT INTO `Vergleich` (`ID`, `Name`) VALUES ('"+str(ID)+"', '"+name+"');")
            connection.commit()





#sync_Uebersicht_und_Vergleich()
c=connection.cursor()
c.execute('SELECT ID FROM Vergleich WHERE `Vergleich`.`1-2` IS NULL')
table_rows = c.fetchall()
table_rows=list(table_rows)
version1=1
version2=2
for row in table_rows:
    ID=row[0]
    c.execute('SELECT `Name`,`RockPfad` FROM `Uebersicht` WHERE `ID`='+str(ID))
    table_rows = c.fetchall()
    table_rows=list(table_rows)
    name, path = table_rows[0]
    try:
        idiff=Compare(path,name,version1,version2)
    except:
        idiff=999
    c.execute('UPDATE `Vergleich` SET `2-3` = '+str(idiff)+' WHERE `Vergleich`.`ID` = '+str(ID)+';')
    connection.commit()



