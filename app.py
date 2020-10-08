class storage():
    def __init__(self):
        # CONNECTION INFO
        self.db = ""
        self.user = ""
        self.passwd = ""

class database():
    def __init__(self):
        import cx_Oracle
        self.cx_Oracle = cx_Oracle
        self.storage = storage()
        self.connect = self.cx_Oracle.connect(self.storage.user, self.storage.passwd, self.storage.db)
        print("DB CONNECT")

    def read(self, locate):
        try:
            cursor = self.connect.cursor()
            row = cursor.execute("SELECT * from coronamap where locate="+locate).fetchmany()
            print("DB GET")
            cursor.close()
            return row
        except self.cx_Oracle.DatabaseError as exception:
            print("Failed to run sql.\n"+exception)
            return -1

    def close(self):
        self.connect.close()

class server():
    def __init__(self):
        pass
    
    def checkbox(self):
        row = database().read("01")
        tmp = '<form method="post" name="users">\n'
        i = 0
        while True:
            if i == len(row):
                tmp += '</form>'
                break
            tmp += '<input name="user" type="checkbox" value="'+str(i)+'" onclick="go()">'+str(i)+'번 확진자<p />'
            i += 1

        return tmp


from flask import *
from flask_compress import Compress
import os

compress = Compress()
app = Flask(__name__)
app.secret_key = os.urandom(12)

@app.route('/get')
def coronaget():
    
    return server().checkbox()

@app.route('/')
def main():
    return "It Works!"

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", threaded=True, port=10826)