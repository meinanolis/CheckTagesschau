import glob
import os
from bs4 import BeautifulSoup
import difflib
import MySQLdb
import numpy as np
import webbrowser
import os.path

connection = MySQLdb.connect(
     host="192.168.2.3",
     port=3307,
     db="Tagesschau",
     user="Tagesschau", passwd="g00gle"
    )

f=open('Compared_File_Overview.html','w')
f.write('<html><head><style>tr.uncorr {display: none;} td.error {background-color:black; color:white} td.corr {background-color:red; color:black} td.uncorr {background-color:lightgreen; color:black}</style></head><body><table border=1>\n')

c=connection.cursor()
c.execute('SELECT `ID`,`1`,`2`,`3`,`4`,`5`,`6` FROM Vergleich')
table_rows = c.fetchall()
table_rows=list(table_rows)
for row in table_rows:
    ID,c1,c2,c3,c4,c5,c6=row
    cs=np.array([c1,c2,c3,c4,c5,c6])
    c.execute('SELECT `Name`,`RockPfad` FROM `Uebersicht` WHERE `ID`='+str(ID))
    table_rows = c.fetchall()
    table_rows=list(table_rows)
    name, path = table_rows[0]
    tr_class=''
    if (cs==888).any():
        tr_class+=' corr'
    if (cs==999).any():
        tr_class+=' error'
    if (cs==0).all():
        tr_class='uncorr'   
    f.write('<tr class="'+tr_class+'" id="'+str(ID)+'"><td class="index">'+str(ID)+'</td><td class="name">'+name+'</td>')
    for i,cell in enumerate(cs): 
        if (cell==888):
            td_class='corr'
        elif (cell==999):
            td_class='error'
        elif (cell==0):
            td_class='uncorr' 
        else:
            td_class='' 
        if (cell==888):
            f.write('<td class="c'+str(i+1)+' '+td_class+'"><a href="file://blackrock/Tagesschau/'+path+'/diff_'+str(i)+'-'+str(i+1)+'.html" target="inhalt">'+str(cell)+'</a></td>')
        else:
            f.write('<td class="c'+str(i+1)+' '+td_class+'">'+str(cell)+'</td>')
    f.write('</tr>')
f.write('</table></body></html>')
f.close()