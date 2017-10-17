# coding=utf-8
import requests
import re
from bs4 import BeautifulSoup
from chardet import detect

wrong_pattern = re.compile(u"学号或者密码错误")
login_url = 'http://pead.scu.edu.cn/jncx/logins.asp'
host = 'http://pead.scu.edu.cn/jncx/'
mid_url = 'http://pead.scu.edu.cn/jncx/?security_verify_data=313932302c31303830'
data_url = 'http://pead.scu.edu.cn/jncx/tcsh2.asp'


class Data(object):
    def __init__(self):
        self.name = ''
        self.datas = []
        self.scores = []
        self.term = []
        self.assessment = []
        self.suggestion = []


def has_logined(page):
    return wrong_pattern.search(page) == None


def login_scu(account, password):
    s = requests.session()
    user_info = {
        'xh': account,
        'xm': password,
        'Submit': '',
    }
    s = requests.session()
    # 访问主页
    s.get(host)
    # 跳转
    s.get(mid_url)
    # 登录
    content = s.post(login_url, user_info).content
    home_page = content.decode('gbk')
    if has_logined(home_page):
        return s
    else:
        return None

def deal_string(string):
    if not string:
        return u'无'.encode('utf-8')
    return string.strip().encode('utf-8')

def get_datas(session):
    if session != None:
        soup = BeautifulSoup(session.get(data_url).content, from_encoding='gbk', features='lxml')
        name = soup.find('caption').text.encode('utf-8')
        trs = soup.find_all('tr')[5:]
        # datas = [[第一次], [第二次], [第三次] ...]
        datas = []
        data = Data()
        for i in range(len(trs)):
            if i % 2 == 0:
                # 获取数据, 学期
                tds = trs[i].find_all('td')[1:16]
                for j in range(len(tds)):
                    if j == 14:
                        data.term = deal_string(tds[j].text)
                    else:
                        text = deal_string(tds[j].find('div').text)
                        data.datas.append(text)
            else:
                # 获取分数, 总评, 建议
                tds = trs[i].find_all('td')[1:]
                for j in range(len(tds)):
                    if j == 12:
                        data.scores.append(u'无'.encode('utf-8'))
                    elif j == 13:
                        text = deal_string(tds[j].text)
                        data.assessment = (text)
                    elif j == 14:
                        text = deal_string(tds[j].text)
                        data.suggestion = (text)
                    else:
                        text = deal_string(tds[j].find('div').text)
                        data.scores.append(text)
                data.name = name
                datas.append(data)
                data = Data()
        return datas


if __name__ == '__main__':
    s = login_scu('2016141462310', '462310')
    if s:
        for i in get_datas(s):
            print i.name
            print i.datas
            print i.scores
            print i.assessment
            print i.suggestion
