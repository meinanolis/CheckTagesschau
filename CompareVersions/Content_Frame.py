from flask import Flask, flash, redirect, render_template, request, session, abort
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

def dict_to_bin_vec(form_dict):
    bin_vec_int=0
    for k in form_dict:
        if not k=='ID':
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
def write_bin_vec_to_db(ID, bin_vec_int):
    return None

#------------TODO  
def read_data_from_db(ID):
    data_dict = {
        'ID': ID,
        'Name': 'name',
        'Path': 'path',
        'Date': 'date',
        'bin_vec_int': 111
    }
    if data_dict['bin_vec_int'] == 888:
        data_dict['bin_vec_int'] = 0
    return data_dict

#------------TODO  
def get_random_888():
    ID=111
    return ID


#------------TODO  kann das framing ding werden
@app.route("/")
def hello():
    return "Hello World!"

@app.route("/id/<int:ID>/")
def outer_frame(ID):
    data_dict = read_data_from_db(ID)
    d = bin_vec_to_dict(data_dict['bin_vec_int'])
    print(data_dict)
    return render_template('outer_frame.html',data_dict=data_dict, d=d)

@app.route("/next/")
def outer_frame_next():
    ID = get_random_888()
    data_dict = read_data_from_db(ID)
    d = bin_vec_to_dict(data_dict['bin_vec_int'])
    print(data_dict)
    return render_template('outer_frame.html',data_dict=data_dict, d=d)

@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        ID = result['ID']
        bin_vec_int = dict_to_bin_vec(result)
        write_bin_vec_to_db(ID, bin_vec_int)
    return 'ok '+str(ID)+' '+str(bin_vec_int)

if __name__ == "__main__":
    app.run()