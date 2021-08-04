from re import A
from flask import Flask,render_template,redirect,request,session,flash
from forms import RegisterForm,LoginForm,DashForm
import os,pymongo,time,datetime
from user.models import User
from functools import wraps
#pip3 install 'pymongo[srv]'
#/Applications/Python\ 3.6/Install\ Certificates.command
#建立app物件

client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.jyp4y.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.herokuweb
collection=db.users

app=Flask(__name__)
app.secret_key=os.urandom(16).hex()#密鑰 csrf,session,login
app.permanent_session_lifetime=datetime.timedelta(hours=2)
#ROUTES---------------

#裝飾器
from decorators import login_required,authority_admin,authority_staff

#註冊頁面
@app.route("/register",methods=["GET","POST"])
def register():
    form=RegisterForm()
    session['from']=request.path
    if form.validate_on_submit():
        #sign up
        result=User().sign_up(form)
        #email username error
        if 'name_error' in result:
            form.username.errors.append(result['name_error'])
            return render_template("register.html",form=form,page="register")
        if 'email_error' in result:
            form.email.errors.append(result['email_error'])
            return render_template("register.html",form=form,page="register")
        #註冊沒有錯誤，引導到登錄介面
        return redirect('login')
    return render_template("register.html",form=form,page="register")

#登錄頁面
@app.route("/login",methods=["GET","POST"])
def login():
    form=LoginForm()
    session['from']=request.path
    if form.validate_on_submit():
        result=User().login(form.username.data,form.password.data)
        #用戶名或密碼錯誤
        if 'name_error' in result:
            form.username.errors.append(result['name_error'])
            return render_template("login.html",form=form,page="login")
        if 'password_error' in result:
            form.password.errors.append(result['password_error'])
            return render_template("login.html",form=form,page="login")
        #成功登錄
        return redirect('/')
    return render_template("login.html",form=form,page="login")

#登出
@app.route('/logout')
def logout():
    User().log_out()
    return redirect('/')

#內部行政系統——————————————————————————————————————————
#布告欄
@app.route('/dashboard/')
@login_required
@authority_staff
def dashboard():
    collection=db.dashboard#操作users集合
    results=collection.find()
    session['from']=request.path
    return render_template('dashboard.html',results=results)

@app.route('/dashboard/<title>')
@login_required
@authority_staff
def contentspace(title):
    collection=db.dashboard#操作users集合
    result=collection.find_one({"title":title})
    return render_template('dashboard-each.html',result=result)

@app.route('/dashboard/<title>/delete')
@login_required
@authority_admin
def delete(title):
    collection=db.dashboard#操作users集合
    collection.remove({"title":title})
    return redirect("/dashboard/")


@app.route('/dashboard/upload/',methods=['GET','POST'])
@login_required
@authority_admin
def upload():
    form=DashForm()
    if form.validate_on_submit():
        collection=db.dashboard#操作users集合
        collection.insert_one({
            "time":time.strftime("%Y-%m-%d %I:%M:%S %p", time.localtime()),
            "title":form.title.data,
            "content":form.content.data,
            "by_name":form.by_name.data
        })
        return redirect('/dashboard/')
    session['from']=request.path
    return render_template("upload.html",form=form)


#首頁
@app.route("/")
def home():
    session['from']=request.path
    return render_template("base.html",page="home")

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