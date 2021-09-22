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
            'email':form.email.data,
            'password':generate_password_hash(form.password.data),
            'birth':str(form.birth.data),
            'gender':form.gender.data,
            'name':form.name.data,
            'authority':'normal',
        }
        #email 錯誤處理
        if db.users.find_one({'email':user['email']}):
            return {'email_error':'此郵箱已經註冊'}
        db.users.insert_one(user)
        # self.start_session(user)
        return user

    def login(self,email,password):
        user=db.users.find_one({'email':email})
        if user:
            if check_password_hash(user['password'],password):
                self.start_session(user)
                return user
            else:
                return {'password_error':'密碼錯誤'}
        else:
            return {'email_error':'郵箱錯誤'}

    def log_out(self):
        session.clear()

    def refresh_user(self):
        user=db.users.find_one({'email':session['current_user']['email']})
        self.start_session(user)

class UserData():
    def update_basic(self,form):
        updatedata={
            'birth':str(form.birth.data),
            'phone':form.phone.data
        }

        # db.users.update({'account':session['current_user']['account']}, {'$set': {"name":updatedata['name']}})
        # db.users.update({'account':session['current_user']['account']}, {'$set': {"email":updatedata['email']}})
        db.users.update({'email':session['current_user']['email']}, {'$set': {"phone":updatedata['phone']}})
        db.users.update({'email':session['current_user']['email']}, {'$set': {"birth":updatedata['birth']}})
        # db.users.update({'account':session['current_user']['account']}, {'$set': {"gender":updatedata['gender']}})

    def update_password(self,form):
        password=generate_password_hash(form.password.data)
        db.users.update({'email':session['current_user']['email']}, {'$set':{"password":password}})