from flask import session
import uuid,pymongo
from werkzeug.security import check_password_hash, generate_password_hash

client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.jyp4y.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.herokuweb

class User():
    def start_session(self,user):
        del user['password']
        session['logged_in']=True
        session['current_user']=user

    def sign_up(self,form):
        user={
            '_id':uuid.uuid4().hex,
            'username':form.username.data,
            'password':generate_password_hash(form.password.data),
            'email':form.email.data,
            'authority':'normal',
        }
        #email name 錯誤處理
        if db.users.find_one({'username':user['username']}):
            return {'name_error':'用戶名已存在'}
        if db.users.find_one({'email':user['email']}):
            return {'email_error':'此郵箱已經註冊'}
        db.users.insert_one(user)
        self.start_session(user)
        return user

    def login(self,username,password):
        user=db.users.find_one({'username':username})
        if user:
            if check_password_hash(user['password'],password):
                self.start_session(user)
                return user
            else:
                return {'password_error':'密碼錯誤'}
        else:
            return {'name_error':'用戶名錯誤'}

    def log_out(self):
        session.clear()