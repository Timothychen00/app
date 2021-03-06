from flask_wtf import FlaskForm
# from wtforms import StringField,PasswordField,SubmitField
from wtforms.fields.html5 import EmailField,URLField
from wtforms.fields import StringField,PasswordField,SubmitField,BooleanField,TextAreaField,DateField,RadioField,IntegerField
from wtforms.validators import Email, EqualTo,Length,InputRequired,Regexp
# pip3 install email_validator
class RegisterForm(FlaskForm):
    #field(標籤文字，驗證方式)
    name=StringField('姓名',validators=[InputRequired("此為必填欄目"),Length(max=4)])
    email=EmailField("Email",validators=[InputRequired("此為必填欄目"),Email("請輸入正確的郵箱格式")])
    gender=RadioField('性別：',choices=['男','女','其他'])
    birth=DateField('出生日期',validators=[InputRequired("此為必填欄目")],format='%Y-%m-%d')
    password=PasswordField("Password",validators=[InputRequired("此為必填欄目"),Length(min=8,max=20,message="請輸入8至20位之間的密碼"),Regexp(regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d$@$!%*?&]{8,20}",message='密码至少包含1个大写字母，1个小写字母，1个数字')])
    confirm=PasswordField("Repeat Password",validators=[InputRequired("此為必填欄目"),EqualTo("password",message="請確認兩次輸入密碼是否一致")])
    checkbox=BooleanField("check this out",validators=[InputRequired()])
    submit=SubmitField("Submit")

class LoginForm(FlaskForm):
    #field(標籤文字，驗證方式)
    email=EmailField("Email",validators=[InputRequired("此為必填欄目"),Email("請輸入正確的郵箱格式")])
    password=PasswordField("Password",validators=[InputRequired("此為必填欄目"),Length(min=8,max=20,message="請輸入8至20位之間的密碼"),Regexp(regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d$@$!%*?&]{8,20}",message='密码至少包含1个大写字母，1个小写字母，1个数字')])
    remember=BooleanField('remember me')
    submit=SubmitField("Submit")

class DashForm(FlaskForm):
    #field(標籤文字，驗證方式)
    title=StringField("標題",validators=[InputRequired("此為必填欄目")])
    content=TextAreaField("內容",validators=[InputRequired("此為必填欄目")])
    duration=IntegerField('持續時間：（天數，數字）')
    category=RadioField('推送分類',choices=['最新公告','隊務公告','招生＆招募專區'],default='最新公告')
    collection=RadioField('推送位置',choices=['內部公告','對外公告'])
    link=URLField('相關連結')
    submit=SubmitField("送出")

class EditForm(FlaskForm):
    # name=StringField('姓名',validators=[InputRequired("此為必填欄目")])
    # email=EmailField('郵箱',validators=[InputRequired("此為必填欄目"),Email('請輸入正確的郵箱地址')])
    birth=DateField('出生日期',validators=[InputRequired("此為必填欄目")],format='%Y-%m-%d')
    phone=StringField('手機號',validators=[InputRequired("此為必填欄目"),Length(min=10,max=10,message='請輸入正確的手機號')])
    # gender=RadioField('性別',choices=['男','女'])
    submit=SubmitField('保存')

class EditPasswordForm(FlaskForm):
    password=PasswordField("Password",validators=[InputRequired("此為必填欄目"),Length(min=8,max=20,message="請輸入8至20位之間的密碼"),Regexp(regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d$@$!%*?&]{8,20}",message='密码至少包含1个大写字母，1个小写字母，1个数字')])
    confirm=PasswordField("Repeat Password",validators=[InputRequired("此為必填欄目"),EqualTo("password",message="請確認兩次輸入密碼是否一致")])
    submit=SubmitField('保存')