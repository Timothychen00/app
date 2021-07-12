#!/usr/bin/env python3
#! -*- encoding:utf-8 -*-
from flask import Flask,render_template
from threading import Thread
app=Flask(__name__)#檢測執行時的模組，可以是main

@app.route("/")
def home():
    return render_template("main_test.html")

def run():
    app.run(host="0.0.0.0",port="80")

t = Thread(target=run)
t.start()