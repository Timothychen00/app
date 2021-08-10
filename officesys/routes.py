from flask import render_template,flash,session,request,Blueprint,redirect
from forms import *
from decorators import login_required,authority_admin,authority_staff
import pymongo,time
#連結mongodb
client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.m8nzl.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.flaskweb
#設定藍圖
app_officesys_routes = Blueprint('app_file2',__name__)


#內部行政系統——————————————————————————————————————————
#行政系統
@app_officesys_routes.route('/officesys/')
@login_required
@authority_staff
def office():
    return render_template('officesys/system.html')

#差遣系統
@app_officesys_routes.route('/officesys/attendance/')
@login_required
@authority_staff
def assignment():
    return render_template('officesys/attendance.html')

#公文系統
@app_officesys_routes.route('/officesys/bulletin/')
@login_required
@authority_staff
def bulletin():
    return render_template('officesys/bulletin.html')

#請假系統
@app_officesys_routes.route('/officesys/leave/')
@login_required
@authority_staff
def leave():
    return render_template('officesys/leave.html')

#任務系統
@app_officesys_routes.route('/officesys/task/')
@login_required
@authority_staff
def task():
    return render_template('officesys/task.html')

#財務系統
@app_officesys_routes.route('/officesys/finance/')
@login_required
@authority_staff
def finance():
    return render_template('officesys/finance.html')

#布告欄
@app_officesys_routes.route('/officesys/dashboard/')
@login_required
@authority_staff
def dashboard():
    collection=db.dashboard#操作users集合
    results=collection.find()
    session['from']=request.path
    return render_template('officesys/dashboard.html',results=results)

#布告欄-每個
@app_officesys_routes.route('/officesys/dashboard/<title>/')
@login_required
@authority_staff
def contentspace(title):
    collection=db.dashboard#操作users集合
    result=collection.find_one({"title":title})
    return render_template('officesys/dashboard-each.html',result=result)

#布告欄 刪除
@app_officesys_routes.route('/officesys/dashboard/<title>/delete/')
@login_required
@authority_admin
def delete(title):
    collection=db.dashboard#操作users集合
    collection.remove({"title":title})
    return redirect("/officesys/dashboard/")

#布告欄 新增
@app_officesys_routes.route('/officesys/dashboard/upload/',methods=['GET','POST'])
@login_required
@authority_admin
def upload():
    form=DashForm()
    if form.validate_on_submit():
        print(1)
        data={
                "time":time.strftime("%Y-%m-%d %I:%M:%S %p", time.localtime()),
                "duration":form.duration.data,
                "title":form.title.data,
                "content":form.content.data,
                'link':form.link.data,
                "by_name":session['current_user']['account']
            }
        #內部公告
        if form.collection.data=='內部公告':
            collection=db.dashboard#操作users集合
        else:#外部公告
            collection=db.announcement
            data['category']=form.category.data
            del data['duration']
        #若真實姓名存在則填入
        if session['current_user']['name']:
            data['by_name']=session['current_user']['name']
        #上傳
        collection.insert_one(data)

        return redirect('/officesys/dashboard/')
    session['from']=request.path
    return render_template("officesys/upload1231.html",form=form)