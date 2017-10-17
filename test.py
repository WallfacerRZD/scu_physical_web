# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask, render_template, send_file, redirect, url_for, session
from flask import request
from spider import *
from scu_physical_web.sql import DataBase
from chardet import detect

app = Flask(__name__)
app.secret_key = 'g\x1a\xfa\xab\xd4\xcd\x89\xc9O\xde\xb1\xd9\x88\xfa\xf7Z\x892\x97F'


def has_login():
    return session.get('account') != None


@app.route('/', methods=['GET', 'POST'])
def index():
    if not has_login():
        return send_file('./static/index.html')
    else:
        return render_template('home.html', name=session['name'])


@app.route('/login', methods=['POST'])
def login():
    db = DataBase()
    account = request.form['account']
    password = request.form['password']
    rs = db.query_user(account, password)
    # 本地数据库有记录, 登录, 保存会话
    if rs:
        session['account'] = rs[0]
        session['password'] = rs[1]
        session['name'] = rs[2]
        return redirect(url_for('index'))
    # 本地数据库无记录, 登录体育学院网站
    else:
        # 登录学院网站成功, 写入用户数据到本地数据库
        s = login_scu(account, password)
        if s:
            datas = get_datas(s)
            name = datas[0].name
            db.insert_users(account, password, name)
            session['account'] = account
            session['password'] = password
            session['name'] = name
            return redirect(url_for('index'))
            # db.insert_datas(datas)
        # 登录学院网站失败, 提示账号或密码错误
        else:
            session['account'] = None
            session['password'] = None
            session['name'] = None
        return '<p>账号或密码错误</p>'


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('account', None)
    session.pop('name', None)
    session.pop('password', None)
    # print session
    return redirect(url_for('index'))


@app.route('/query', methods=['GET'])
def query():
    if has_login():
        # 从本地数据库获取体侧数据
        db = DataBase()
        rs = db.query_datas(session['account'])
        return render_template('datas.html', datas=rs[0][1:])
    else:
        return '<p>请登录!!</p>'


if __name__ == '__main__':
    app.run('0.0.0.0', port=2333, debug=True)
