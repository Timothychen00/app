from flask import Flask,render_template,redirect,request,session,flash
from forms import RegisterForm,LoginForm,DashForm,EditForm,EditPasswordForm
import os,pymongo,time,datetime
from user.models import User,UserData
#pip3 install 'pymongo[srv]'
#/Applications/Python\ 3.6/Install\ Certificates.command
#建立app物件
client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.m8nzl.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.flaskweb
collection=db.users

app=Flask(__name__)
app.secret_key=os.urandom(16).hex()#密鑰 csrf,session,login
app.permanent_session_lifetime=datetime.timedelta(hours=2)
#ROUTES---------------
from decorators import login_required,authority_admin,authority_staff #裝飾器

#首頁
@app.route("/")
def home():
    session['from']=request.path
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
            form.account.errors.append(result['name_error'])
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
        result=User().login(form.account.data,form.password.data)
        #用戶名或密碼錯誤
        if 'name_error' in result:
            form.account.errors.append(result['name_error'])
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

@app.route('/userspace/')
@login_required
def userspace():
    User().refresh_user()
    return render_template('userspace.html')

@app.route('/userspace/edit/',methods=['POST','GET'])
@login_required
def userspace_edit():
    form=EditForm()
    if form.validate_on_submit():
        UserData().update_basic(form)
        flash('修改成功')
        return redirect('/userspace/')
    return render_template('userspace-edit.html',form=form)

@app.route('/userspace/edit/password/',methods=['POST','GET'])
@login_required
def edit_password():
    form=EditPasswordForm()
    if form.validate_on_submit():
        UserData().update_password(form)
        flash('密碼修改成功')
        return redirect('/userspace/')
    return render_template('userspace-edit-password.html',form=form)

#內部行政系統——————————————————————————————————————————
#行政系統
@app.route('/officesys/')
@login_required
@authority_staff
def office():
    return render_template('officesys/system.html')

#差遣系統
@app.route('/officesys/attendance/')
@login_required
@authority_staff
def assignment():
    return render_template('officesys/attendance.html')

#公文系統
@app.route('/officesys/bulletin/')
@login_required
@authority_staff
def bulletin():
    return render_template('officesys/bulletin.html')

#請假系統
@app.route('/officesys/leave/')
@login_required
@authority_staff
def leave():
    return render_template('officesys/leave.html')

#任務系統
@app.route('/officesys/task/')
@login_required
@authority_staff
def task():
    return render_template('officesys/task.html')

#財務系統
@app.route('/officesys/finance/')
@login_required
@authority_staff
def finance():
    return render_template('officesys/finance.html')

#布告欄
@app.route('/officesys/dashboard/')
@login_required
@authority_staff
def dashboard():
    collection=db.dashboard#操作users集合
    results=collection.find()
    session['from']=request.path
    return render_template('officesys/dashboard.html',results=results)

#布告欄-每個
@app.route('/officesys/dashboard/<title>/')
@login_required
@authority_staff
def contentspace(title):
    collection=db.dashboard#操作users集合
    result=collection.find_one({"title":title})
    return render_template('officesys/dashboard-each.html',result=result)

#布告欄 刪除
@app.route('/officesys/dashboard/<title>/delete/')
@login_required
@authority_admin
def delete(title):
    collection=db.dashboard#操作users集合
    collection.remove({"title":title})
    return redirect("/officesys/dashboard/")

#布告欄 新增
@app.route('/officesys/dashboard/upload/',methods=['GET','POST'])
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
            "by_name":session['current_user']['account']
        })
        return redirect('/officesys/dashboard/')
    session['from']=request.path
    return render_template("officesys/upload.html",form=form)

if __name__=="__main__":
    app.run(debug=True)