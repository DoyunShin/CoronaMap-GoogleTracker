#-*- coding:utf-8 -*-
class storage():
    def __init__(self):
        # CONNECTION INFO
        self.db = "tdb0_tpurgent"
        self.user = "comseba0"
        self.passwd = "zjaTpqkepdlxjqpdltm1!"

class database():
    def __init__(self):
        import cx_Oracle
        self.cx_Oracle = cx_Oracle
        self.storage = storage()
        self.connect = self.cx_Oracle.connect(self.storage.user, self.storage.passwd, self.storage.db)
        self.cursor = self.connect.cursor()
        print("DB CONNECT")

    def read(self, locate):
        try:
            return self.cursor.execute("select count(distinct userid) from COMSEBA0.CORONAMAP where INFECTION=1 and locate="+locate).fetchmany()[0][0]
        except self.cx_Oracle.DatabaseError as exception:
            print(exception)
            print("failed to extract")
            return []
    
    def readid(self, userid):
        sql = "SELECT USERID, CENTERLATE7, CENTERLNGE7, STARTTIMESTAMPMS, ENDTIMESTAMPMS from COMSEBA0.CORONAMAPDT where userid='{userid}'".format(userid=userid)
        return self.cursor.execute(sql).fetchmany()

    def readinf(self):
        sql = "SELECT USERID, CENTERLATE7, CENTERLNGE7, STARTTIMESTAMPMS, ENDTIMESTAMPMS, INFECTION from COMSEBA0.CORONAMAPDT where INFECTION=1"
        return self.cursor.execute(sql).fetchmany()


    def readall(self):
        sql = "SELECT USERID, CENTERLATE7, CENTERLNGE7, STARTTIMESTAMPMS, ENDTIMESTAMPMS, INFECTION from COMSEBA0.CORONAMAPDT"
        return self.cursor.execute(sql).fetchmany()

    def readcheck(self, lat, lng, timestamp, rg):
        sql = "select * from CORONAMAPDT where CENTERLATE7 between :1 and :2 and CENTERLNGE7 between :3 and :4 and STARTTIMESTAMPMS <= :5 and INFECTION=1"
        try:
            return self.cursor.execute(sql, (lat-rg, lat+rg, lng-rg, lng+rg, timestamp)).fetchmany()
        except self.cx_Oracle.DatabaseError as exception:
            print(exception)
            print("failed to extract")
            return []

    def putalljson(self, userid, jsondata, locate, infection):
        from json import dumps
        sql = "INSERT INTO COMSEBA0.CORONAMAP (USERID, JSON_DATA, LOCATE, INFECTION) VALUES (:USERID, :JSON_DATA, :LOCATE, :INFECTION)"
        self.cursor.execute(sql, (userid, dumps(jsondata), locate, infection))
    
    def putplace(self, userid, centerLatE7, centerLngE7, startTimestampMs, endTimestampMs, infection):
        sql = "INSERT INTO COMSEBA0.CORONAMAPDT (USERID, CENTERLATE7, CENTERLNGE7, STARTTIMESTAMPMS, ENDTIMESTAMPMS, INFECTION) VALUES (:USERID, :CENTERLATE7, :CENTERLNGE7, :STARTTIMESTAMPMS, :ENDTIEMSTAMPMS, :INFECTION)"
        self.cursor.execute(sql, (userid, centerLatE7, centerLngE7, startTimestampMs, endTimestampMs, infection))
        
    def cursorrefresh(self):
        self.cursor.close()
        self.cursor = None
        self.cursor = self.connect.cursor()

    #def coronausers(self):
    #    sql = "select count(distinct userid) from COMSEBA0.CORONAMAP where INFECTION=1"
    #    return str(self.cursor.execute(sql).fetchmany()[0][0])

    def commit(self): self.connect.commit()
    def close(self): self.connect.close()

