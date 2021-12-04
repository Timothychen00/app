from flask import render_template,flash,session,request,Blueprint,redirect
from forms import *
from bson import ObjectId
from decorators import login_required,authority_staff
import datetime,pymongo
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
@app_officesys_routes.route('/officesys/dashboard/<id>/')
@login_required
@authority_staff
def contentspace(id):
    collection=db.dashboard#操作users集合
    result=collection.find_one(ObjectId(id))
    result['time']=datetime.datetime.strptime(result['time'], "%Y-%m-%d %H:%M:%S")
    result['end-time']=result['time']+datetime.timedelta(days=result['duration'])
    return render_template('officesys/dashboard-each.html',result=result)

#布告欄 刪除
@app_officesys_routes.route('/officesys/dashboard/<id>/delete/')
@login_required
@authority_staff
def delete(id):
    collection=db.dashboard#操作users集合
    collection.remove({"_id":ObjectId(id)})
    return redirect("/officesys/dashboard/")

#布告欄 新增
@app_officesys_routes.route('/officesys/dashboard/upload/',methods=['GET','POST'])
@login_required
@authority_staff
def upload():
    form=DashForm()
    if form.validate_on_submit():
        print(form.duration.data)
        # 設定為 +8 時區
        tz = datetime.timezone(datetime.timedelta(hours=+8))
        data={
                "time":datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S"),
                "duration":form.duration.data,
                "title":form.title.data,
                "content":form.content.data,
                'link':form.link.data,
                "by_name":session['current_user']['name']
            }
        #內部公告
        if form.collection.data=='內部公告':
            collection=db.dashboard#操作users集合
        else:#外部公告
            collection=db.announcement
            data['category']=form.category.data
        if not form.duration.data:
            data['duration']=1
        #上傳
        collection.insert_one(data)

        return redirect('/officesys/dashboard/')
    session['from']=request.path
    return render_template("officesys/upload.html",form=form)

@app_officesys_routes.route('/officesys/punch_in/')
@login_required
@authority_staff
def daka():
    return render_template('officesys/punchin.html')


#打卡系統
#上班打卡
@app_officesys_routes.route('/officesys/punch_in/clockin/<data>',methods=['GET'])
@login_required
@authority_staff
def clockin(data):
    date,time=data.split(' ')
    collection=db.clockin#操作users集合
    result=collection.find_one({"name":session["current_user"]['name']})
    if(not result):#不存在
        collection.insert_one({'name':session['current_user']['name']})
    result=collection.find_one({"name":session["current_user"]['name']})
    if(date in result.keys()):#重複打上班卡
        flash("今日已經打卡")
    else:
        result[date]={'clockin':time,'clockout':0,"worktime":0}
        collection.update_one({'name':session['current_user']['name']},{'$set':result})
        flash("上班打卡成功")
    return render_template('officesys/punchin.html')

#下班打卡
@app_officesys_routes.route('/officesys/punch_in/clockout/<data>',methods=['GET'])
@login_required
@authority_staff
def clockout(data):
    date,time=data.split(' ')
    collection=db.clockin#操作users集合
    result=collection.find_one({"name":session["current_user"]['name']})
    if(not result):#不存在
        collection.insert_one({'name':session['current_user']['name']})
    if(not date in result.keys()):#沒打上班卡
        flash("請先上班打卡")
    elif(result[date]['clockout']):#重複打下班卡
        flash("今日已經完成下班打卡")
    else:
        result[date]['clockout']=time
        result[date]['worktime']=str(datetime.datetime.strptime(result[date]['clockout'],"%H:%M:%S")-datetime.datetime.strptime(result[date]['clockin'],"%H:%M:%S"))
        collection.update_one({'name':session['current_user']['name']},{'$set':result})
        flash("下班打卡成功")
    return render_template('officesys/punchin.html')