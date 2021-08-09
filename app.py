from flask import Flask,render_template,redirect,request,session,flash
import os,pymongo,datetime
from user.routes import app_user_routes
from officesys.routes import app_officesys_routes
#pip3 install 'pymongo[srv]'
#/Applications/Python\ 3.6/Install\ Certificates.command
#建立app物件

client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.m8nzl.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.flaskweb
collection=db.users
#定義主程序
app=Flask(__name__)
app.secret_key=os.urandom(16).hex()#密鑰 csrf,session,login
app.permanent_session_lifetime=datetime.timedelta(hours=2)

app.register_blueprint(app_user_routes)#用戶系統
app.register_blueprint(app_officesys_routes)#辦公系統

#首頁
@app.route("/")
def home():
    session['from']=request.path
    newest_results=db.announcement.find({'category':'最新公告'})
    newest_results.sort("time",pymongo.DESCENDING)
    teams_results=db.announcement.find({'category':'隊務公告'})
    teams_results.sort("time",pymongo.DESCENDING)
    newest_results=db.announcement.find({'category':'最新公告'})
    newest_results.sort("time",pymongo.DESCENDING)
    return render_template("base.html",page="home",newest_results=newest_results)

#最新消息頁面
@app.route("/newest")
def newest():
    session['from']=request.path
    return render_template("newest.html",page="newest")

#活動資訊頁面
@app.route("/activities")
def activities():
    session['from']=request.path
    return render_template("activities.html",page="activities")

#加入我們頁面
@app.route("/join")
def join():
    session['from']=request.path
    return render_template("join.html",page="join")

if __name__=="__main__":
    app.run(debug=True)