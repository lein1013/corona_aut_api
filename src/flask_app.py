# Corona Austria API
# 
from flask import Flask
import urllib.request, json
import time
import datetime

DELTA_UPDATE_TIME=600

data=[]
lastUpdateTime=datetime.datetime.now()
timestr=datetime.datetime.now().__str__()
print(timestr)
stats={"apiupdatetime":timestr}
time.sleep(3)
print(timestr)

def updateDataSet():
    global data
    global stats
    global lastUpdateTime
    #print(datetime.datetime.now().__str__())
    #print(datetime.datetime.now()-lastUpdateTime)
    # only update if last update is old
    if (datetime.datetime.now()-lastUpdateTime) > datetime.timedelta(seconds=DELTA_UPDATE_TIME) or data==[]:
        print("update dataset")
        with urllib.request.urlopen(coronasource) as url:
            data = json.loads(url.read().decode())
            #data=datatmp.copy()
            #print(data)
            lastUpdateTime=datetime.datetime.now()
            stats["apiupdatetime"]=datetime.datetime.now().__str__()
            print("updateDataSet(): " + stats["apiupdatetime"])
    else:
        print("no update due to time delta")
    return data


app = Flask(__name__)
coronasource="https://corona-ampel.gv.at/sites/corona-ampel.gv.at/files/coronadata/CoronaKommissionV2.json"
lastUpdateTime=datetime.datetime.now()-datetime.timedelta(seconds=DELTA_UPDATE_TIME+10)
print("start data update")
#odcu=OpenDataCoronaUpdate()
#print("Wait")
#time.sleep(3)
#print(odcu.data["VersionDate"])
# set pointer
updateDataSet()
#print(data)
print("update done: " + stats["apiupdatetime"])
#app.odcu=odcu
#data=odcu.data
#last_update_time_str=odcu.last_update_time_str
#print(odcu.last_update_time_str)
#print("pointer")
#print(data["VersionDate"])
#odcu.data["Test"]="asdf"
#print(data["Test"])

@app.route('/updatetime')
def updatetime():
    global stats
    #updateDataSet()
    #return "api polled data the last time at: " + self.odcu.last_update_time_str
    print("updatetime done " + stats["apiupdatetime"])
    return ("api polled data the last time at: " + stats["apiupdatetime"])

@app.route('/hi')
def hi():
    mystr="hi  - it is " + datetime.datetime.now().__str__()
    return mystr

@app.route('/')
def web_root():
    str="""
    <h1>Simple Corona AT json 2 API Wrapper</h1>
    <br>
    some examples:<br>

    <br>http://lein1013.pythonanywhere.com/v1/corona_aut_api/warnname/Steyr ... {"Begruendung":"","GKZ":"40201","KW":38,"Name":"Steyr","Region":"Gemeinde","Warnstufe":"2"}
    <br>http://lein1013.pythonanywhere.com/v1/corona_aut_api/warngkz/3 ... {"Begruendung":"","GKZ":"3","KW":38,"Name":"Nieder\u00f6sterreich","Region":"Bundesland","Warnstufe":"1"}
    <br>http://lein1013.pythonanywhere.com/v1/corona_aut_api/data ... full original dataset from source
    <br>http://lein1013.pythonanywhere.com/v1/corona_aut_api/source ... https://corona-ampel.gv.at/sites/corona-ampel.gv.at/files/coronadata/CoronaKommissionV2.json
    <br>
    I've no idea if this dataset is maintained :-) but latest calender week is the current week (while developing)
    """
    return str

@app.route('/v1/corona_aut_api/homeassistant')
def v1_corona_homeassistant():
    str="""
    # turn on a ligth with the related corona ampel color for the selected region<br>
    # change light name and Corona region<br>
automation:<br>
&nbsp;&nbsp;  - alias: 'Corona Ampel'<br>
&nbsp;&nbsp;&nbsp;&nbsp;    trigger:<br>
&nbsp;&nbsp;&nbsp;&nbsp;      platform: time_pattern<br>
&nbsp;&nbsp;&nbsp;&nbsp;      # You can also match on interval. This will match every 5 minutes<br>
&nbsp;&nbsp;&nbsp;&nbsp;      minutes: "/5"<br>
&nbsp;&nbsp;&nbsp;&nbsp;    action:<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;      - service: light.turn_on<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;        data_template:<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;          entity_id: light.pl16<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;          brightness_pct: 30<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;          color_name: ><br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;            {% set map = {'1': 'green', '2': 'yellow', '3': 'orange','4':'red'} %}<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;            {% set state = states('sensor.enns_corona_ampel') %}<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;           {{ map[state] if state in map else 'white' }}<br>

<br>
    # simple homeassistant rest sensor configuration for corona warning system<br>
    sensor:<br>
    &nbsp;&nbsp;  - platform: rest<br>
    &nbsp;&nbsp;&nbsp;&nbsp;resource: http://lein1013.pythonanywhere.com/v1/corona_aut_api/warnname/Enns<br>
    &nbsp;&nbsp;&nbsp;&nbsp;    method: GET<br>
    &nbsp;&nbsp;&nbsp;&nbsp;    scan_interval: 600<br>
    &nbsp;&nbsp;&nbsp;&nbsp;    value_template: '{{value_json.Warnstufe}}'<br>
    &nbsp;&nbsp;&nbsp;&nbsp;    name: "Enns Corona Ampel"<br>
    """
    return str

@app.route('/v1/corona_aut_api/data')
def v1_corona_data():
    updateDataSet()
    #print(data)
    return data

@app.route('/v1/corona_aut_api/versionsnr')
def v1_corona_versionsnr():
    updateDataSet()
    return data["VersionsNr"]

@app.route('/v1/corona_aut_api/source')
def v1_corona_source():
    return coronasource



def getWarnFromGkz(data,gkz):
    warnlist=data["Kalenderwochen"][0]["Warnstufen"]
    for warn in warnlist:
        if warn["GKZ"]==str(gkz):
            return warn
    return "na"

def getRegionFromGkz(data,gkz):
    regionlist=data["Regionen"]
    for region in regionlist:
        if region["GKZ"]==str(gkz):
            return region
    return "na"

@app.route('/v1/corona_aut_api/warngkz/<gkz>')
def v1_corona_warngkz(gkz):
    updateDataSet()
    global data
    ret={"KW":data["Kalenderwochen"][0]["KW"]}
    tmp={"GKZ":gkz}
    ret.update(tmp)
    ret.update(getWarnFromGkz(data,gkz))
    ret.update(getRegionFromGkz(data,gkz))
    return ret

@app.route('/v1/corona_aut_api/warnregionname/<region>/<name>')
def v1_corona_warnregionname(region,name):
    updateDataSet()
    global data
    #return(region) #debug
    regionlist=data["Regionen"]
    #return(regionlist)
    for region in regionlist:
        #if region["Region"]==str(region):
        if region["Name"]==str(name):
            gkz=region["GKZ"]
            print(gkz)
            #return gkz
            return v1_corona_warngkz(gkz)
    return "na"

@app.route('/v1/corona_aut_api/warnname/<name>')
def v1_corona_warnname(name):
    updateDataSet()
    print(name)
    global data
    regionlist=data["Regionen"]
    for region in regionlist:
        if region["Name"]==str(name):
            gkz=region["GKZ"]
            return v1_corona_warngkz(gkz)
    return "na"