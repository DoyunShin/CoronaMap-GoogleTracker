#class storage():
#    def __init__(self):
#        # CONNECTION INFO
#        self.db = "tdb0_low"
#        self.user = "comseba0"
#        self.passwd = "zjaTpqkepdlxjqpdltm1!"
#
#
#class database():
#    def __init__(self):
#        import cx_Oracle
#        self.cx_Oracle = cx_Oracle
#        self.storage = storage()
#        self.connect = self.cx_Oracle.connect(self.storage.user, self.storage.passwd, self.storage.db)
#
#    def read(self, locate):
#        try:
#            cursor = self.connect.cursor()
#            row = cursor.execute("SELECT * from coronamap where locate="+locate).fetchmany()
#            cursor.close()
#            return row
#        except self.cx_Oracle.DatabaseError as exception:
#            print("Failed to run sql.\n"+exception)
#            return -1
#
#    def close(self):
#        self.connect.close()
#            
#
#class server():
#    def __init__(self):
#        pass
#    
#    def checkbox(self):
#        row = database().read("01")
#        tmp = '<form method="post" name="users">\n'
#        i = 0
#        while True:
#            if i == len(row):
#                tmp += '</form>'
#                break
#            tmp += '<input name="user" type="checkbox" value="'+str(i)+'" onclick="go()">'+str(i)+'번 확진자<p />'
#
#        return tmp

from flask import Flask, render_template, request
from flask_compress import Compress
import json
import os

app = Flask(__name__)



@app.route('/corona/get')
def coronaget():
    from requests import get
    return get("http://127.0.0.1:10826/get")
    
    #return server().checkbox()

@app.route('/corona/put', methods=['POST'])
def coronaput():
    from requests import post
    post("http://127.0.0.1:10826/put", json=request.json)

@app.route('/corona')
def corona():
    return "It Works!"

#@app.route('/corona/get', methods=['GET'])
#def coronashow():
#    json_data = json.loads(request.json)
#    srv = server()
#    return rtn
#