class htmledit():
    def __init__(self):
        self.content = 0
        self.marker = 0
        self.flightPath = 0
        self.mk = ""

    def start(self, lat, lng):
        self.mk = str('<!DOCTYPE html><html><head><meta name="viewport" content="initial-scale=1.0, user-scalable=no"><meta charset="utf-8"><title>Simple Polylines</title><style>#map {height: 100%;}html, body {height: 100%;margin: 0;padding: 0;}</style></head><body>')
        self.mk += str("<div id='map'></div><script> function initMap() "+'{'+"\n  var map = new google.maps.Map(document.getElementById('map'), "+'{'+"zoom: 15,center: "+'{'+"lat: 37.4539125, lng: 126.6972400}}); \n")
        pass
    
    def infocont(self, content, title):
        cont = '<div id="content"><div id="siteNotice"><h1 id="firstHeading" class="firstHeading">{title}</h1></div><p/><div id="bodyContent"><p/>{content}</div></div>'.format(title=title,content=content)
        self.mk += "  var contentString{num} = '{cont}'; var infowindow{num} = new google.maps.InfoWindow(".format(num=str(self.content),cont=cont)+'{'+"content: contentString"+str(self.content)+"}); \n"
        self.content += 1
        return "infowindow"+str(self.content-1)

    def infocontobj(self, title,date,intime,outtime,lat,lng):
        cont = '<div id="content"><div id="siteNotice"><h1 id="firstHeading" class="firstHeading">{title}</h1></div><p/><div id="bodyContent"><p><b>{title}</b></p>방문 일시: {date}<p/>들어온 시간: {intime}<p/>나간 시간: {outtime}<p/><p/>위치정보: {lat}, {lng}</div></div>'.format(title=title,date=date,intime=intime,outtime=outtime,lng=lng,lat=lat)
        self.mk += "  var contentString{num} = '{cont}'; var infowindow{num} = new google.maps.InfoWindow(".format(num=str(self.content),cont=cont)+'{'+"content: contentString"+str(self.content)+"}); \n"
        self.content += 1
        return "infowindow"+str(self.content-1)

    def infocontobjuser(self, title,date,intime,count,lat,lng):
        cont = '<div id="content"><div id="siteNotice"><h1 id="firstHeading" class="firstHeading">{title}</h1></div><p/><div id="bodyContent"><p><b>{title}</b></p>방문 일시: {date}<p/>시작 시간: {intime}<p/><p/>위치정보: {lat}, {lng}<p/>확진자와 겹친 동선: {count}개</div></div>'.format(title=title,date=date,intime=intime,count=count,lat=lat,lng=lng)
        self.mk += "  var contentString{num} = '{cont}'; var infowindow{num} = new google.maps.InfoWindow(".format(num=str(self.content),cont=cont)+'{'+"content: contentString"+str(self.content)+"}); \n"
        self.content += 1
        return "infowindow"+str(self.content-1)

    def markeradd(self, lat, lng, title):
        if title == "사용자":
            self.mk += "  var marker"+str(self.marker)+" = new google.maps.Marker("+'{'+"position: "+'{'+"lat: "+str(int(lat)/10000000)+", lng: "+str(int(lng)/10000000)+"}, map: map, title: '"+title+"'}); \n"
        else:
            self.mk += "  var marker"+str(self.marker)+" = new google.maps.Marker("+'{'+"position: "+'{'+"lat: "+str(int(lat)/10000000)+", lng: "+str(int(lng)/10000000)+"}, map: map, title: '"+title+"', icon: 'https://developers.google.com/maps/documentation/javascript/examples/full/images/library_maps.png'}); \n"
        self.marker += 1
        return "marker"+str(self.marker-1)

    def attachinfomark(self, marker, info):
        self.mk += marker+".addListener('click', function() "+'{'+info+".open(map, "+marker+");});"
        #  marker.addListener('click', function() {infowindow.open(map, marker);});
        pass

    def path(self, lat, lng, rang):
        self.mk += "  var flightPlanCoordinates"+str(self.flightPath)+" = [{lat: "+str((lat-rang)/10000000)+", lng: "+str((lng-rang)/10000000)+"},{lat: "+str((lat-rang)/10000000)+", lng: "+str((lng+rang)/10000000)+"},{lat: "+str((lat+rang)/10000000)+", lng: "+str((lng+rang)/10000000)+"},{lat: "+str((lat+rang)/10000000)+", lng: "+str((lng-rang)/10000000)+"},{lat: "+str((lat-rang)/10000000)+", lng: "+str((lng-rang)/10000000)+"}];   var flightPath"+str(self.flightPath)+" = new google.maps.Polyline({path: flightPlanCoordinates"+str(self.flightPath)+",geodesic: true,strokeColor: '#FF0000',strokeOpacity: 1.0,strokeWeight: 2}); flightPath"+str(self.flightPath)+".setMap(map);"
        self.flightPath += 1

    def checkbox(self, users):
        tmp = '<form method="post" name="users">'
        i = 0
        while True:
            if i == users:
                tmp += '</form>'
                break
            tmp += '<input name="user" type="checkbox" value"'+str(i)+'" onclick="go()">'+str(i+1)+'번 확진자<p/>'
            i += 1

        tmp += '</form>'
        return tmp

    def close(self):
        self.mk += 'flightPath.setMap(map);\n}\n </script><script async defer src="https://maps.googleapis.com/maps/api/js?key=AIzaSyBIFkHPa-wnmhvFnakxqoD7FRo2qyyOuaQ&callback=initMap"> </script></body></html>'
        return self.mk

