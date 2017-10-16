# coding=utf-8
import requests
from bs4 import BeautifulSoup

login_url = 'http://pead.scu.edu.cn/jncx/logins.asp'
host = 'http://pead.scu.edu.cn/jncx/'
mid_url = 'http://pead.scu.edu.cn/jncx/?security_verify_data=313932302c31303830'


def get_test_datas(account, password):
    user_info = {
        'xh': account,
        'xm': password,
        'Submit': '',
    }
    s = requests.session()  # 访问主页
    s.get(host)
    # 跳转
    s.get(mid_url)

    # 登录
    s.post(login_url, user_info)
    # 获取数据
    soup = BeautifulSoup(s.get('http://pead.scu.edu.cn/jncx/tcsh2.asp').text, 'lxml')
    trs = soup.find_all('tr')[5:]
    # datas = [[第一次], [第二次], [第三次] ...]
    datas = []
    temp = []
    for tr in trs:
        temp.append(map(lambda x: x.text.strip().encode('utf-8') if x.text else '/', tr.find_all('div', attrs={'align': "center"})))
        if len(temp) == 2:
            datas.append(temp)
            temp = []
    return datas


if __name__ == '__main__':
    print get_test_datas('2016141462267', '462267')
