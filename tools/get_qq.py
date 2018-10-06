#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/10/4
import pymysql
conn=pymysql.connect(host='127.0.0.1',user='root',passwd='123',db='movie')
cursor=conn.cursor()

def get_all(offset):  #从数据库中获取qq号
    select_count_sql='select count(*) from qq_info'
    select_count=cursor.execute(select_count_sql)
    count=cursor.fetchall()[0][0]
    if offset<int(count):
        sql='select uin from qq_info limit 1 offset {}'.format(offset)
        res=cursor.execute(sql)
        return cursor.fetchall()

def get_list():     #将qq以列表形式返回
    offset=0
    res=''
    ss=[]
    while 1:
        res=get_all(offset)
        offset+=1
        if res is None:
            break
        ss.append(res[0][0])

    return ss


if __name__=='__main__':
    res=get_list()
    print(res)
    #ss='((249,),' 结果为这总形式 所有需要用[0][0]获取数字