class server():
    def __init__(self, database):
        self.database = database
        pass
    
    def checkbox(self): return htmledit().checkbox(users=self.database.read("01"))

    def parse(self, json):
        main = json["timelineObjects"]
        rtn = []
        i = 0
        while True:
            if i == len(main):
                break
            elif "activitySegment" in main[i]:
                pass
                #rtn.append(self.activitySegment(main[i]["activitySegment"]))
            elif "placeVisit" in main[i]:
                rtn.append(self.placeVisit(main[i]["placeVisit"]))
            
            i += 1
        
        return rtn

    def activitySegment(self, json): return {"type": "activitySegment", "location": {"start": [json["startLocation"]["latitudeE7"], json["startLocation"]["longitudeE7"]], "end": [json["endLocation"]["latitudeE7"], json["endLocation"]["longitudeE7"]]},"time": [json["timestamp"]["startTimestampMs"],json["timestamp"]["endTimestampMs"]],"distance": json["distance"],"activityType": json["activityType"],"mid": json["simplifiedRawPath"]["points"],"parking": json["parkingEvent"]}
    def placeVisit(self, json): return {"type": "placeVisit","location": [json["centerLatE7"], json["centerLngE7"]],"timestamp": [json["duration"]["startTimestampMs"], json["duration"]["endTimestampMs"]]}

    def tsconv(self, timestamp):
        import time
        timestamp = int(timestamp)/1000
        return [time.strftime('%Y년%m월%d일', time.gmtime(timestamp)), time.strftime('%H시%M분%S초', time.gmtime(timestamp))]

    def tsconva(self, timestamp):
        import time
        timestamp = int(timestamp)/1000
        return str(time.strftime('%Y%m', time.gmtime(timestamp)))

    def encode(self, input): 
        import hashlib
        return hashlib.sha256(input.encode()).hexdigest()

    def put(self, json):
        userid = self.encode(json["username"]+json["birthday"])
        jsondata = json["JSON_DATA"]
        locate = json["locate"]
        infection = json["infection"]

        self.database.putalljson(userid, jsondata, locate, infection)
        rtn = self.parse(jsondata)
        
        i = 0
        while True:
            if i == len(rtn):
                break
            now = rtn[i]
            self.database.putplace(userid, now["location"][0], now["location"][1], now["timestamp"][0], now["timestamp"][1], infection)
            i += 1
        
        self.database.commit()
        return "ok"

    #def check(self, json):
    #    #clientid = json["clientid"]
    #    self.chkinf(self.parse(json["jsondata"]))
    #    print(l)
    #    return l
    #    pass

    #def chkinf(self, data):
    #    i = 0
    #    l = []
    #    while True:
    #        if i == len(data):
    #            break
    #        now = rtn[i]
    #        tmp = self.database.readcheck(now["location"][0], now["location"][1], now["timestamp"][0], 10000)
    #        if tmp == []:
    #            pass
    #        else:
    #            l.append({"information": {"lat": now["location"][0], "lng": now["location"][1], "timestamp": now["timestamp"][0]},"status": tmp})
    #    
    #    return l

    #def rtncompas(self, who): 
    #    from json import loads
    #    row = database.read("01")
    #    i = 0
    #    while True:
    #        if i == len(who)-1:
    #            break
    #            pass
    #        
    #        i += 1
    #    pass
    
    def gjson(self, arg):
        data = database.readid(arg["userid"])
        i = 0
        lat = 0
        lng = 0
        while True:
            if i == len(data): 
                lat = str(lat/(i+1)/10000000)
                lng = str(lng/(i+1)/10000000)
                break
            lat += data[i][1]
            lng += data[i][2]
            i += 1
        html = htmledit()
        html.start(lat=lat, lng=lng)
        i = 0
        while True:
            if i == len(data): return html.close()
            arg = {"lat": data[i][1], "lng": data[i][2], "timestamp": data[i][4]}
            self.htmleditor(arg=arg, html=html)
            i += 1
            

    def htrtn(self, arg):
        if "mode" in arg:
            if arg["mode"] == "gjson":
                return self.gjson(arg)
            else: pass
        html = htmledit()
        html.start(lat=str(int(arg["lat"])/10000000), lng=str(int(arg["lng"])/10000000))
        self.htmleditor(arg=arg, html=html)
        return html.close()
            

    def htmleditor(self, arg, html):
        data = {"information": {"lat": arg["lat"], "lng": arg["lng"], "timestamp": arg["timestamp"]},"status": database.readcheck(lat=int(arg["lat"]),lng=int(arg["lng"]),timestamp=int(arg["timestamp"]),rg=10000)}
        datetime = self.tsconv(arg["timestamp"])
        userinfo = html.infocontobjuser(title="사용자 위치",date=datetime[0],intime=datetime[1],count=len(data["status"]),lat=data["information"]["lat"],lng=data["information"]["lng"])
        usermark = html.markeradd(lat=data["information"]["lat"],lng=data["information"]["lng"],title="사용자")
        html.attachinfomark(marker=usermark,info=userinfo)
        i = 0
        now = data["status"]
        while True:
            if i == len(now): break
            if now[i][5] == 1: 
                datetime = self.tsconv(now[i][3])
                datetimea = self.tsconv(now[i][4])
                if datetime[0] != datetimea[0]: datetime[0] = datetime[0]+" ~ "+datetimea[0]
                mark = html.markeradd(lat=now[i][1],lng=now[i][2],title="확진자 위치 "+str(i+1))
                info = html.infocontobj(title="확진자 위치 "+str(i+1),date=datetime[0],intime=datetime[1],outtime=datetimea[1],lat=now[i][1],lng=now[i][2])
                html.path(lat=now[i][1], lng=now[i][2], rang=10000)
                html.attachinfomark(marker=mark,info=info)
            i += 1

    def inf(self):
        html = htmledit()
        html.start(lat=0,lng=0)
        now = self.database.readinf()
        i = 0
        while True:
            if i == len(now): return html.close()
            datetime = self.tsconv(now[i][3])
            datetimea = self.tsconv(now[i][4])
            if datetime[0] != datetimea[0]: datetime[0] = datetime[0]+" ~ "+datetimea[0]
            mark = html.markeradd(lat=now[i][1],lng=now[i][2],title="확진자 위치 "+str(i+1))
            info = html.infocontobj(title="확진자 위치 "+str(i+1),date=datetime[0],intime=datetime[1],outtime=datetimea[1],lat=now[i][1],lng=now[i][2])
            #html.path(lat=now[i][1], lng=now[i][2], rang=10000)
            html.attachinfomark(marker=mark,info=info)
            i += 1


    def getall(self):
        data = database.readall()
        html = htmledit()
        html.start(lat=0, lng=0)
        i = 0
        while True:
            if i == len(data): return html.close()
            if data[i][5] == 1:
                datetime = self.tsconv(data[i][3])
                datetimea = self.tsconv(data[i][4])
                if datetime[0] != datetimea[0]: datetime[0] = datetime[0]+" ~ "+datetimea[0]
                mark = html.markeradd(lat=data[i][1],lng=data[i][2],title="확진자")
                info = html.infocontobj(title="확진자 위치 "+str(i+1),date=datetime[0],intime=datetime[1],outtime=datetimea[1],lat=data[i][1],lng=data[i][2])
                html.attachinfomark(marker=mark,info=info)
                html.path(lat=data[i][1], lng=data[i][2], rang=10000)
            else:
                datetime = self.tsconv(data[i][3])
                usermark = html.markeradd(lat=data[i][1],lng=data[i][2],title="사용자")
                userinfo = html.infocontobjuser(title="사용자 위치",date=datetime[0],intime=datetime[1],count=0,lat=data[i][1],lng=data[i][2])
                html.attachinfomark(marker=usermark,info=userinfo)
            i += 1
        pass

