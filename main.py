from flask import Flask,render_template,redirect,request
from forms import RegisterForm,LoginForm
import pymongo
from forms import DashForm
import os
import time
# from wtforms import StringField,PasswordField,SubmitField
# pip3 install email_validator
#建立app物件
app=Flask(__name__)
#密鑰 csrf,session,login
app.secret_key=os.urandom(16).hex()

#首頁
@app.route("/")
def home():
    return render_template("base.html")

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



#內部行政系統——————————————————————————————————————————
#布告欄
@app.route('/dashboard/')
def dashboard():
    client = pymongo.MongoClient("mongodb+srv://admin-mangodb-1:Roottimothychen@cluster0-development.ao9sl.mongodb.net/test?retryWrites=true&w=majority")
    db = client.herokuweb#選擇操作test資料庫
    collection=db.dashboard#操作users集合
    results=collection.find()
    return render_template('dashboard.html',results=results)

@app.route('/dashboard/<title>')
def contentspace(title):
    client = pymongo.MongoClient("mongodb+srv://admin-mangodb-1:Roottimothychen@cluster0-development.ao9sl.mongodb.net/test?retryWrites=true&w=majority")
    db = client.herokuweb#選擇操作test資料庫
    collection=db.dashboard#操作users集合
    result=collection.find_one({"title":title})
    return render_template('dashboard-each.html',result=result)

@app.route('/dashboard/<title>/delete')
def delete(title):
    client = pymongo.MongoClient("mongodb+srv://admin-mangodb-1:Roottimothychen@cluster0-development.ao9sl.mongodb.net/test?retryWrites=true&w=majority")
    db = client.herokuweb#選擇操作test資料庫
    collection=db.dashboard#操作users集合
    result=collection.remove({"title":title})
    return redirect("/dashboard/")



@app.route('/dashboard/upload/',methods=['GET','POST'])
def upload():
    form=DashForm()
    if form.validate_on_submit():
        client = pymongo.MongoClient("mongodb+srv://admin-mangodb-1:Roottimothychen@cluster0-development.ao9sl.mongodb.net/test?retryWrites=true&w=majority")
        db = client.herokuweb#選擇操作test資料庫
        collection=db.dashboard#操作users集合
        collection.insert_one({
            "time":time.strftime("%Y-%m-%d %I:%M:%S %p", time.localtime()),
            "title":form.title.data,
            "content":form.content.data,
            "by_name":form.by_name.data
        })
        return redirect('/dashboard/')
    return render_template("upload.html",form=form)

if __name__=="__main__":
    app.run(debug=True)