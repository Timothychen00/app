from flask import session
import uuid,pymongo
from werkzeug.security import check_password_hash, generate_password_hash

client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.m8nzl.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.flaskweb

class User():
    def start_session(self,user):
        del user['password']
        session['logged_in']=True
        session['current_user']=user

    def sign_up(self,form):
        user={
            '_id':uuid.uuid4().hex,
            'account':form.account.data,
            'password':generate_password_hash(form.password.data),
            'email':form.email.data,
            'authority':'normal',
        }
        #email name 錯誤處理
        if db.users.find_one({'account':user['account']}):
            return {'name_error':'用戶名已存在'}
        if db.users.find_one({'email':user['email']}):
            return {'email_error':'此郵箱已經註冊'}
        db.users.insert_one(user)
        # self.start_session(user)
        return user

    def login(self,account,password):
        user=db.users.find_one({'account':account})
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

    def refresh_user(self):
        user=db.users.find_one({'account':session['current_user']['account']})
        self.start_session(user)

class UserData():
    def update_basic(self,form):
        updatedata={
            'name':form.name.data,
            'birth':str(form.birth.data),
            'email':form.email.data,
            'phone':form.phone.data
        }
        # for key in updatedata.keys():

        db.users.update({'account':session['current_user']['account']}, {'$set': {"name":updatedata['name']}})
        db.users.update({'account':session['current_user']['account']}, {'$set': {"email":updatedata['email']}})
        db.users.update({'account':session['current_user']['account']}, {'$set': {"phone":updatedata['phone']}})
        db.users.update({'account':session['current_user']['account']}, {'$set': {"birth":updatedata['birth']}})

    def update_password(self,form):
        password=generate_password_hash(form.password.data)
        db.users.update({'account':session['current_user']['account']}, {'$set':{"password":password}})