# title,date,intime,outtime,count

from flask import *
from flask_compress import Compress
import os

compress = Compress()
app = Flask(__name__)
app.secret_key = os.urandom(12)
database = database()


@app.route('/get')
def coronaget():
    return server(database).checkbox()

@app.route('/gp')
def comp():
    
    pass

@app.route('/put', methods=['POST'])
def put():
    if request.json == None: 
        a = request.form
        from json import loads
        json = {"username": a["username"], "birthday": a["birthdayy"]+a["birthdaym"]+a["birthdayd"], "JSON_DATA": loads(a["jsondata"]), "infection": int(a["infection"]), "locate": a["locate"]}
    else:
        json = request.json
    return server(database).put(json)

@app.route('/')
def main():
    return "It Works!"

@app.route('/check', methods=['GET'])
def check(): return server(database).htrtn(arg=request.args)

@app.route('/check', methods=['POST'])
def checkpost():
    a = request.form
    t = server(database)
    json = {"mode": "gjson", "userid": t.encode(a["username"]+a["birthdayy"]+a["birthdaym"]+a["birthdayd"])}
    
    return t.htrtn(arg=json)

@app.route('/tmp')
def getc(): return server(database).htrtn(arg=request.args)

@app.route('/infection')
def infection(): return server(database).inf()

@app.route('/test')
def testac():
    database.cursorrefresh()

    return server(database).getall()


    arg = request.args
    #if "lat" in arg:
    #    print("\n\n")
    #    print(database.readcheck(lat=int(arg["lat"]),lng=int(arg["lng"]),timestamp=int(arg["timestamp"]),rg=10000))
    #    print("\n\n")
    #    return str(database.readcheck(lat=int(arg["lat"]),lng=int(arg["lng"]),timestamp=int(arg["timestamp"]),rg=10000))
    #else: return "Something Went wrong"
    tmp = database.readcheck(lat=int(arg["lat"]),lng=int(arg["lng"]),timestamp=int(arg["timestamp"]),rg=10000)
    if tmp == []:
        pass
    else:
        return {"information": {"lat": arg["lat"], "lng": arg["lng"], "timestamp": arg["timestamp"]},"status": tmp}

    return "NO ATTRIB"
    pass


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", threaded=True, port=10826)
    
    #exit
    database.close()