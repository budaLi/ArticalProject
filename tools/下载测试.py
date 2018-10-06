#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/9/6
import os
import sys
from contextlib import closing  #把任意对象变为上下文管理 并支持with语句
import requests
import re
from tools.he_mp4 import hebin

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings()
def video_downloader(video_url):
    print('下载链接',video_url)
    sess = requests.Session()
    size = 0
    dir=r'C:\Users\Lenovo\ArticalProject\ArticalProject\utls\视频'
    with closing(sess.get(video_url, stream=True, verify=False)) as response:
        match=re.compile('.*?,(.*?)#')
        res=re.findall(match,response.text.replace('\n','').replace('\n',''))
        for i,one in enumerate(res):
            with closing(sess.get('https://ltsbsy.qq.com/uwMRJfz-r5jAYaQXGdGnC2_ppdhgmrDlPaRvaV7F2Ic/cKca1lOtahfenk_VeCQJuyhangsrssr_8PZe5Jyr-TJmhZFTeR2mOEl4BpzfjRacuhNb1t0Sv1NlF61Uv3kDwS4-NWNMi9-UhP90gTJf1lsGeB2xC1DHjGB4FQC6wCo0mJqnuWuikvrfYkxrBVd405UAkNjp4oc2/'+one, stream=True, verify=False)) as response:
                chunk_size = 1024
                content_size = int(response.headers['content-length'])
                if response.status_code == 200:
                    sys.stdout.write('  [文件大小]:%0.2f MB\n' % (content_size / chunk_size / 1024))
                    video_name = os.path.join(dir, str(i)+'.mp4')
                    with open(video_name, 'wb') as file:
                        for data in response.iter_content(chunk_size = chunk_size):
                            file.write(data)
                            size += len(data)
                            file.flush()

                            sys.stdout.write('  [下载进度]:%.2f%%' % float(size / content_size * 100) + '\r')
                            # sys.stdout.flush()
                            if size / content_size == 1:
                                print('\n')
                else:
                    print('链接异常')


if __name__ == "__main__":

    video_downloader('https://ltsbsy.qq.com/uwMRJfz-r5jAYaQXGdGnC2_ppdhgmrDlPaRvaV7F2Ic/cKca1lOtahfenk_VeCQJuyhangsrssr_8PZe5Jyr-TJmhZFTeR2mOEl4BpzfjRacuhNb1t0Sv1NlF61Uv3kDwS4-NWNMi9-UhP90gTJf1lsGeB2xC1DHjGB4FQC6wCo0mJqnuWuikvrfYkxrBVd405UAkNjp4oc2/l002657vhrn.321002.ts.m3u8?ver=4')
    hebin(r'C:\Users\Lenovo\ArticalProject\ArticalProject\utls\视频',r'C:\Users\Lenovo\ArticalProject\ArticalProject\utls')