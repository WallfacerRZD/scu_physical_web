# coding=utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask, render_template, redirect, url_for, session, request
from spider import *
from sql import DataBase
from chardet import detect

app = Flask(__name__)
app.secret_key = 'g\x1a\xfa\xab\xd4\xcd\x89\xc9O\xde\xb1\xd9\x88\xfa\xf7Z\x892\x97F'


def has_login():
    return session.get('account') != None


@app.route('/', methods=['GET', 'POST'])
def index():
    if not has_login():
        return render_template('login.html')
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
        try:
            s = login_scu(account, password)
            if s:
                test_datas = get_datas(s)
                name = test_datas[0].name
                db.insert_users(account, password, name)
                for test_data in test_datas:
                    db.insert_datas(account, test_data.datas, test_data.term, test_data.assessment,
                                    test_data.suggestion)
                    db.insert_scores(account, test_data.scores, test_data.term)
                session['account'] = account
                session['password'] = password
                session['name'] = name
                return redirect(url_for('index'))
        except Exception, e:
            return '<p>出错啦!,%s</p>' % str(e)
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


def compose_data(test_datas, scores):
    # 组合同一次体侧的数据与成绩
    # datas = [[[数据],[成绩]], [[]]....]
    datas = []
    for i in test_datas:
        for j in scores:
            if i[15] in j:
                datas.append([i, j])
    return datas


# 返回测试数据
@app.route('/query', methods=['GET'])
def query():
    if has_login():
        # 从本地数据库获取体侧数据
        db = DataBase()
        try:
            test_datas = db.query_datas(session['account'])
            scores = db.query_scores(session['account'])
            # 同一次数据和成绩组合在一起
            datas = compose_data(test_datas, scores)
            return render_template('datas.html', datas=datas)
            # return "<p>test</p>"
        except Exception, e:
            return '<p>出错啦!,%s</p>' % str(e)

    else:
        return '<p>请登录!!</p>'


# 返回可预约信息
@app.route('/tests', methods=['GET', 'POST'])
def tests():
    db = DataBase()
    result = db.query_tests()
    return render_template('tests.html', datas=result)


# 返回预约信息
@app.route('/reserve', methods=['GET', 'POST'])
def reserve():
    if has_login():
        db = DataBase()
        result = db.query_reservations(session['account'])
        return render_template('reservation.html', data=result)
    else:
        return '<p>亲,请登录哦!</p>'


# 预约
@app.route('/do_reserve', methods=['POST'])
def do_reserve():
    if has_login():
        db = DataBase()
        try:
            _id = request.form.get('id', '-1')
        except:
            _id = '-1'
        if _id != '-1':
            result = db.query_tests_by_id(_id)
            has_reserved = db.query_has_reserved(session['account'])
            has_cancled = db.query_cancel(session['account'])
            if(not has_reserved and not has_cancled):
                db.insert_reservation(session['account'], result[1], result[2], _id)
                db.decrease_tests_capacity(_id)
        return redirect(url_for('index'))
    else:
        return '<p>亲,请登录哦!</p>'


# 取消预约
@app.route('/cancle_reservation', methods=['POST'])
def cancel_reservation():
    db = DataBase()
    has_reserved = db.query_has_reserved(session['account'])
    if has_reserved:
        _id = db.get_tests_id(session['account'])
        db.increase_tests_capacity(_id)
        db.delete_reservation(session['account'])
    return redirect(url_for('index'))


# 申请免测
@app.route('/cancle', methods=['POST'])
def cancle():
    db = DataBase()
    result = db.query_cancel(session['account'])
    if not result:
        reason = request.form.get('reason', None)
        if reason:
            db.insert_cancels(session['account'], reason)
            has_reserved = db.query_has_reserved(session['account'])
            if has_reserved:
                _id = db.get_tests_id(session['account'])
                db.increase_tests_capacity(_id)
                db.delete_reservation(session['account'])
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True, port=2333)
