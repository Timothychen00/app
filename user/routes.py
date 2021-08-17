from flask import Blueprint
from forms import *
from flask import session,request,render_template,redirect,flash
from user.models import User,UserData
from decorators import login_required
app_user_routes = Blueprint('app_file1',__name__)

@app_user_routes.route("/login",methods=["GET","POST"])
def login():
    form=LoginForm()
    session['from']=request.path
    if form.validate_on_submit():
        result=User().login(form.email.data,form.password.data)
        #用戶名或密碼錯誤
        if 'email_error' in result:
            form.email.errors.append(result['email_error'])
            return render_template("login.html",form=form,page="login")
        if 'password_error' in result:
            form.password.errors.append(result['password_error'])
            return render_template("login.html",form=form,page="login")
        #記住我選項
        if form.remember.data==True:
            session.permanent=True
        #成功登錄
        return redirect('/')
    return render_template("login.html",form=form,page="login")

#註冊頁面
@app_user_routes.route("/register",methods=["GET","POST"])
def register():
    form=RegisterForm()
    session['from']=request.path
    if form.validate_on_submit():
        #sign up
        result=User().sign_up(form)
        #email username error
        if 'email_error' in result:
            form.email.errors.append(result['email_error'])
            return render_template("register.html",form=form,page="register")
        #註冊沒有錯誤，引導到登錄介面
        return redirect('login')
    return render_template("register.html",form=form,page="register")

#登出
@app_user_routes.route('/logout')
@login_required
def logout():
    User().log_out()
    return redirect('/')


@app_user_routes.route('/userspace/')
@login_required
def userspace():
    User().refresh_user()
    return render_template('userspace.html')

@app_user_routes.route('/userspace/edit/',methods=['POST','GET'])
@login_required
def userspace_edit():
    form=EditForm()
    if form.validate_on_submit():
        UserData().update_basic(form)
        flash('修改成功')
        return redirect('/userspace/')
    return render_template('userspace-edit.html',form=form)

@app_user_routes.route('/userspace/edit/password/',methods=['POST','GET'])
@login_required
def edit_password():
    form=EditPasswordForm()
    if form.validate_on_submit():
        UserData().update_password(form)
        flash('密碼修改成功')
        return redirect('/userspace/')
    return render_template('userspace-edit-password.html',form=form)