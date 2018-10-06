#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/10/4
from tools.get_qq import get_list
import requests
def get_shuoshuo(self,qq):
    '''
    获取好友的前100条说说吧 不够就不获取了
    :param response:
    :return:
    '''
    #qq号 g_tk 以及查询的量（只需变跳过数)
    shuoshuo_url='https://h5.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?uin={}&inCharset=utf-8&outCharset=utf-8&hostUin={}&notice=0&sort=0&pos={}&num=20&cgi_host=http%3A%2F%2Ftaotao.qq.com%2Fcgi-bin%2Femotion_cgi_msglist_v6&code_version=1&format=jsonp&need_private_comment=1&g_tk={}'
    for num in range(0,100,20):
        url=shuoshuo_url.format(qq,qq,num,self.g_tk)  #第三个参数为跳过数
def get_shuoshuo_detail(self,response):
    print(response.text)