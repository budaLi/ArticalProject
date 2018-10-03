#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/29
import scrapy
import re
from scrapy.http import Request
from urllib import parse
from ArticalProject.items import MeiziItem
from ArticalProject.utls.common import get_md5


class MeiziSpider(scrapy.Spider):
    name = 'meizi'
    allowed_domains = ['www.meizitu.com']
    start_urls = ['http://www.meizitu.com/a/more_1.html']
    custom_settings = {
            "DOWNLOAD_DELAY": 0.00
        }

    def parse(self,response):
        pic_urls=response.css('.wp-item .tit a::attr(href)').extract()
        for one in pic_urls:
            yield Request(url=one,callback=self.parse_detail)
        nex_url='http://www.meizitu.com/a/more_{0}.html'
        #提取下一页并进行下载
        for i in range(2,16):  #共有
            yield Request(url=nex_url.format(i),callback=self.parse)
    def parse_detail(self,response):
        pic_urls=response.css('#picture img::attr(src)').extract()
        for one in pic_urls:
            meizi=MeiziItem()
            meizi['image_url']=[one]
            yield meizi