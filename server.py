from flask import Flask,render_template,jsonify,make_response,abort,request
from flask_httpauth import HTTPDigestAuth
import datetime
import peewee
import base64
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'matsusakaEDPcenter'
auth = HTTPDigestAuth()
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

# API用DB接続クラス
db=None
if os.path.exists('/tmp'):
    db = peewee.SqliteDatabase("/tmp/data.db")
elif os.path.exists('c:\\temp'):
    db = peewee.SqliteDatabase("c:\\temp\\data.db")

# 換気情報データクラス
class VentilationInfo(peewee.Model):
    recdate = peewee.DateTimeField()
    temperature = peewee.FloatField()
    humidity = peewee.FloatField()
    numOfPeople = peewee.IntegerField()
    images = peewee.TextField()

    class Meta:
        database = db

db.create_tables([VentilationInfo])


users = {
    "user": "password",
}

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None


# API実装
# データ取得API
@app.route('/getVentilation/<int:numOfRecord>', methods=['GET'])
def get_Ventilations(numOfRecord):
    try:
        ventilist = VentilationInfo.select().order_by(VentilationInfo.recdate)
    except VentilationInfo.DoesNotExist:
        abort(404)
    dataset1 = {
        'label':'気温',
        'backgroundColor':'rgba(75,192,192,0.4)',
        'borderColor':'rgba(75,192,192,1)',
        'data':[]
    }
    dataset2 = {
        'label':'湿度',
        'backgroundColor':'rgba(192,75,192,0.4)',
        'borderColor':'rgba(192,75,192,1)',        
        'data':[]
    }
    dataset3 = {
        'label':'人数',
        'backgroundColor':'rgba(192,192,75,0.4)',
        'borderColor':'rgba(192,192,75,1)',        
        'data':[]
    }
    labels = []
    for v in ventilist:
        key=v.recdate.strftime('%Y-%m-%D %H:%M:%S')
        labels.append(key)
        dataset1['data'].append(v.temperature)
        dataset2['data'].append(v.humidity)
        dataset3['data'].append(v.numOfPeople*10)
        
    result = {"labels":labels,"datasets":[dataset1,dataset2,dataset3]}
    return make_response(jsonify(result))

# データ登録API
@app.route('/addVentilation/', methods=['POST'])
def add_Ventilation():
    result="ok"
    try:
        d = datetime.datetime.now()
        jsonData = request.json
        t = jsonData.get("temperature")
        h = jsonData.get("humidity")
        p = jsonData.get("numOfpeople")
        g = jsonData.get("image").encode('utf-8')

        print("{} t:{} h:{} p:{} g:{}".format(d,t,h,p,len(g)))
        v = VentilationInfo(recdate=d,temperature=t,humidity=h,numOfPeople=p,images=g)
        v.save()
    except Exception as e:
        print(e)
        result="ng"
    return result

# APIエラー
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

#####################################################################
# ページ遷移
@app.route('/')
def index():
    idx=0
    h=0
    t=0
    p=0

    try:
        ventilist = VentilationInfo.select().order_by(VentilationInfo.recdate.desc()).limit(1)
    except VentilationInfo.DoesNotExist:
        abort(404)
    if len(ventilist) > 0:
        v = ventilist[0]
        idx=int(v.numOfPeople/10*100)
        h=v.humidity
        t=v.temperature
        p=v.numOfPeople
    if v.humidity > 50:
        idx += (v.humidity - 50)

    return render_template('index.html',
            idx=idx,
            temperature=t,
            humidity=h,
            person=p)

@app.route('/graph')
def graph():
    return render_template('graph.html')

@app.route('/images')
@auth.login_required
def images():
    try:
        ventilist = VentilationInfo.select().order_by(VentilationInfo.recdate.desc()).limit(10)
    except VentilationInfo.DoesNotExist:
        abort(404)

    return render_template('images.html',images=ventilist)

@app.route('/help')
def help():
    return render_template('help.html')
#####################################################################

# サービス起動
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
