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
stats={"apiupdatetime":timestr}
time.sleep(3)
print(timestr)

def updateDataSet():
    '''
    download the dataset only on request and if update was long ago (DELTA_UPDATE_TIME)
    '''
    global data
    global stats
    global lastUpdateTime
    # only update if last update is old
    if (datetime.datetime.now()-lastUpdateTime) > datetime.timedelta(seconds=DELTA_UPDATE_TIME) or data==[]:
        print("update dataset")
        with urllib.request.urlopen(coronasource) as url:
            data = json.loads(url.read().decode())
            lastUpdateTime=datetime.datetime.now()
            stats["apiupdatetime"]=datetime.datetime.now().__str__()
            print("updateDataSet(): " + stats["apiupdatetime"])
    else:
        print("no update due to time delta")
    return data


app = Flask(__name__)
coronasource="https://corona-ampel.gv.at/sites/corona-ampel.gv.at/files/assets/Warnstufen_Corona_Ampel_Gemeinden_aktuell.json"
lastUpdateTime=datetime.datetime.now()-datetime.timedelta(seconds=DELTA_UPDATE_TIME+10)
print("start data update")
updateDataSet()
print("update done: " + stats["apiupdatetime"])
print("flask web app should be running now...")

@app.route('/updatetime')
def updatetime():
    global stats
    #updateDataSet()
    #return "api polled data the last time at: " + self.odcu.last_update_time_str
    print("updatetime done " + stats["apiupdatetime"])
    return ("api polled data the last time at: " + stats["apiupdatetime"])

@app.route('/time')
def time():
    mystr="hi  - it is " + datetime.datetime.now().__str__()
    return mystr

@app.route('/')
def web_root():
    str="""
    <h1>Simple Corona AT json 2 API Wrapper</h1>
    <br>
    some examples:<br>

    <br>http://lein1013.pythonanywhere.com/v1/corona_aut_api/name/Steyr ... {"GKZ":"40201","2020-10-01T19:30:00Z",""Name":"Steyr","Region":"Gemeinde","Warnstufe":"2"}
    <br>http://lein1013.pythonanywhere.com/v1/corona_aut_api/gkz/10308 ... {"GKZ":"3","Stand": "2020-10-01T19:30:00Z","Name":"Nieder\u00f6sterreich","Region":"Bundesland","Warnstufe":"1"}
    <br>http://lein1013.pythonanywhere.com/v1/corona_aut_api/data ... full original dataset from source
    <br>http://lein1013.pythonanywhere.com/v1/corona_aut_api/source ... https://corona-ampel.gv.at/sites/corona-ampel.gv.at/files/assets/Warnstufen_Corona_Ampel_Gemeinden_aktuell.json
    <br>
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
    &nbsp;&nbsp;&nbsp;&nbsp;resource: http://lein1013.pythonanywhere.com/v1/corona_aut_api/name/Enns<br>
    &nbsp;&nbsp;&nbsp;&nbsp;    method: GET<br>
    &nbsp;&nbsp;&nbsp;&nbsp;    scan_interval: 600<br>
    &nbsp;&nbsp;&nbsp;&nbsp;    value_template: '{{value_json.Warnstufe}}'<br>
    &nbsp;&nbsp;&nbsp;&nbsp;    name: "Enns Corona Ampel"<br>
    """
    return str

@app.route('/v1/corona_aut_api/data')
def v1_corona_data():
    updateDataSet()
    return json.dumps(data)

@app.route('/v1/corona_aut_api/source')
def v1_corona_source():
    return coronasource

@app.route('/v1/corona_aut_api/gkz/<gkz>')
def v1_corona_warnlevel_by_gkz(gkz):
    ''' 
    just use the gkz to get the warning level
    '''
    updateDataSet()
    global data
    warnlevelist=data[0]["Warnstufen"]
    for warnlevel in warnlevelist:
        if warnlevel["GKZ"]==str(gkz):
            ret={"Stand":data[0]["Stand"]}
            ret.update(warnlevel)
            return ret 

@app.route('/v1/corona_aut_api/name/<name>')
def v1_corona_warnlevel_by_Name(name):
    ''' 
    just use the name to get the warning level
    '''
    updateDataSet()
    global data
    warnlevelist=data[0]["Warnstufen"]
    for warnlevel in warnlevelist:
        if warnlevel["Name"]==str(name):
            ret={"Stand":data[0]["Stand"]}
            ret.update(warnlevel)
            return ret 
    return "na"