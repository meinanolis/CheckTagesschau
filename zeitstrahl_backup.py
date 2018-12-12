import os
#os.chdir('/home/pi/share/CheckTagesschau/sharefolder')
os.chdir('//BLACKROCK/Tagesschau')
#import requests
#from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from time import localtime, strftime
import re
#import matplotlib
## Force matplotlib to not use any Xwindows backend.
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime
import mpld3



day_now=strftime("%Y-%m-%d", localtime())
month_now=strftime("%Y-%m", localtime())




df=pd.read_excel(month_now+'/list_of_all_Article.xlsx')
print(df.columns)
alle_positionen=df['position'].values
alle_zeiten=df['startseite'].values
alle_titel=df['link'].values
fig, ax = plt.subplots(figsize=(30,10))
for pos,zeit,titel in zip(alle_positionen,alle_zeiten,alle_titel):
	pos=np.array([int(i) for i in re.findall('\d+',pos)])*-1
	zeit=[datetime.strptime(d, '%Y-%m-%d %H:%M:%S') for d in zeit.split(', ')]
	titel=titel.split('/')[-1].split('.')[0][:-4]
	lines=ax.plot_date(zeit,pos,'.-',label=titel)
	ax.text(zeit[0],pos[0],titel,fontsize=10)
ax.grid()
plt.gcf().autofmt_xdate()
plt.tight_layout()
plt.savefig('Zeitstrahl.pdf')
#tooltip = mpld3.plugins.PointLabelTooltip(lines[0])
#mpld3.plugins.connect(fig, tooltip)
#
#mpld3.show()





