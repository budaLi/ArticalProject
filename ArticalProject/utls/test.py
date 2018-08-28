#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/13
import requests
import http.cookiejar as cookielib
import re
import time
import hmac
from hashlib import sha1
import json
import base64
from PIL import Image

# 利用session保持链接
session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename="cookies.txt")  # cookie存储文件，
# 提取保存的cookie
try:
    session.cookies.load(ignore_discard=True)  # 从文件中读取cookie
except:
    print("cookie 未能加载")

# 伪造header
agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
header = {
    "HOST": "www.zhihu.com",
    "Referer": "https://www.zhihu.com",
    "User-Agent": agent,
    'Connection': 'keep-alive'
}


def is_login():
    # 通过个人中心页面返回状态码来判断是否登录
    # 通过allow_redirects 设置为不获取重定向后的页面
    response = session.get("https://www.zhihu.com/inbox", headers=header, allow_redirects=False)
    if response.status_code != 200:
        zhihu_login("+15735656005", "zslswmz+")
    else:
        print("你已经登陆了")


def get_xsrf_dc0():
    # 获取xsrf code和d_c0
    # 在请求登录页面的时候页面会将xsrf code 和d_c0加入到cookie中返回给客户端
    response = session.get("https://www.zhihu.com/signup", headers=header)
    print(response.cookies)
    return response.cookies["_xsrf"], response.cookies["d_c0"]


def get_signature(time_str):
    # 生成signature,利用hmac加密
    # 根据分析之后的js，可发现里面有一段是进行hmac加密的
    # 分析执行加密的js 代码，可得出加密的字段，利用python 进行hmac几码
    h = hmac.new(key='d1b964811afb40118a12068ff74a12f4'.encode('utf-8'), digestmod=sha1)
    grant_type = 'password'
    client_id = 'c3cef7c66a1843f8b3a9e6a1e3160e20'
    source = 'com.zhihu.web'
    now = time_str
    h.update((grant_type + client_id + source + now).encode('utf-8'))
    return h.hexdigest()


def get_identifying_code(headers):
    # 判断页面是否需要填写验证码
    # 如果需要填写则弹出验证码，进行手动填写

    # 请求验证码的url 后的参数lang=en，意思是取得英文验证码
    # 原因是知乎的验证码分为中文和英文两种
    # 中文验证码是通过选择倒置的汉字验证的，破解起来相对来说比较困难，
    # 英文的验证码则是输入验证码内容即可，破解起来相对简单，因此使用英文验证码
    response = session.get('https://www.zhihu.com/api/v3/oauth/captcha?lang=en', headers=headers)
    # 盘但是否存在验证码
    r = re.findall('"show_captcha":(\w+)', response.text)
    if r[0] == 'false':
        return ''
    else:
        response = session.put('https://www.zhihu.com/api/v3/oauth/captcha?lang=en', headers=header)
        show_captcha = json.loads(response.text)['img_base64']
        with open('captcha.jpg', 'wb') as f:
            f.write(base64.b64decode(show_captcha))
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
        captcha = input('输入验证码:')
        session.post('https://www.zhihu.com/api/v3/oauth/captcha?lang=en', headers=header,
                     data={"input_text": captcha})
        return captcha


def zhihu_login(account, password):
    '''知乎登陆'''
    post_url = 'https://www.zhihu.com/api/v3/oauth/sign_in'
    XXsrftoken, XUDID = get_xsrf_dc0()
    header.update({
        "authorization": "oauth c3cef7c66a1843f8b3a9e6a1e3160e20",  # 固定值
        "X-Xsrftoken": XXsrftoken,
    })
    time_str = str(int((time.time() * 1000)))
    # 直接写在引号内的值为固定值，
    # 只要知乎不改版反爬虫措施，这些值都不湖边
    post_data = {
        "client_id": "c3cef7c66a1843f8b3a9e6a1e3160e20",
        "grant_type": "password",
        "timestamp": time_str,
        "source": "com.zhihu.web",
        "password": password,
        "username": account,
        "captcha": "",
        "lang": "en",
        "ref_source": "homepage",
        "utm_source": "",
        "signature": get_signature(time_str),
        'captcha': get_identifying_code(header)
    }

    response = session.post(post_url, data=post_data, headers=header, cookies=session.cookies)
    if response.status_code == 201:
        # 保存cookie，下次直接读取保存的cookie，不用再次登录
        session.cookies.save()
    else:
        print("登录失败")


if __name__ == '__main__':
    is_login()