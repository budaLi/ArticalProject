# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#pipeline作用是截取数据 将其保存到我们想保存的位置
import codecs
import json
from scrapy.pipelines.images import ImagesPipeline,FilesPipeline
from scrapy.exporters import JsonItemExporter       #我们可以在这里自定义文件类型导出
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi #可以将mysql操作转换为异步操作
class ArticalprojectPipeline(object):
    def process_item(self, item, spider):
        return item
class TianyanchaPipeline(object):
    def process_item(self, item, spider):
        item=json.dumps(dict(item), ensure_ascii=False)
        return item
class JsonWithEncodingPipeline(object):     #将item写成json文件
    def __init__(self):
        self.file=codecs.open('article.json','w',encoding='utf-8')  #打开文件
    def process_item(self, item, spider):           #将item写入文件
        lines=json.dumps(dict(item),ensure_ascii=False)+'/n'  #False 否则写入中文出错
        self.file.write(lines)
        return item
    def spider_close(self,spider):  #爬虫结束时关闭文件
        self.file.close()

class JsonExporterPipleline(object):        #自定义json文件导出 调用scrapy 提供的JsonExporter 导出j'son文件
    def __init__(self):
        self.file=open('artileexport.json','wb')    #以二进制方式打开
        self.exporter=JsonItemExporter(self.file,encoding='utf-8',ensure_ascii=False)
        self.exporter.start_exporting()         #开始导出
    def close_spider(self,spider):
        self.exporter.finish_exporting()        #结束导出
        self.file.close()
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item




# class ArticalImagePipeline(ImagesPipeline):     #存储图片
#     def item_completed(self, results, item, info):
#         if 'fornt_image_path' in item:
#             for ok,value in results:
#                 image_url_field=value['path']
#                 item['front_image_path']=image_url_field
#
#             return item
class MeiziImagePipeline(ImagesPipeline):     #存储图片
    def item_completed(self, results, item, info):
        if 'image_url' in item:
            for ok,value in results:
                image_url_field=value['path']
                item['image_path']=image_url_field

                return item
class MovieImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if 'image_url' in item:
            for ok,value in results:
                movie_url_field=value['path']
                item['image_path']=movie_url_field

            return item


class MysqlPipeLine(object):        #将内容保存数据库
    def __init__(self):
        self.conn=MySQLdb.connect('localhost','root','123','movie',charset='utf8',use_unicode=True) #注意此处时utf8
        self.cursor=self.conn.cursor()
    def process_item(self, item, spider):
        insert_sql='''insert into article(title,url,url_object_id)
        VALUE (%s,%s,%s)
        '''
        self.cursor.execute(insert_sql,(item['title'],item['url'],item['url_object_id']))
        self.conn.commit()


class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        #使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider) #处理异常

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print ('啊啊异常了',failure)

    def do_insert(self, cursor, item):
        #执行具体的插入
        #根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)
