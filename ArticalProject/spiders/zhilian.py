# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.loader import ItemLoader
from ArticalProject.items import ZhilianzhaopinItem
from ArticalProject.utls.common import get_md5
import requests
import re
from urllib import parse


class ZhilianSpider(scrapy.Spider):
    name = 'zhilian'
    allowed_domains = ['https://fe-api.zhaopin.com','sou.zhaopin.com/?jl=489']
    start_urls=['https://sou.zhaopin.com/?jl=489']
    josn_url = 'https://fe-api.zhaopin.com/c/i/sou?start=0&pageSize=60&cityId=489&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kt=3&lastUrlQuery=%7B%22p%22:1,%22jl%22:%22489%22%7D'
    headers = {
        # "HOST": "sou.zhaopin.com/?jl=489",
        # "Referer": "https://sou.zhaopin.com/?jl=489",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
    }

    custom_settings = {
        "COOKIES_ENABLED": True,
        "DOWNLOAD_DELAY": 1,
    }

    def parse(self, response):
        page_size=60
        next_page=1
        try:
            #提取是否有下一页 去api接口构造访问
                next_page+=1
                page_size+=60
                url=self.josn_url.format(60,2)
                yield Request(url,headers=self.headers,callback=self.parse_item)
        except:
            print('无数据')
    def parse_item(self,response):  #获取json
        print('匹配正确')
        math=re.compile('(https://jobs.zhaopin.com/.*?.htm)')
        res=math.findall(response.text)     #所有符合条件的
        for one in res:
            detail=requests.get(one)
            yield Request(one,callback=self.parse_detail,headers=self.headers)
    def parse_detail(self,response):
        print('1')
        # te='['首页', '保定人才网', '保定销售代表招聘', '6000-10000元/月\xa0', '全职', '不限', '本科', '10人 ', '双休', '试用期缴纳五险一金', '1000-9999人', '民营', '\n石家庄市桥东区中山路39号勒泰中心（B座）写字楼37/38/39层', '\n']'
        # print(response.text)
        try:
            itemloder=ItemLoader(item=ZhilianzhaopinItem(),response=response)
            itemloder.add_value('url',response.url)
            itemloder.add_value('url_object_id',get_md5(response.url))
            # itemloder.add_css('title','.l.info-h3::text')
            # itemloder.add_css('all','strong::text') #salary work_years degree_need  job_addvantage scale company_type address
            # itemloder.add_css('tags','.icon-promulgator-person a::text')
            # itemloder.add_css('job_info','.pos-ul span::text')
            # itemloder.add_css('company_name','.companny a::text')


            item=itemloder.load_item()
            return item
        except Exception as e:
            print(e)
            pass
