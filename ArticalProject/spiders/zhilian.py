# -*- coding: utf-8 -*-
import scrapy
from scrapy.spider import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from scrapy.loader import ItemLoader
from ArticalProject.items import ZhilianzhaopinItem
from ArticalProject.utls.common import get_md5
import requests
import re
from urllib import parse

count=0
class ZhilianSpider(CrawlSpider):
    name = 'zhilian'
    allowed_domains = ['jobs.zhaopin.com']
    start_urls=['https://jobs.zhaopin.com/131945248250288.htm']
    josn_url = 'https://fe-api.zhaopin.com/c/i/sou?start=0&pageSize=60&cityId=489&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kt=3&lastUrlQuery=%7B%22p%22:1,%22jl%22:%22489%22%7D'
    custom_settings = {
        "COOKIES_ENABLED": True,
        "DOWNLOAD_DELAY": 0.03,
        'DEFAULT_REQUEST_HEADERS': {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
       'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Connection':'keep-alive',
        'Cookie':'Hm_lvt_ffcba8bba444f065b18b388402d00e95=1535115372,1535115372,1535115407,1535115407; Hm_lpvt_ffcba8bba444f065b18b388402d00e95=1535115407',
        'Host':'jobs.zhaopin.com',
        'Referer':'https://jobs.zhaopin.com/',
        'Upgrade-Insecure-Requests':1,
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
    } }
    rules = (
        Rule(LinkExtractor(allow=r'https://jobs.zhaopin.com/\d{15}.*?.htm'), callback='parse_detail', follow=True),
        Rule(LinkExtractor(allow=r'https://sou.zhaopin.com/.*?'),follow=True),

    )
    def parse_detail(self,response):
        global count
        count+=1
        print(count)
        # te='['首页', '保定人才网', '保定销售代表招聘', '6000-10000元/月\xa0', '全职', '不限', '本科', '10人 ', '双休', '试用期缴纳五险一金', '1000-9999人', '民营', '\n石家庄市桥东区中山路39号勒泰中心（B座）写字楼37/38/39层', '\n']'
        # print(response.text)
        # itemloder=ItemLoader(item=ZhilianzhaopinItem(),response=response)
        # itemloder.add_value('url',response.url)
        # itemloder.add_value('url_object_id',get_md5(response.url))
        # itemloder.add_css('title','.l.info-h3::text')
        # itemloder.add_css('all','strong::text') #salary work_years degree_need  job_addvantage scale company_type address
        # itemloder.add_css('job_addvantage','p::text')
        # # itemloder.add_css('job_info','.pos-ul p::text')
        # itemloder.add_css('company_name','.pro-mark a::attr(alt)')
        # itemloder.add_css('tags','.iconfont a::text')
        #
        #
        # item=itemloder.load_item()
        # return item
