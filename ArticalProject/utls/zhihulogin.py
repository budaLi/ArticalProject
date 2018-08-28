#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/13
import requests
import re

try:
    import cookielib
except:
    import http.cookiejar as cookielib
session=requests.session()  #创建一个request的session对象
session.cookies=cookielib.LWPCookieJar(filename='cookie.txt')   #可以调用session.cookies.save（）
try:
    session.cookies.load(ignore_discard=True)
except:
    print('cookie未能加载')

agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
headers={
    'user-agent':agent
}
def get_xsrf():     #获取xsrf
    response=requests.get('https://www.zhihu.com/signin',headers=headers)
    return response.cookies['_xsrf']

def login_zhihu(username,password):
    if re.match('^1\d{10}',username):
        print('手机号码登陆')
        post_url='https://www.zhihu.com'
        post_date={
            '_xsrf':get_xsrf(),
            username:username,
            password:password
        }
        response=session.post(post_url,data=post_date,headers=headers)
        session.cookies.save()

def check_is_login():       #访问个人主页来确定是否完成登陆
    response=session.get('https://www.zhihu.com/people/shime-bu-da/activities',headers=headers,allow_redirects=False)
    with open('login.html','w',encoding='utf-8') as f :
                f.write(response.text)
    if response.status_code==200:
        print('已经登陆')
        response=session.get('https://www.zhihu.com/signin',headers=headers)
        if response.status_code==200:
            print('登陆成功')
            with open('login_sucess.html','w',encoding='utf-8') as f :
                f.write(response.text)
    else:
        print('尚未登陆')
login_zhihu('15735656005','zslswmz+')
check_is_login()
