from flask import (Flask,render_template,request,redirect,url_for,make_response,Response)
import uuid
import pymongo
import time
from pymongo import MongoClient 
import random
import redis
import json

rdb = redis.Redis(host='localhost',port=6379,db=0)
client = MongoClient()
db1 = client.login
user = db1.col
app=Flask(__name__)

@app.route('/hello')
def hello():
    return json.dumps({"errcode":0})
    #return render_template('hello.html')

@app.route('/')
def chushi():
    username = request.cookies.get('username')
    T=rdb.get('username')
    print(T)
    if T==None or username == None:
        return json.dumps({"errcode":1})
        #return render_template('login.html')
    else:
        print(T)
        return json.dumps({"errcode":0})
        #return render_template('hello.html') 

@app.route('/login', methods=['GET', 'POST'])
def login():
    username=request.values.get('username')
    password=request.values.get('password')
    T=user.find_one({'username':username})
    print(T,username,password)
    if T==None:
        #code=400
        return json.dumps({"errcode":1,"msg":"用户名错误","code":400})
        #return '用户名错误',code
    elif T['password']==None or T['password']!=password:
        #code=410
        #return '密码错误',code
        return json.dumps({"errcode":1,"msg":"密码错误","code":410})
    elif T['password']==password:
        print('i')
        #resp=make_response(render_template('hello.html'))
        Uuid = str(uuid.uuid4())
        rdb.mset(username=Uuid)
        resp.set_cookie('username',Uuid,expires=time.time()+3600*24*30)
        return json.dumps({"errcode":0})
    

@app.route('/registere')
def registere():
    #return render_template('registered.html')
    return json.dumps({"errcode":0})

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
        #return '用户名已存在',code
        return json.dumps({"errcode":1,"msg":"用户名已存在","code":400})
    elif E!=None: 
        code=410
        print(2)
        #return 'Email已注册',code
        return json.dumps({"errcode":1,"msg":"Email已注册","code":410})
    elif username=='':
        code=420
        print(3)
        #return '用户名不能为空',code
        return json.dumps({"errcode":1,"msg":"用户名不能为空","code":420})
    elif password=='':
        code=430
        print(4)
        #return '密码不能为空',code
        return json.dumps({"errcode":1,"msg":"密码不能为空","code":430})
    elif password != confirm:
        code = 440
        print(5)
        #return '两次密码不相同',code
        return json.dumps({"errcode":1,"msg":"两次密码不相同","code":440})
    else:
        print(password,confirm,5)
        #resp=make_response(render_template('hello.html'))
        Uuid = str(uuid.uuid4())
        rdb.mset(username=Uuid)
        resp.set_cookie('username',Uuid,expires=time.time()+3600*24*30)
        user.insert({'username':username,'password':password,'E-mail':Email})
        return json.dumps({"errcode":0})

@app.route('/forgotten_password')
def forgotten_password():
    send_email()
    #return render_template('forgotten.html')
    return json.jumps({"errcode":0})

@app.route('/email_change_password',methods=['GET','POST'])
def email_change_password():
    username = request.values.get('username')
    password = request.values.get('password')
    confirm_password = request.values.get('confirm_password')
    if password == confirm_password:
        return json.dumps({"errcode":0})
    return json.dumps({"errcode":1,"msg":"两次密码不相同"})

@app.route('/change_password',methods=['GET','POST'])
def change_password():
    username = request.values.get('username')   
    old_password = request.values.get('old_password')
    new_password = request.values.get('new_password')
    correct_password = user.find_one({'username':username},{'password':1})
    if old_password == correct_password:
        user.update({'username':username},{'$set':{'password':new_password}})
        rdb.delete('username')
        #return render_template('login.html')
        return json.dumps({"errcode":0})
    #return render_template('change_password.html')
    return json.dumps({"errcode":1,"msg":"密码不相同","code":400})    


app.run(debug=True,host='0.0.0.0')

