import requests
from bs4 import BeautifulSoup
import json


headers = {
'Host':'github.com',
'Origin':'https://github.com',
'Referer':'https://github.com/login',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
}


class GitHub():

    def __init__(self):
        self.session = requests.session()
        self.timeline = []
        self.name = ''
        self.user = ''
        self.passwd = ''

    def login(self):
        self.user = input('please input username:')
        self.passwd = input('please input password:')
        html = self.session.get('https://github.com/login', headers=headers).text
        authenticity_token = BeautifulSoup(html, 'lxml').find(
            'input', {'name': 'authenticity_token'}).get('value')
        print(authenticity_token)
        data = {
            'commit': "Sign+in",
            'utf8': "✓",
            'login': self.user,
            'password': self.passwd,
            'authenticity_token': authenticity_token
        }
        html = self.session.post('https://github.com/session', data=data, headers=headers)
        with open('github.html','w',encoding='utf8') as f:
            f.write(html.text)


github = GitHub()
github.login() # 这一步会提示你输入用户名和密码
