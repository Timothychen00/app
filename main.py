from flask import Flask,render_template,redirect,request
from forms import RegisterForm,LoginForm
import pymongo
from forms import DashForm
import os
# from wtforms import StringField,PasswordField,SubmitField
# pip3 install email_validator
#建立app物件
app=Flask(__name__)
#密鑰 csrf,session,login
app.secret_key=os.urandom(16).hex()

#首頁
@app.route("/")
def home():
    return render_template("base.html",page="home")

#註冊頁面
@app.route("/register",methods=["GET","POST"])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        data={
            "username":form.username.data,
            "email":form.email.data,
            "password":form.password.data,
            }
        return "<h1>form submitted</h1>"+str(data)
    return render_template("register.html",form=form,page="register")

#登錄頁面
@app.route("/login",methods=["GET","POST"])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        return "成功登錄"
    return render_template("login.html",form=form,page="login")

@app.route("/successful")
def seccessful():
    return "成功註冊"

#最新消息頁面
@app.route("/about")
def about():
    return render_template("about.html",page="about")
#加入我們頁面
@app.route("/join")
def join():
    return render_template("join.html",page="join")
#學習環境頁面
@app.route("/environment")
def environment():
    return render_template("environment.html",page="joenvironment")

@app.route('/dashboard/')
def dashboard():
    client = pymongo.MongoClient("mongodb+srv://admin-mangodb-1:Roottimothychen@cluster0-development.ao9sl.mongodb.net/test?retryWrites=true&w=majority")
    db = client.herokuweb#選擇操作test資料庫
    collection=db.dashboard#操作users集合
    results=collection.find()
    return render_template('dashboard.html',results=results)

@app.route('/dashboard/upload/',methods=['GET','POST'])
def upload():
    form=DashForm()
    if form.validate_on_submit():
        client = pymongo.MongoClient("mongodb+srv://admin-mangodb-1:Roottimothychen@cluster0-development.ao9sl.mongodb.net/test?retryWrites=true&w=majority")
        db = client.herokuweb#選擇操作test資料庫
        collection=db.dashboard#操作users集合
        collection.insert_one({
            "time":"1231231313",
            "content":form.content.data,
            "By":form.by_name.data
        })
        return "送出成功"
    return render_template("upload.html",form=form)

if __name__=="__main__":
    app.run(debug=True)