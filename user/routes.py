from flask import Flask,render_template,flash,redirect
from __main__ import app
from app import collection,db
from user.models import User
from flask_login import login_user,login_required,logout_user
from werkzeug.security import check_password_hash #checking password
from forms import RegisterForm,LoginForm,DashForm
import time

#註冊頁面
@app.route("/register",methods=["GET","POST"])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        # AddUserData(form.username.data,form.email.data,form.password.data)
        return User().sign_up(form)
    return render_template("register.html",form=form,page="register")

#登錄頁面
@app.route("/login",methods=["GET","POST"])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        # return "成功登錄"
        user = collection.find_one({'username':form.username.data})
        if user is not None and check_password_hash(user['password'],form.password.data):
            user_id=user['_id']
            curr_user = User()
            curr_user.id = user_id

            # 通過Flask-Login的login_user方法登入使用者
            login_user(curr_user)

            return redirect('/')

        flash('Wrong username or password!')
    return render_template("login.html",form=form,page="login")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out successfully!'

#內部行政系統——————————————————————————————————————————
#布告欄
@app.route('/dashboard/')
def dashboard():
    collection=db.dashboard#操作users集合
    results=collection.find()
    return render_template('dashboard.html',results=results)

@app.route('/dashboard/<title>')
def contentspace(title):
    collection=db.dashboard#操作users集合

    result=collection.find_one({"title":title})
    return render_template('dashboard-each.html',result=result)

@app.route('/dashboard/<title>/delete')
def delete(title):
    collection=db.dashboard#操作users集合
    result=collection.remove({"title":title})
    return redirect("/dashboard/")


@app.route('/dashboard/upload/',methods=['GET','POST'])
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
    return render_template("upload.html",form=form)

