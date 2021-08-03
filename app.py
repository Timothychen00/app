from flask import Flask,render_template,redirect,request,session,flash
from flask_login import login_user,login_required,logout_user
from werkzeug.security import check_password_hash #checking password
from forms import RegisterForm,LoginForm,DashForm
import time
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

# #註冊頁面
# @app.route("/register",methods=["GET","POST"])
# def register():
#     form=RegisterForm()
#     if form.validate_on_submit():
#         # AddUserData(form.username.data,form.email.data,form.password.data)
#         return User().sign_up(form)
#     return render_template("register.html",form=form,page="register")

# #登錄頁面
# @app.route("/login",methods=["GET","POST"])
# def login():
#     form=LoginForm()
#     if form.validate_on_submit():
#         # return "成功登錄"
#         user = collection.find_one({'username':form.username.data})
#         if user is not None and check_password_hash(user['password'],form.password.data):
#             user_id=user['_id']
#             curr_user = User()
#             curr_user.id = user_id

#             # 通過Flask-Login的login_user方法登入使用者
#             login_user(curr_user)

#             return redirect('/')

#         flash('Wrong username or password!')
#     return render_template("login.html",form=form,page="login")

# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return 'Logged out successfully!'

# #內部行政系統——————————————————————————————————————————
# #布告欄
# @app.route('/dashboard/')
# def dashboard():
#     collection=db.dashboard#操作users集合
#     results=collection.find()
#     return render_template('dashboard.html',results=results)

# @app.route('/dashboard/<title>')
# def contentspace(title):
#     collection=db.dashboard#操作users集合

#     result=collection.find_one({"title":title})
#     return render_template('dashboard-each.html',result=result)

# @app.route('/dashboard/<title>/delete')
# def delete(title):
#     collection=db.dashboard#操作users集合
#     result=collection.remove({"title":title})
#     return redirect("/dashboard/")


# @app.route('/dashboard/upload/',methods=['GET','POST'])
# def upload():
#     form=DashForm()
#     if form.validate_on_submit():
#         collection=db.dashboard#操作users集合
#         collection.insert_one({
#             "time":time.strftime("%Y-%m-%d %I:%M:%S %p", time.localtime()),
#             "title":form.title.data,
#             "content":form.content.data,
#             "by_name":form.by_name.data
#         })
#         return redirect('/dashboard/')
#     return render_template("upload.html",form=form)


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