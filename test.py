# coding=utf-8
from flask import Flask, render_template, send_file, redirect, url_for, session
from flask import request

from scu_physical_web.sql import DataBase

app = Flask(__name__)
app.secret_key = 'g\x1a\xfa\xab\xd4\xcd\x89\xc9O\xde\xb1\xd9\x88\xfa\xf7Z\x892\x97F'

db = DataBase()


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
    account = request.form['account']
    password = request.form['password']
    rs = db.query_user(account, password)
    if rs:
        if rs['password'] == password:
            session['account'] = rs['account']
            session['name'] = rs['name']
            return redirect(url_for('index'))
        else:
            return '<p>密码错误</p>'
    else:
        session['account'] = None
        return '<p>账号不存在</p>'


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('account', None)
    session.pop('name', None)
    print session
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run('0.0.0.0', port=2333, debug=True)
