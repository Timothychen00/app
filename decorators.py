from flask import session,flash,redirect,request
from functools import wraps
def login_required(a):
    @wraps(a)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return a(*args,**kwargs)
        else:
            flash('請先登錄')
            return redirect('/login')
    return wrap

def authority_staff(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if session['current_user']['authority']in ['admin','staff']:
            return f(*args,**kwargs)
        else:
            flash('您沒有此權限')
            if 'from' in session:
                return redirect(session['from'])
            return redirect('/')
    return wrap

def authority_admin(b):
    @wraps(b)
    def wrap(*args,**kwargs):
        if session['current_user']['authority']=='admin':
            return b(*args,**kwargs)
        else:
            flash('您沒有此權限')
            if 'from' in session:
                return redirect(session['from'])
            return redirect('/')
    return wrap