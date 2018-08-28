# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ArticalProject.items import ShixisengItem
from scrapy.loader import ItemLoader
from ArticalProject.utls.common import get_md5
class ShixisengSpider(CrawlSpider):
    name = 'shixiseng'
    allowed_domains = ['www.shixiseng.com']
    start_urls = ['https://www.shixiseng.com/interns/st-intern_?k=&p=1']

    rules = (
        Rule(LinkExtractor(allow=r'https://www.shixiseng.com/intern/inn.*?'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=('https://www.shixiseng.com/com/.*?')),follow=True),
        Rule(LinkExtractor(allow=('https://www.shixiseng.com/')),follow=True)
        ,

    )

    def parse_item(self, response):
        itemloder=ItemLoader(item=ShixisengItem(),response=response)
        itemloder.add_css('title','.new_job_name::text')
        itemloder.add_value('url',response.url)
        itemloder.add_value('url_object_id',get_md5(response.url))
        itemloder.add_css('upgrade_time','.job_date span::text')
        itemloder.add_css('salary_min','.job_money::text')      #范围
        itemloder.add_css('job_city','.job_position::attr(title)')
        itemloder.add_css('degree_need','.job_academic::text')
        itemloder.add_css('work_per_week','.job_week::text')
        itemloder.add_css('shixi_time','.job_time::text')
        itemloder.add_css('job_addvantage','.job_good::text')
        itemloder.add_css('job_info','.job_part ::text')
        itemloder.add_css('company_name','.job_com_name::text')
        itemloder.add_css('company_url','.job_link::text')
        itemloder.add_css('work_address','.com_position::text')
        itemloder.add_css('tags','.job_detail_msg span::text')
        itemloder.add_css('end_time','.deadline .job_detail::text')


        item=itemloder.load_item()
        return item
