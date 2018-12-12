import glob
import os
from bs4 import BeautifulSoup
import difflib
#import webbrowser
import MySQLdb

os.chdir('//RASPBERRYPI/PiShare/CheckTagesschau/sharefolder/')


class article:
	def __init__(ID,name,pfad):
		self.ID=ID
		self.name=name
		self.pfad=pfad


connection = MySQLdb.connect(
     host="192.168.2.100",
     port=3307,
     db="Tagesschau",
     user="Tagesschau", passwd="g00gle"
    )

c=connection.cursor()

c.execute('SELECT `ID`,`Name`,`RockPfad` FROM `Uebersicht`')
	table_rows = c.fetchall()
	table_rows=list(table_rows)
	for row in table_rows[1:]:
		ID,name,pfad=row