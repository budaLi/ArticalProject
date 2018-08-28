# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ArticalProject.items import MovieItem
from scrapy.loader import ItemLoader
from ArticalProject.utls.common import get_md5
import urllib.request

class MovieSpider(CrawlSpider):

    name = 'movie'
    allowed_domains = ['v.qq.com']
    start_urls = ['https://v.qq.com/movie/']
    movie_detail_url='http://yun.baiyug.cn/vip/index.php?url='
    custom_settings = {
        "COOKIES_ENABLED": True,
        "DOWNLOAD_DELAY": 0.03,
        'DEFAULT_REQUEST_HEADERS': {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
       'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Connection':'keep-alive',
        'Cookie':'Hm_lvt_ffcba8bba444f065b18b388402d00e95=1535115372,1535115372,1535115407,1535115407; Hm_lpvt_ffcba8bba444f065b18b388402d00e95=1535115407',
        'Host':'v.qq.com',
        'Referer':'https://v.qq.com/movie/',
        'Upgrade-Insecure-Requests':1,
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
    } }
    rules = (
        Rule(LinkExtractor(allow=r'https://v.qq.com/x/cover/.*?.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'https://v.qq.com/movie/'),follow=True),

    )
    def parse_item(self, response):     #每一页有多个电影 需要 对每个电影解析

        itemloader=ItemLoader(item=MovieItem(),response=response)
        itemloader.add_value('url',response.url)
        itemloader.add_value('url_object_id',get_md5(response.url))
        itemloader.add_css('main_title','.video_title a::text')
        itemloader.add_css('title','.video_title::text')
        itemloader.add_css('tags','.video_info a::text')
        itemloader.add_css('score1','.video_score .units::text')  #评分两部分构成
        itemloader.add_css('score2','.video_score .decimal::text')
        itemloader.add_css('info','.summary::text')
        itemloader.add_css('role','.director a::text')
        itemloader.add_css('image_url','.figure_pic::attr(style)')
        itemloader.add_value('movie_url',self.movie_detail_url+response.url)


        item=itemloader.load_item()

        return item
