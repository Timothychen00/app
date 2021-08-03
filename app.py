from flask import Flask,render_template,redirect,request,session,flash
import os,pymongo,time
from flask_login import LoginManager
from user.models import User
#pip3 install 'pymongo[srv]'
#/Applications/Python\ 3.6/Install\ Certificates.command
#建立app物件
app=Flask(__name__)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Access denied.'
login_manager.init_app(app)

client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.jyp4y.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.herokuweb
collection=db.users
#密鑰 csrf,session,login
app.secret_key=os.urandom(16).hex()
# session["user_list"]=[]


#flask login_manager
@login_manager.user_loader
def load_user(user_id):
    if collection.find_one({'_id':user_id}) is not None:
        curr_user = User()
        curr_user.id = user_id
        return curr_user

#import user routes
import user.routes

#首頁
@app.route("/")
def home():
    return render_template("base.html",page="home")



@app.route("/successful")
def seccessful():
    return "成功註冊"

#最新消息頁面
@app.route("/newest")
def newest():
    return render_template("newest.html",page="newest")
#活動資訊頁面
@app.route("/activities")
def activities():
    return render_template("activities.html",page="activities")
#加入我們頁面
@app.route("/join")
def join():
    return render_template("join.html",page="join")






if __name__=="__main__":
    app.run(debug=True)