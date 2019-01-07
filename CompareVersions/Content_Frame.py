from flask import Flask, flash, redirect, render_template, request, session, abort
import MySQLdb


app = Flask(__name__)

bin_dict={'Stand':              1,
        'Rechtschreibfehler':   2,
        'Hinzugefuegt':         4,
        'Entfernt':             8,
        'Aenderung30':          16,
        'Aenderung50':          32,
        'Favorit':              64,
        'Error':                128
}

connection = MySQLdb.connect(
     host="192.168.2.3",
     port=3307,
     db="Tagesschau",
     user="Tagesschau", passwd="g00gle"
    )

def datenbankabfrage(s):
    c=connection.cursor()
    c.execute(s)
    table_rows = c.fetchall()
    table_rows=list(table_rows)
    c.close()
    return table_rows

def datenbankupdate(s):
    c=connection.cursor()
    c.execute(s)
    connection.commit()
    c.close()
    return None



def dict_to_bin_vec(form_dict):
    bin_vec_int=0
    for k in form_dict:
        if not (k=='ID' or k=='VERSION'):
            bin_vec_int+=bin_dict[k]
    return bin_vec_int

def bin_vec_to_dict(bin_vec_int):
    d={}
    for k,v in list(bin_dict.items())[::-1]:
        if bin_vec_int >= v:
            d[k]=1
            bin_vec_int-=v
        else:
            d[k]=0
    return d


#------------TODO    
def write_bin_vec_to_db(ID, VERSION, bin_vec_int):
    datenbankupdate('UPDATE `Vergleich` SET `'+VERSION+'` = '+str(bin_vec_int)+' WHERE `Vergleich`.`ID` = '+str(ID))
    print('UPDATE `Vergleich` SET `'+VERSION+'` = '+str(bin_vec_int)+' WHERE `Vergleich`.`ID` = '+str(ID))
    return None

#------------TODO  
def read_data_from_db(ID, VERSION):
    row=datenbankabfrage('SELECT `Name`,`RockPfad`, `Date` FROM `Uebersicht` WHERE `ID`='+str(ID))
    name,path,date=row[0]
    row=datenbankabfrage('SELECT `'+str(VERSION)+'` FROM Vergleich WHERE `ID`='+str(ID))
    bin_vec_int=int(row[0][0])
    data_dict = {
        'ID': ID,
        'VERSION' : VERSION,
        'Name': name,
        'Path': path,
        'Date': date,
        'bin_vec_int': bin_vec_int,
    }
    return data_dict

#d=read_data_from_db(59, 1)
#print(d)
#quit()

#------------TODO  
def get_random_888():
    ID=111
    VERSION=1
    return ID, VERSION


#------------TODO  kann das framing ding werden
@app.route("/")
def hello():
    return "Hello World!"

@app.route("/id/<int:ID>/<int:VERSION>/")
def outer_frame(ID,VERSION):
    data_dict = read_data_from_db(ID,VERSION)
    if data_dict['bin_vec_int'] == 888:
        data_dict['bin_vec_int']=0
    d = bin_vec_to_dict(data_dict['bin_vec_int'])
    print(data_dict)
    return render_template('outer_frame.html',data_dict=data_dict, d=d)

@app.route("/next/")
def outer_frame_next():
    ID, VERSION = get_random_888()
    data_dict = read_data_from_db(ID, VERSION)
    if data_dict['bin_vec_int'] == 888:
        data_dict['bin_vec_int']=0
    d = bin_vec_to_dict(data_dict['bin_vec_int'])
    print(data_dict)
    return render_template('outer_frame.html',data_dict=data_dict, d=d)

@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        ID = result['ID']
        VERSION = result['VERSION']
        bin_vec_int = dict_to_bin_vec(result)
        write_bin_vec_to_db(ID, VERSION, bin_vec_int)
    return 'ok, ID: '+str(ID)+', Version: '+str(VERSION)+', Bin_Vec '+str(bin_vec_int)

if __name__ == "__main__":
    app.run()