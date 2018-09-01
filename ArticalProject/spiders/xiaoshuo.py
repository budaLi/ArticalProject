#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/30
import scrapy
from scrapy.http import Request
from ArticalProject.items import XiaoshuoItem
from urllib import parse
from ArticalProject.utls.common import remove_xiexian

class XiaoshuoSpider(scrapy.Spider):
    name = 'xiaoshuo'
    allowed_domains = ['www.4455pg.com']
    start_urls = ['https://www.4455pg.com/htm/novellist1/']
    urls='https://www.4455pg.com'
    custom_settings = {
            "DOWNLOAD_DELAY": 0.0
        }

    def parse(self,response):
        this_url=response.url
        nex_url='https://www.4455pg.com/htm/novellist{0}/'
        for i in range(2,37):
            pic_urls=response.css('.news_list li a::attr(href)').extract()
            for one in pic_urls:
                yield Request(url=parse.urljoin(self.urls,one),callback=self.parse_detail)
            then_url=this_url+str(i)+'.htm'
            yield Request(then_url,callback=self.parse_detail)
            #提取下一页并进行下载
        for j in [2,4,5,6,8]:  #共有
            yield Request(url=nex_url.format(j),callback=self.parse)
    def parse_detail(self,response):
        import os
        os.getcwd()
        os.chdir(r'E:\data\xiaoshuo')
        xiaoshuo=XiaoshuoItem()
        xiaoshuo['title']=response.css('.tit1::text').extract()
        xiaoshuo['content']=response.css('.main').extract()
        title=str(xiaoshuo['title'])+'.txt'
        content=remove_xiexian(''.join(xiaoshuo['content']))
        with open(title,'wb') as f:
            f.write(content.encode('utf-8'))
        yield xiaoshuo