#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/8/12
import hashlib
import re
def get_md5(url):   #将url进行md5转换
    if isinstance(url,str):
        url=url.encode('utf-8')         #python3中已经将字符串改为Unicode编码，需要将其转换为utf-8才能进行哈希
    m=hashlib.md5()
    m.update(url)
    return m.hexdigest()    #摘要

def get_per_week(value):      #提取实习天数
    s2=str(value).replace('\\u','').replace('[','').replace(']','').replace('-','')
    mat=re.match(".*?(([a-z]|(0-9)).*?)[\u4e00-\u9fa5]", s2)
    if mat:
        res=mat.group(1)
        value=cut_text(res)
        res=mapping(value)
        return ''.join(res).replace('-','')+'天/周'
def get_end_time(value):
    s2=str(value).replace('\\u','').replace('[','').replace(']','').replace('-','')
    return s2
def get_salary(value):
    res=get_end_time(value)
    res=cut_text(res)
    res=mapping((res))
    if len(res)==6:
        res.insert(3,'-')
    else:
        res.insert(2,'-')
    res=''.join(res)
    res.split('-')
    return res
def mapping(value):     #映射
    for i in range(len(value)):
        value[i]=value[i].strip()
        # if value[i]=='e9f6': value[i]='0'
        # elif value[i]=='f2dc': value[i]='1'
        # elif value[i]=='e6f8': value[i]='2'
        # elif value[i]=='efc7': value[i]='3'
        # elif value[i]=='e373': value[i]='4'
        # elif value[i]=='ec5c': value[i]='5'
        # elif value[i]=='ee14': value[i]='6'
        # elif value[i]=='f151': value[i]='7'
        # elif value[i]=='e173': value[i]='8'
        # elif value[i]=='f009': value[i]='9'
        if value[i]=='efdc': value[i]='0'
        elif value[i]=='ef48': value[i]='1'
        elif value[i]=='ef4e': value[i]='2'
        elif value[i]=='f056': value[i]='3'
        elif value[i]=='f0a3': value[i]='4'
        elif value[i]=='e78a': value[i]='5'
        elif value[i]=='ed39': value[i]='6'
        elif value[i]=='ec7b': value[i]='7'
        elif value[i]=='e7b8': value[i]='8'
        elif value[i]=='ea33': value[i]='9'
    return value

def get_date(value):
    value=list(value)
    value.insert(4,"-")
    value.insert(7,"-")
    return ''.join(value)

def cut_text(text):     #按位置切片
    res=[]
    conpire=re.compile('(([a-z]|[0-9]){4})')
    for one in conpire.findall(text):
        res.append(one[0])
    return res
def extract_num(text):
    if text=="":
        return 0
    #从字符串中提取出数字
    match_re = re.match(".*?(\d+).*", text)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0

    return nums

def get_finally(value):
    res=get_end_time(value)
    res=cut_text(res)
    res=mapping(res)
    res=get_date(res)
    return res
def remove_xiexian(text):       #去除斜线换行符
    if text=="":
        return ''
    text=text.replace('/n','').replace("/","").replace(' ','').replace('</p>','').replace('<p>','').replace('<li class="labels">','').replace(
        '</li>','').replace('<pclass="description">','').replace('<br>','').replace('<spanclass="">','').replace('<span>','').replace('\n','').replace('<pclass="">','').replace('<strong>','').replace('<brclass="">','').replace('\t','')
    return text
if __name__=='__main__':
    import requests
    movie_url="https://stsws.qq.com/uwMRJfz-r5jAYaQXGdGnC2_ppdhgmrDlPaRvaV7F2Ic/LrMDwQm_EBI1poYzqP9qLpNgcGv-n8dOjW_E7m1rYMyWt2ualf08KK6cH7xhmNZSsU8i1yh4Aj9nl2buVNIT8tkzgWeOQ0ytu9LoBUx7JB0uRKGRrjSdsTCNdyiPevqta-zVgCZnTygszImGZC0E6LO-qLsP57oC/b00138lwsnj.320090.1.ts?index=4&start=39880&end=50080&brs=3412576&bre=4305575&ver=4"
    res= requests.get(movie_url)
    with open('movie.mp4','w') as f:
        f.write(res)
    print('ok')
    # res='sss:"https://jobs.zhaopin.com/CC2976868ssss8347402.htm,sss:"https://jobs.zhaopin.com/CC29fffss8347402.htm'
    # math=re.compile('(https://jobs.zhaopin.com/.*?.htm)')
    # res=math.findall(res)
    # if res:
    #     print(res)
    #
    #
    # pattern = re.compile("([a-z])")
    # arry = pattern.findall("a b c d e f g h")
    # print(arry)
    # pass

    # from fake_useragent import UserAgent
    # ua=UserAgent()
    # print(ua.random)


    # str='1k/n / -16k/'
    # res=remove_xiexian(str)
    # print(res)
