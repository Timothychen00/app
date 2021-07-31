from flask_wtf import FlaskForm
# from wtforms import StringField,PasswordField,SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.fields import StringField,PasswordField,SubmitField,BooleanField,TextAreaField
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
    remember=BooleanField("記住我")
    submit=SubmitField("Submit")

class DashForm(FlaskForm):
    content=TextAreaField("輸入內容",validators=[InputRequired()])
    by_name=StringField("署名",validators=[InputRequired()])
    title=StringField("標題",validators=[InputRequired()])
    submit=SubmitField('送出')