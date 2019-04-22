'''
Created on Jul 22, 2018

@author: akashi
'''
from classes.run_commands import run_commands
#from classes import ConnectionHandler
from classes.unix_commands import unix_commands

from flask import Flask, render_template, redirect, request,jsonify,url_for
import random
import json,time
from datetime import datetime
import os  
from os.path import isfile

ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

app = Flask(__name__, template_folder=ASSETS_DIR, static_folder=ASSETS_DIR)


@app.route('/')
def home():    
    print("hi")
    return render_template('index.html')
    

@app.route('/run',methods=['POST'])
def run():
    #return render_template('index.html')
    #command=str(request.form.get('command'))
    commands=request.get_json('name')
    print("here")
    print(commands)
    temp=commands.get('document name',[])
    print (str(temp).strip())
    data = {'string': commands}
    data = jsonify(data)
    #str1="I was here"
    return data
    #print(command)

'''
def newmac():
    return "%02x:%02x:%02x:%02x:%02x:%02x" % (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
        )

def addToUrl(url):
    d=json.load(open("urls.json"))
    d.append(url)
    d=d[-50:]
    json.dump(d, open("urls.json",'w'))

@app.route('/addLoc/<string:new_loc>')
def addLoc(new_loc):
    d=json.load(open("locations.json"))
    d.append(new_loc)
    json.dump(d, open("locations.json",'w'))

@app.route('/redirect', methods=['POST'])
def signup():
    macId=str(request.form.get('mac_id'))
    location=request.form.get('loc')
    redtype=request.form.get('env')    
    if  str(request.form.get('cus')).lower() == "new":
        tratype="n"
    else:     
        tratype="e"    
    url="?macId="+macId.replace(":","%3A")+"&c="+tratype+"&apMacId="+macId.replace(":","%3A")+"&location="+location+"&issuer=r&deviceModel=Samsung+Galaxy+Note4&uiSimulator=false"
    if redtype.lower() == "production":        
        addToUrl("[PROD] [MAC ID: "+macId+"] "+str(datetime.now()).split(".")[0]+": "+"https://wifiondemand.xfinity.com/wod/landing"+url)        
        return redirect("https://wifiondemand.xfinity.com/wod/landing"+url, code=302)
    else:
        addToUrl("[STAGE] [MAC ID: "+macId+"] "+str(datetime.now()).split(".")[0]+": "+"https://wifiondemand-stage.xfinity.com/wod/landing"+url)
        return redirect("https://wifiondemand-stage.xfinity.com/wod/landing"+url, code=302)
        
@app.route('/getmac', methods=['GET'])
def getmac():
    return jsonify({"result": newmac()}), 200 

@app.route('/geturls', methods=['GET'])
def geturls():
    return jsonify({"result": json.load(open("urls.json"))[:-51:-1]}), 200 

'''

if __name__ == '__main__':
    app.debug=True
    app.run(port=1011,host='0.0.0.0')

#Getter and setter for Unix commands
#unix_commands_object=unix_commands()
#unix_commands_object.set_unix_commands()
#commands=unix_commands_object.get_unix_commands()


#run_commands_object=run_commands()
#run_commands_object.run_unix_commands(commands)


