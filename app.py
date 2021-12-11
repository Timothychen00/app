from flask import Flask,render_template,redirect,request,session,flash
import os,pymongo,datetime
from bson import ObjectId
from user.routes import app_user_routes
from officesys.routes import app_officesys_routes
# from dotenv import load_dotenv
# load_dotenv()

#pip3 install 'pymongo[srv]'
#/Applications/Python\ 3.6/Install\ Certificates.command
#建立app物件
# test1123
client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.m8nzl.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.flaskweb
collection=db.users
#定義主程序
app=Flask(__name__)
app.secret_key=os.urandom(16).hex()#密鑰 csrf,session,login
#session生命週期
app.permanent_session_lifetime=datetime.timedelta(hours=2)

app.register_blueprint(app_user_routes)#用戶系統
app.register_blueprint(app_officesys_routes)#辦公系統

@app.before_first_request
def do_something():
    flash('這個一個新版本')

@app.route('/announcement/<id>/')
def home_each(id):
    collection=db.announcement#操作users集合
    result=collection.find_one(ObjectId(id))
    result['time']=datetime.datetime.strptime(result['time'], "%Y-%m-%d %H:%M:%S")
    result['end-time']=result['time']+datetime.timedelta(days=result['duration'])
    return render_template('/officesys/dashboard-each.html',result=result)

#首頁
@app.route("/")
def home():
    flash(os.environ['DB_URL'])
    session['from']=request.path
    # flash(os.getenv("DB_URL"))
    # flash(os.getenv("SOURCE_CODE_RELEASE_URL"))
    #最新公告
    newest_results=db.announcement.find({'category':'最新公告'})
    newest_results.sort("time",pymongo.DESCENDING)#按照時間降序排列
    newest_results.limit(10)#限制數量
    #隊務公告
    team_results=db.announcement.find({'category':'隊務公告'})
    team_results.sort("time",pymongo.DESCENDING)#按照時間降序排列
    team_results.limit(10)#限制數量
    #招生&招募專區
    recruit_results=db.announcement.find({'category':'招生＆招募專區'})
    recruit_results.sort("time",pymongo.DESCENDING)#按照時間降序排列
    recruit_results.limit(10)#限制數量

    return render_template("base.html",page="home",newest_results=newest_results,team_results=team_results,recruit_results=recruit_results)

#最新消息頁面
@app.route("/news/")
def newest():
    session['from']=request.path
    
    #最新公告
    newest_results=db.announcement.find({'category':'最新公告'})
    newest_results.sort("time",pymongo.DESCENDING)#按照時間降序排列
    newest_results.limit(10)#限制數量
    #隊務公告
    team_results=db.announcement.find({'category':'隊務公告'})
    team_results.sort("time",pymongo.DESCENDING)#按照時間降序排列
    team_results.limit(10)#限制數量
    #招生&招募專區
    recruit_results=db.announcement.find({'category':'招生＆招募專區'})
    recruit_results.sort("time",pymongo.DESCENDING)#按照時間降序排列
    recruit_results.limit(10)#限制數量
    
    return render_template("news.html",page="news",newest_results=newest_results,team_results=team_results,recruit_results=recruit_results)

#活動資訊頁面
@app.route("/activities/")
def activities():
    session['from']=request.path
    return render_template("activities.html",page="activities")

#加入我們頁面
@app.route("/join/")
def join():
    session['from']=request.path
    return render_template("join.html",page="join")

@app.route('/develop/versions/')
def versions():
    return redirect('https://github.com/Timothychen00/app/releases')

if __name__=="__main__":
    app.run(debug=True)