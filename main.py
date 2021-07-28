from flask import Flask,render_template,redirect,request
from forms import RegisterForm,LoginForm
import os
from flask_wtf import FlaskForm
# from wtforms import StringField,PasswordField,SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.fields import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import Email, EqualTo,Length,InputRequired, ValidationError,Regexp
# pip3 install email_validator
class RegisterForm(FlaskForm):
    #field(標籤文字，驗證方式)
    username=StringField("Username",validators=[InputRequired("此為必填欄目"),Length(min=6,max=20,message="請輸入6至20位的用戶名稱")])
    email=EmailField("Email",validators=[InputRequired("此為必填欄目"),Email("請輸入正確的郵箱格式")])
    password=PasswordField("Password",validators=[InputRequired("此為必填欄目"),Length(min=8,max=20,message="請輸入8至20位之間的密碼"),Regexp(regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d$@$!%*?&]{8,20}",message='密码至少包含1个大写字母，1个小写字母，1个数字')])
    confirm=PasswordField("Repeat Password",validators=[InputRequired("此為必填欄目"),EqualTo("password",message="請確認兩次輸入密碼是否一致")])
    checkbox=BooleanField("check this out",validators=[InputRequired()])
    submit=SubmitField("Submit")

class LoginForm(FlaskForm):
    #field(標籤文字，驗證方式)
    username=StringField("Username",validators=[InputRequired("此為必填欄目"),Length(min=6,max=20,message="請輸入6至20位的用戶名稱")])
    password=PasswordField("Password",validators=[InputRequired("此為必填欄目"),Length(min=8,max=20,message="請輸入8至20位之間的密碼"),Regexp(regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d$@$!%*?&]{8,20}",message='密码至少包含1个大写字母，1个小写字母，1个数字')])
    submit=SubmitField("Submit")

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
@app.route("/login")
def login():
    form=LoginForm()
    if form.validate_on_submit():
        return "成功登錄"
    return render_template("login.html",form=form,page="login")

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