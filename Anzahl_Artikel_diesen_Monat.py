#import requests
#from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from time import localtime, strftime
#import re
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime
import glob
import os
os.chdir('/home/pi/share/CheckTagesschau/sharefolder')


day_now=strftime("%Y-%m-%d", localtime())
month_now=strftime("%Y-%m", localtime())

files=glob.glob(month_now+'/**/0_*.html')
print(len(files))

if os.path.isfile(month_now+'/Artikelanzahl.txt'):
	f=open(month_now+'/Artikelanzahl.txt', 'a')
else:
	f=open(month_now+'/Artikelanzahl.txt', 'w')
	f.write('Zeit\tArtikelanzahl\n')

f.write(day_now+'\t'+str(len(files))+'\n')
f.close()


df=pd.read_csv(month_now+'/Artikelanzahl.txt',sep='\t')
alle=df['Artikelanzahl'].values
dates= [datetime.strptime(d, '%Y-%m-%d') for d in df['Zeit'].values]
day= [datetime.strftime(d, '%d') for d in dates]
dates = matplotlib.dates.date2num(dates)

plt.plot_date(dates,alle,'.-')
if len(dates)>7:
	divider=np.round(len(dates)/6)
	plt.xticks(dates[::divider],day[::divider])
else:
	plt.xticks(dates,day)
plt.title('Artikelanzahl')
plt.xlabel('Zeit')
plt.gcf().autofmt_xdate()
plt.tight_layout()
plt.savefig('/opt/fhem/www/images/default/Artikelanzahl.png')
plt.savefig(month_now+'/Artikelanzahl.png')