#!/usr/bin/env python3
#! -*- encoding:utf-8 -*-
from flask import Flask,render_template
app=Flask(__name__)#檢測執行時的模組，可以是main

@app.route("/")
def home():
    return render_template("a.html")

if __name__=="__main__":
    app.run()#啟動伺服器