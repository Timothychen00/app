
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
    next='2'
    # print('/home' if next=='2' else 'sh')
    return '678768768'

if __name__=='__main__':
    app.run()