from flask import (Flask,render_template,request,redirect,url_for,make_response,Response)
import uuid
import pymongo
import time
from pymongo import MongoClient 
import random
import redis
rdb = redis.Redis(host='localhost',port=6379,db=0)
client = MongoClient()
db1 = client.login
user = db1.col
app=Flask(__name__)

@app.route('/hello')
def hello():
    return render_template('hello.html')

@app.route('/')
def chushi():
    username = request.cookies.get('username')
    T=rdb.get('username')
    print(T)
    if T==None or username == None:
        return render_template('login.html')
    else:
        print(T)
        return render_template('hello.html') 

@app.route('/login', methods=['GET', 'POST'])
def login():
    username=request.values.get('username')
    password=request.values.get('password')
    T=user.find_one({'username':username})
    print(T,username,password)
    if T==None:
        code=400
        return '用户名错误',code
    elif T['password']==None or T['password']!=password:
        code=410
        return '密码错误',code
    elif T['password']==password:
        print('i')
        resp=make_response(render_template('hello.html'))
        rdb.mset(username=str(uuid.uuid4()))
        resp.set_cookie('username',str(uuid.uuid4()),expires=time.time()+3600*24*30)
        return resp 
    

@app.route('/registere')
def registere():
    return render_template('registered.html')

@app.route('/registered',methods=['GET','POST'])
def registered():
    username=request.values.get('username')
    Email=request.values.get('Email')
    password=request.values.get('password')
    confirm=request.values.get('confirm')
    U=user.find_one({'username':username})
    E=user.find_one({'E-mail':Email})
    print(username,Email,1)
    print(U,E,2)
    print(password,confirm,3)
    if U!=None:
        code=400
        print(1)
        return '用户名已存在',code
    elif E!=None: 
        code=410
        print(2)
        return 'Email已注册',code
    elif username=='':
        code=420
        print(3)
        return '用户名不能为空',code
    elif password=='':
        code=430
        print(4)
        return '密码不能为空',code
    elif password != confirm:
        code = 440
        print(5)
        return '两次密码不相同',code
    else:
        print(password,confirm,5)
        resp=make_response(render_template('hello.html'))
        rdb.mset(username=str(uuid.uuid4()))
        resp.set_cookie('username',str(uuid.uuid4()),expires=time.time()+3600*24*30)
        user.insert({'username':username,'password':password,'E-mail':Email})
        return resp
   

app.run(debug=True)
