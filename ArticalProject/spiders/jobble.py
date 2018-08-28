# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse
from ArticalProject.items import JobboleArticalItem
from ArticalProject.utls.common import get_md5
import datetime
from scrapy.loader import ItemLoader
from ArticalProject.items import ArticleItemLoder
class JobbleSpider(scrapy.Spider):
    name = 'jobble'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    #收集所有404页面的url以及页面数
    handle_httpstatus_list=[404]
    def ___init__(self):
        self.fail_urls=[]

    def parse(self, response):
        if response.status==404:
            self.fail_urls.append(response.url)
            self.crawler.stats.inc_value('failed_url')
        artical_urls=response.css('#archive .post-thumb a')  #提取所有文章的url
        for node_url in artical_urls:
            post_url=node_url.css('::attr(href)').extract_first('')
            image_url=node_url.css('img::attr(src)').extract_first('')
            yield Request(url=parse.urljoin(response.url,post_url),meta={'front_image_url':image_url},callback=self.parse_detail)     #回掉函数 解析具体字段
        #提取下一页并进行下载
        next_urls=response.css('.next.page-numbers::attr(href)').extract_first('')
        if next_urls:
            yield Request(url=parse.urljoin(response.url,next_urls),callback=self.parse)

    def parse_detail(self,response):        #提取文章的具体字段
        # article_item = JobboleArticalItem()
        # #通过css选择器提取字段
        # front_image_url = response.meta.get("front_image_url", "")  #文章封面图
        # title = response.css(".entry-header h1::text").extract_first('')
        # create_date = response.css("p.entry-meta-hide-on-mobile::text").extract_first('').strip().replace("·","").strip()
        # praise_nums = response.css(".vote-post-up h10::text").extract_first('')
        # fav_nums = response.css(".bookmark-btn::text").extract_first('')
        # match_re = re.match(".*?(\d+).*", fav_nums)
        # if match_re:
        #     fav_nums = int(match_re.group(1))
        # else:
        #     fav_nums = 0
        #
        # comment_nums = response.css("a[href='#article-comment'] span::text").extract_first('')
        # match_re = re.match(".*?(\d+).*", comment_nums)
        # if match_re:
        #     comment_nums = int(match_re.group(1))
        # else:
        #     comment_nums = 0
        #
        # content = response.css("div.entry").extract_first('')
        #
        # tag_list = response.css("p.entry-meta-hide-on-mobile a::text").extract()
        # tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        # tags = ",".join(tag_list)
        #
        # article_item["url_object_id"] = get_md5(response.url)
        # article_item["title"] = title
        # article_item["url"] = response.url
        # try:
        #     create_date = datetime.datetime.strptime(create_date, "%Y/%m/%d").date()#date类型不可调用json.dumps 进行序列化
        # except Exception as e:
        #     create_date = datetime.datetime.now().date()
        # article_item["create_date"] = create_date
        # article_item["front_image_url"] = [front_image_url]
        # article_item["praise_nums"] = praise_nums
        # article_item["comment_nums"] = comment_nums
        # article_item["fav_nums"] = fav_nums
        # article_item["tags"] = tags
        # article_item["content"] = content

        front_image_url = response.meta.get("front_image_url", "")  #文章封面图
        # item_loder=ItemLoader(item=JobboleArticalItem(),response=response)  #在此处实例化一个item对象传进去，格式
        item_loder=ArticleItemLoder(item=JobboleArticalItem(),response=response)  #改写loderItem
        item_loder.add_css('title','.entry-header h1::text')
        item_loder.add_css('create_date','p.entry-meta-hide-on-mobile::text')
        item_loder.add_css('praise_nums','.vote-post-up h10::text')
        item_loder.add_css('fav_nums','.bookmark-btn::text')
        item_loder.add_css('comment_nums',"a[href='#article-comment'] span::text")
        item_loder.add_css('content','.entry p::text')
        item_loder.add_css('tags','p.entry-meta-hide-on-mobile a::text')
        item_loder.add_value('url',response.url)
        item_loder.add_value('url_object_id',get_md5(response.url))
        item_loder.add_value('front_image_url',[front_image_url])

        article_item=item_loder.load_item()     #调用才会解析

        yield article_item