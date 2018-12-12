import os
#os.chdir('/home/pi/share/CheckTagesschau/sharefolder')
os.chdir('//BLACKROCK/Tagesschau')
import pandas as pd
import numpy as np
from time import localtime, strftime
import re
from datetime import datetime
from bokeh.io import  show, save
from bokeh.plotting import output_file, figure
from bokeh.models import ColumnDataSource, HoverTool






day_now=strftime("%Y-%m-%d", localtime())
month_now=strftime("%Y-%m", localtime())




df=pd.read_excel(month_now+'/list_of_all_Article.xlsx')
print(df.columns)
alle_positionen=df['position'].values
alle_zeiten=df['startseite'].values
alle_titel=df['link'].values
data=dict(
	zeit=[],
	pos=[],
	titel=[],
	)
for pos,zeit,titel in zip(alle_positionen,alle_zeiten,alle_titel):
	pos=np.array([int(i) for i in re.findall('\d+',pos)])*-1
	zeit=[datetime.strptime(d, '%Y-%m-%d %H:%M:%S') for d in zeit.split(', ')]
	titel=titel.split('/')[-1].split('.')[0][:-4]
	data['zeit'].append(zeit)
	data['pos'].append(pos)
	data['titel'].append(titel)


source = ColumnDataSource(data)
# create a new plot with default tools, using figure
p = figure(plot_width=1000, plot_height=800)
p.multi_line('zeit', 'pos', line_width=5, line_color='grey', line_alpha=0.6,
             hover_line_color='blue', hover_line_alpha=1.0,
             source=source)
p.add_tools(HoverTool(line_policy='next', tooltips=[
    ('Titel', '@titel')]))

output_file("test.html")
save(p)






