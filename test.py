
from flask import jsonify,Flask,request,session,url_for
import datetime
app=Flask(__name__)
app.secret_key='akdsjla'

@app.after_request
def after(response):
    print(request.path)
    return response


@app.route('/')
def home():
    print(jsonify(name='timothychen',age='800yearsold'))
    print(url_for('home',name='s'))
    return jsonify(jsonify='timothychen',age='800yearsold')
if __name__=='__main__':
    app.run()