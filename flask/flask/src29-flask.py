# python -m flask --app src29-flask run

import numpy as np
import datetime
import time

from flask import Flask, request, redirect, url_for
from flask import render_template

import pymysql

gname = ""
database_password__ = "houpr1013"
name_forget = ''
name_exists :bool = True

app = Flask(__name__)

@app.route('/index.html')
def index():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password=database_password__,
        database='homeSystem'
        )
    cursor = conn.cursor()
    sql = "select count(id) from person"
    cursor.execute(sql)
    res = cursor.fetchone()[0]
    sql = "select min(timestamp) from mood"
    cursor.execute(sql)
    duration = cursor.fetchone()[0]
    nday = datetime.datetime.now()
    duration = nday - duration
    #print(type(duration))
    duration = duration.days

    sql = "select * from person order by birthday_ asc"
    cursor.execute(sql)
    res1 = cursor.fetchall()
    #print(res1)
    plist = []
    for p in res1:
        pdic = dict()
        pdic["id"] = p[0]
        pdic["name"] = p[1]
        pdic["birth"] = p[2].strftime("%Y-%m-%d %H:%M:%S")[0:10]
        pdic["role"] = p[3]
        pdic["gender"] = p[4]
        pdic["song"]= p[5]
        plist.append(pdic)
    #print(plist)
    return render_template("index.html", number = res, time = duration, home = gname, member=plist)

@app.route('/gyj.html/<name>')
def gyj(name):
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password=database_password__,
        database='homeSystem'
        )
    cursor = conn.cursor()
    sql = 'select id from person where name = %s'
    cursor.execute(sql, name)
    id = cursor.fetchall()[0]
    sql = 'select mood,timestamp from mood where id = %s order by timestamp asc'
    cursor.execute(sql,id)
    res = cursor.fetchall()
    mydic = dict()
    for item in res:
        mydic[item[1].strftime("%Y-%m-%d %H:%M:%S")] = item[0]
    #print(res)
    #print(mydic)
    sql = "select * from person order by birthday_ asc"
    cursor.execute(sql)
    res1 = cursor.fetchall()
    #print(res1)
    plist = []
    for p in res1:
        pdic = dict()
        pdic["id"] = p[0]
        pdic["name"] = p[1]
        pdic["birth"] = p[2].strftime("%Y-%m-%d %H:%M:%S")[0:10]
        pdic["role"] = p[3]
        pdic["gender"] = p[4]
        pdic["song"]= p[5]
        plist.append(pdic)
        if p[1]==name:
            this = pdic
    return render_template("gyj.html",home = gname,result = mydic,person=name,member=plist,this_person=this)

@app.route('/add.html', methods=['GET', 'POST'])
def add():
    newname = ""
    if request.method == "POST":
        conn = pymysql.connect(
        host='localhost',
        user='root',
        password=database_password__,
        database='homeSystem'
        )
        cursor = conn.cursor()
        sql = "insert into person values(%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,(request.form['id'],request.form['name'],request.form['birth'],request.form['role'],request.form['gender'],request.form['song']))
        conn.commit()
        newname = request.form['name']

    conn = pymysql.connect(
        host='localhost',
        user='root',
        password=database_password__,
        database='homeSystem'
        )
    
    cursor = conn.cursor()
    sql = "select count(id) from person"
    cursor.execute(sql)
    res = cursor.fetchone()[0]
    sql = "select min(timestamp) from mood"
    cursor.execute(sql)
    duration = cursor.fetchone()[0]
    nday = datetime.datetime.now()
    duration = nday - duration
    #print(type(duration))
    duration = duration.days

    sql = "select * from person order by birthday_ asc"
    cursor.execute(sql)
    res1 = cursor.fetchall()
    #print(res1)
    plist = []
    for p in res1:
        pdic = dict()
        pdic["id"] = p[0]
        pdic["name"] = p[1]
        pdic["birth"] = p[2].strftime("%Y-%m-%d %H:%M:%S")[0:10]
        pdic["role"] = p[3]
        pdic["gender"] = p[4]
        pdic["song"]= p[5]
        plist.append(pdic)
    #print(plist)
    return render_template("add.html", home = gname, member=plist, newname=newname)


@app.route('/')
@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        global gname
        gname = request.form['name']
        password = request.form['password']
        res = deal_family(gname, password)
        if res==2:
            return redirect(url_for('index'))
        else:
            return render_template('login.html', errorr=True)
    return render_template('login.html', errorr=False)


# @app.route('/deal_family', methods=['GET', 'POST'])
def deal_family(name, password):

    # name = request.form['name']
    # password = request.form['password']
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password=database_password__,
        database='homeSystem'
        )
    cur = conn.cursor()
    sql = 'select password from family where name=\'{}\''.format(name)
    sql_return = cur.execute(sql)
    if sql_return!=1:
        return 0
    else:
        res = cur.fetchone()
        if res[0]!=password:
            return 1
        else:
            return 2

    # return redirect(url_for('index'))
# temp_function.deal_family()

#@app.route('/forgot_password.html', methods=['GET', 'POST'])
@app.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    if request.method=='POST':
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password=database_password__,
            database='homeSystem'
        )
        cur = conn.cursor()

        name_forget = request.form['password_forgot']
        sql = 'select * from family where name=\'{}\''.format(name_forget)
        num = cur.execute(sql)
        if num==0:
            return render_template('forgot-password.html', error=True)
        else:
            #requests.post()
            # requests.request('POST', '/reset_password', data={'name': name_forget})
            #return redirect(url_for('reset_password'))
            return redirect(url_for('reset_password', **{'name': name_forget}))
        #return redirect(url_for('reset_password'))
    return render_template('forgot-password.html')


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    global name_forget
    if request.method=='GET':
        #global name_forget
        name_forget = request.args.get('name')
    if request.method=='POST':
        password1 = request.form['password1']
        password2 = request.form['password2']
        #name = request.args.get('name')
        # print(password1)
        # print(password2)
        # print('name: '+name_forget)
        name = name_forget
        name_forget = ''
        if password1 != password2:
            pass
        else:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password=database_password__,
                database='homeSystem',
                autocommit=False
            )
            cur = conn.cursor()
            sql='update family set password=\'{}\' where name=\'{}\''.format(password1, name)
            cur.execute(sql)
            conn.commit()
            return redirect(url_for('login'))

    return render_template('reset_password.html')


app.run(debug=True)
