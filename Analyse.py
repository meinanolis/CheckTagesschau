import pandas as pd 
import glob
import numpy as np
import matplotlib.pyplot as plt
import re
from datetime import datetime

if 1: #read all files
	files=glob.glob('*/list_of_all_Article_and_Feature_V1-2.xlsx')
	df=pd.DataFrame([])
	for file in files:
		print(file)
		dftemp=pd.read_excel(file)
		df=pd.concat((df,dftemp))
else:
	df=pd.read_excel('2018-07/list_of_all_Article_and_Feature_V1-2.xlsx')
print(df.columns)
#
if 0: #WortAnzahl
	x=np.array(df['wortAnzahl'].values)
	print(len(x))
	
	plt.hist(x, normed=False, bins=50)
	plt.xlabel('Wörter pro Artikel')
	plt.ylabel('Artikel')
	plt.title('Verteilung der Länge der Artikel')
	plt.savefig('Verteilung der Länge der Artikel.pdf')
	plt.show()

if 0: # Stand
	stand=np.array(df['stand'].values)
	xhour=[]
	xday=[]
	xMonth=[]
	xweekday=[]
	for i in stand:
		dto=datetime.strptime(i, '%Y-%m-%d %H:%M')
		#dto=datetime.strptime(i, 'Stand: %d.%m.%Y %H:%M Uhr')
		xhour.append(dto.hour)
		xday.append(dto.day)
		xMonth.append(dto.month)
		xweekday.append(dto.weekday())
	if 0: #Stunden
		plt.hist(xhour, normed=False, bins=24)
		plt.xlabel('Stunde')
		plt.ylabel('Artikel')
		plt.title('Verteilung der Zeit von Stand')
		plt.savefig('Verteilung der Zeit.pdf')
		plt.show()
	if 0: #Tage
		plt.hist(xday, normed=False, bins=31)
		plt.xlabel('Tag im Monat')
		plt.ylabel('Artikel')
		plt.title('Verteilung der Artikel nach Tagen im Monat')
		plt.savefig('Verteilung Monat.pdf')
		plt.show()
	if 1: #Wochentage
		plt.hist(xweekday, normed=False, bins=7)
		plt.xlabel('Tag in der Woche')
		plt.ylabel('Artikel')
		plt.title('Verteilung der Artikel nach Wochentag')
		plt.savefig('Verteilung Wochentag.pdf')
		plt.show()


if 0: #CDU SPD
		import matplotlib.patches as patches
		CDU=np.array(df['CDU'].values)
		SPD=np.array(df['SPD'].values)
		CDUM=np.sum(CDU)
		SPDM=np.sum(SPD)
		print('CDU',CDUM)
		print('SPD',SPDM)
		fig,ax = plt.subplots(1)
		plt.plot([1,2],[CDUM,SPDM],'o')
		plt.xlim(.5,2.5)
		plt.ylim(0,np.max([CDUM,SPDM])*1.1)
		plt.xticks([1,2],['CDU','SPD'])
		plt.title('Anzahl der Erwähnungen CDU und SPD')
		plt.ylabel('Anzahl der Erwähnungen')
		# Create a Rectangle patch
		rect1 = patches.Rectangle((.7,0),.6,CDUM,linewidth=1,edgecolor='none',facecolor='k')
		rect2 = patches.Rectangle((1.7,0),.6,SPDM,linewidth=1,edgecolor='none',facecolor='r')
		# Add the patch to the Axes
		ax.add_patch(rect1)
		ax.add_patch(rect2)
		plt.show()
if 0: #CDU SPD 2
	nCDU17=np.zeros(12)
	nSPD17=np.zeros(12)
	nCDU18=np.zeros(12)
	nSPD18=np.zeros(12)
	Monatsnamen=np.array(['Jan', 'Feb', 'März', 'Apr', 'Mai', 'Jun','Jul','Aug','Sep','Okt','Nov','Dez'])
	for c,s,d in zip(np.array(df['CDU'].values),np.array(df['SPD'].values),np.array(df['stand'].values)):
		dto=datetime.strptime(d, '%Y-%m-%d %H:%M')
		if dto.year==2017:
			month=dto.month
			nCDU17[month-1]+=c
			nSPD17[month-1]+=s
		else:
			month=dto.month
			nCDU18[month-1]+=c
			nSPD18[month-1]+=s
			(nSPD17+nCDU17)>0
	bool17=(nSPD17+nCDU17)>0
	bool18=(nSPD18+nCDU18)>0
	Monatsnamen17=Monatsnamen[bool17]
	Monatsnamen18=Monatsnamen[bool18]
	Monatsnamen=np.hstack((Monatsnamen17,Monatsnamen18))
	nSPD17=nSPD17[bool17]
	nSPD18=nSPD18[bool18]
	nSPD=np.hstack((nSPD17,nSPD18))
	nCDU17=nCDU17[bool17]
	nCDU18=nCDU18[bool18]
	nCDU=np.hstack((nCDU17,nCDU18))
	n_groups = len(Monatsnamen)
	print(Monatsnamen,nSPD)
	fig, ax = plt.subplots()
	index = np.arange(n_groups)
	bar_width = 0.35
	opacity = 0.9
	rects1 = plt.bar(index, nSPD, bar_width,
	                 alpha=opacity,
	                 color='r',
	                 label='SPD')

	rects2 = plt.bar(index + bar_width, nCDU, bar_width,
	                 alpha=opacity,
	                 color='k',
	                 label='CDU')

	plt.xlabel('Monat')
	plt.ylabel('Erwähnungen')
	plt.title('Anzahl der Erwähnungen CDU und SPD')
	plt.xticks(index + bar_width, Monatsnamen)
	plt.legend()
	plt.tight_layout()
	plt.savefig('Erwähnungen CDU und SPD.pdf')
	plt.show()


if 1: # Keywords
	keywords=np.array(df['tagsDateinamen'].values)
	all_tags=[]
	for k in keywords:
		tags=k[2:-2].split('\', \'')
		all_tags+=tags
	all_tags_unique=np.unique(all_tags)
	tag_freq = np.array([all_tags.count(p) for p in all_tags_unique])
	#a=np.vstack((all_tags_unique,tag_freq))
	df_tag=pd.DataFrame(all_tags_unique,columns=['tag'])
	df_häufigkeit=pd.DataFrame(tag_freq,columns=['häufigkeit'])
	df_key=pd.concat((df_tag,df_häufigkeit), axis=1)
	#print(df_key)
	df_key=df_key.sort_values(by=['häufigkeit'],ascending=False)
	#print(tag_freq)
	n_groups = 50
	fig, ax = plt.subplots()
	index = np.arange(n_groups)[::-1]
	bar_heigth = 0.7
	opacity = 0.9
	bar_width=df_key['häufigkeit'].values[:n_groups]
	print(bar_width)
	rects = plt.barh(index, bar_width, bar_heigth,
	                 alpha=opacity,
	                 color='r')
	plt.xlabel('Häufigkeit')
	plt.ylabel('Keywords')
	plt.title('Anzahl der Erwähnungen von Keywords')
	plt.yticks(index + bar_heigth/2, df_key['tag'].values[:n_groups])
	#plt.legend()
	plt.tight_layout()
	plt.savefig('Keywords.pdf')
	plt.show()

