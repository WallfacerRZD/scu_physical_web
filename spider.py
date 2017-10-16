#coding=utf-8
import requests
import chardet

defaul_header = {
    # 'Connection': 'keep-alive',
    # # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36',
    # 'Host': 'pead.scu.edu.cn',
    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    # 'Accept-Encoding': 'gzip, deflate',
    # 'Accept-Language': 'zh-CN,zh;q=0.8',
}

login_url = 'http://pead.scu.edu.cn/jncx/logins.asp'
host = 'http://pead.scu.edu.cn/jncx/'

account = '2016141462307'
password = '462307'

user_info = {
    'xh': account,
    'xm': password,
    'Submit': '',
}

css_url = 'http://pead.scu.edu.cn/jncx/Css/wangye9pt.css'
mid_url = 'http://pead.scu.edu.cn/jncx/?security_verify_data=313932302c31303830'

s = requests.session()
s.headers.update(defaul_header)
# 访问主页
s.get(host)
# 第一次跳转
s.get(mid_url)

#第二次跳转
response = s.post(login_url, user_info)
content = response.content.decode('gb2312').encode('utf-8')
# content = s.get('http://pead.scu.edu.cn/jncx/main.asp').content.decode('gb2312').encode('utf-8')
# print chardet.detect(content)
# with open('test1.html', 'w') as f:
#     f.write(content)
print content
print s.cookies

