#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/9/17
from contextlib import closing  #把任意对象变为上下文管理 并支持with语句
from ArticalProject.items import WangyiyunItem
import scrapy
import requests
class Wangyiyun(scrapy.Spider):
    name = 'wangyiyun'
    allowed_domains = ['music.163.com']
    start_urls = ['https://music.163.com/#/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset=0']
    urls='https://music.163.com/#/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset={}'
    detail_url='https://music.163.com'
    download_url='http://music.163.com/song/media/outer/url?id={}.mp3'

    custom_settings = {
        "COOKIES_ENABLED": False,
        "DOWNLOAD_DELAY": 0.00,
        'DEFAULT_REQUEST_HEADERS': {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        }
    }

    sess = requests.Session()
    def parse(self, response):
        item=WangyiyunItem()
        pre_page=35
        offset=0
        next_page=1500
        # next_page=response.css('#m-pl-pager > div > a:nth-child(11)').extract()  #得到下一页
        music_list=response.css('.m-cvrlst .f-cb li')
        for music in music_list:
            image_url=music.css('.j-flag::attr(src)')
            file_name=music.css('.dec a::attr(title)')
            music_id_list=music.css('.dec a::attr(href)')
            music_id=music_id_list[0]
            item['image_url']=image_url
            item['file_name']=file_name

            request = scrapy.Request(url=self.detail_url+music_id,callback=self.parse_detail)
            request.meta['item']=item
            yield request

        if offset<next_page:
            offset+=pre_page
            url=self.urls.format(offset)

            yield scrapy.Request(url=url,callback=self.parse)


    def parse_detail(self,response):    #获取所有歌曲的id
        item=response.met['item']
        file_name=item['file_name']

        music_list=response.css('.even ')
        for one in music_list:
            music_name=one.css('.txt b::attr(title)').extract()
            length=one.css('.s-fc3 span::text').extract()
            user=one.css('.text::attr(title)').extract()
            zhuanji=one.css('td:nth-child(5)').extract()
            download_id=one.css('.ttc .txt a::attr(href)')

            item['download_id']=download_id
            item['music_name']=music_name
            item['length']=length
            item['user']=user
            item['zhuanji']=zhuanji

            yield item







