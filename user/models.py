import uuid
from flask_login import UserMixin
import pymongo
from werkzeug.security import generate_password_hash
#json和jsonify唯一的區別就是jsonify回傳的是一個json的物件，並且在回應頭中會標明“application/json”
#而json.dumps回傳的是json的格式字串“text/html”
client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.jyp4y.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.herokuweb

class User(UserMixin):
    def sign_up(self,form):
        user={
            '_id':uuid.uuid4().hex,
            'username':form.username.data,
            'email':form.email.data,
            'password':form.password.data,
            'authorty':'',
        }
        user['password']=generate_password_hash(user['password'])
        db.users.insert_one(user)
        return user
