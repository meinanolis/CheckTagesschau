from flask import Flask, flash, redirect, render_template, request, session, abort
import MySQLdb




class menuu:
    nitems=100

    def __init__(self):
        self.lines = None
    
    def get_lines(self):
        self.lines=[{'ID':57, 'Name':'name','c1':0,'c2':123,'c3':0,'c4':0,'c5':0,'c6':0},
                {'ID':59, 'Name':'name','c1':0,'c2':123,'c3':0,'c4':0,'c5':0,'c6':0},
                {'ID':113, 'Name':'name','c1':0,'c2':123,'c3':0,'c4':0,'c5':0,'c6':0},
                {'ID':114, 'Name':'name','c1':0,'c2':123,'c3':0,'c4':0,'c5':0,'c6':0},
                {'ID':115, 'Name':'name','c1':0,'c2':123,'c3':0,'c4':0,'c5':0,'c6':0},
            ]

class dataa:
    bin_dict={
        'Stand':                1,
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

    def __init__(self,ID=5,VERSION=5):
        self.ID = ID
        self.VERSION = VERSION
        self.read_data_from_db() #name path date bin_vec_int
        self.bin_vec_to_dict() #d

    def datenbankabfrage(self,s):
        self.c=self.connection.cursor()
        self.c.execute(s)
        self.table_rows = self.c.fetchall()
        self.table_rows=list(self.table_rows)
        return self.table_rows

    def datenbankupdate(self,s):
        self.c=self.connection.cursor()
        self.c.execute(s)
        self.connection.commit()

    def dict_to_bin_vec(self, form_dict):
        self.bin_vec_int=0
        for k in form_dict:
            if not (k=='ID' or k=='VERSION'):
                self.bin_vec_int+=self.bin_dict[k]
        return self.bin_vec_int

    def bin_vec_to_dict(self):
        if self.bin_vec_int == 888:
            self.bin_vec_int = 0
        self.d={}
        for k,v in list(self.bin_dict.items())[::-1]:
            if self.bin_vec_int >= v:
                self.d[k]=1
                self.bin_vec_int-=v
            else:
                self.d[k]=0
    
    def read_data_from_db(self):
        row=self.datenbankabfrage('SELECT `Name`,`RockPfad`, `Date` FROM `Uebersicht` WHERE `ID`='+str(self.ID))
        self.name, self.path, self.date=row[0]
        row=self.datenbankabfrage('SELECT `'+str(self.VERSION)+'` FROM Vergleich WHERE `ID`='+str(self.ID))
        self.bin_vec_int =int (row[0][0])


#-----------------TODO
def addHTML(data_dict): 
    data_dict['HTML']='bla'
    return data_dict
   
def write_bin_vec_to_db(ID, VERSION, bin_vec_int):
    self.datenbankupdate('UPDATE `Vergleich` SET `'+VERSION+'` = '+str(bin_vec_int)+' WHERE `Vergleich`.`ID` = '+str(ID))
    print('UPDATE `Vergleich` SET `'+VERSION+'` = '+str(bin_vec_int)+' WHERE `Vergleich`.`ID` = '+str(ID))
    return None




#d=read_data_from_db(59, 1)
#print(d)
#quit()

#------------TODO  
def get_random_888():
    ID=111
    VERSION=1
    return ID, VERSION

app = Flask(__name__)
#------------TODO  
@app.route("/")
def index():
    data = dataa()
    menu = menuu()
    if not menu.lines:
        menu.get_lines()
    return render_template('index.html',menu=menu,data=data)

@app.route("/nav")
#def nav():
#    nitems=request.args.get('nitems')
#    #--------TODO
#    lines=
#    return render_template('nav.html',lines=lines)

@app.route("/id/<int:ID>/<int:VERSION>/")
def outer_frame(ID,VERSION):
    data = data(ID,VERSION)
    
    return render_template('outer_frame.html',data_dict=data_dict, d=d)

@app.route("/next/")
def outer_frame_next():
    ID, VERSION = get_random_888()
    data_dict = read_data_from_db(ID, VERSION)
    if data_dict['bin_vec_int'] == 888:
        data_dict['bin_vec_int']=0
    d = bin_vec_to_dict(data_dict['bin_vec_int'])
    data_dict=addHTML(data_dict)
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