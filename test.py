# coding=utf-8
from flask import Flask, render_template, send_file, redirect, url_for, session
from flask import request
from spider import get_test_datas
from scu_physical_web.sql import DataBase

app = Flask(__name__)
app.secret_key = 'g\x1a\xfa\xab\xd4\xcd\x89\xc9O\xde\xb1\xd9\x88\xfa\xf7Z\x892\x97F'


def has_login():
    print session.get('account')
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
    rs = db.query_user(account)
    if rs:
        if rs['password'] == password:
            session['account'] = rs['account']
            session['password'] = rs['password']
            session['name'] = rs['name']
            return redirect(url_for('index'))
        else:
            return '<p>密码错误</p>'
    else:
        session['account'] = None
        session['password'] = None
        session['name'] = None
        return '<p>账号不存在</p>'


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('account', None)
    session.pop('name', None)
    session.pop('password', None)
    print session
    return redirect(url_for('index'))


@app.route('/query', methods=['GET'])
def query():
    if has_login():
        db = DataBase()
        datas = get_test_datas(session['account'], session['password'])
        for data in datas:
            db.insert_datas(data[0])
        rs = db.query_datas(session['account'])
        return render_template('datas.html', datas=rs[0])
    else:
        return '<p>请登录!!</p>'

if __name__ == '__main__':
    app.run('0.0.0.0', port=2333, debug=True)
