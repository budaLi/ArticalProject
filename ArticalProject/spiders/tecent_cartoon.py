#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/9/2
import scrapy
from ArticalProject.items import CartoonItem
from ArticalProject.utls.common import get_md5

class TencentSpider(scrapy.Spider):
    name = 'tc_cartoon'
    allowed_domains = ['v.qq.com']
    base_url = 'https://v.qq.com/x/list/cartoon?offset='  #电影
    custom_settings = {
        "COOKIES_ENABLED": False,
        "DOWNLOAD_DELAY": 0.00,
        'DEFAULT_REQUEST_HEADERS': {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        }
    }
    offset = 0
    start_urls = [base_url + str(offset)]
    total_page = 0

    def parse(self, response):
        if self.offset == 0:
            self.total_page = int(response.xpath("/html/body/div[3]/div/div/div[2]/span/a[9]/text()").extract()[0])
        video_list = response.xpath("//li[@class='list_item']")
        for node in video_list:
            item = CartoonItem()
            name = node.xpath(".//strong[@class='figure_title']/a/text()").extract()[0]
            score_text = node.xpath(".//div[@class='figure_score']//em/text()").extract()
            score = ''.join(score_text)
            if len(node.xpath(".//span[@class ='figure_info']/text()")):
                short_desc = node.xpath(".//span[@class ='figure_info']/text()").extract()[0]
            else:
                short_desc = ''

            hot = node.xpath(".//span[@class='num']/text()").extract()[0]
            play_url = node.xpath(".//a/@href").extract()[0]
            img = node.xpath(".//img/@r-lazyload").extract()[0]
            item['movie_name'] = name
            item['short_desc'] = short_desc
            item['score'] = score

            item['hot'] = hot
            item['play_url'] = play_url
            item['image_url'] = ['http:'+img]
            request = scrapy.Request(url=play_url, callback=self.get_detail)
            request.meta['item'] = item
            yield request
            # break
        if self.offset < self.total_page - 1:
            self.offset += 1
            url = self.base_url + str(self.offset * 30)
            yield scrapy.Request(url, callback=self.parse)

    def get_detail(self, response):
        item = response.meta['item']
        description = response.xpath("//p[@class='summary']/text()").extract()[0]

        tags_text = response.xpath("//div[@class='video_tags _video_tags']/a/text()").extract()
        if len(tags_text):
            tags = ','.join(tags_text)
        else:
            tags = ''

        #动漫这里显示集数有几种方式
        jishu=''
        jishu_list1=response.css('.item_detail_half a::attr(href)').extract()
        jishu_list2=response.css('.mod_episode .item a::attr(href)').extract()
        if len(jishu_list1):
            for i in range(1,len(jishu_list1)+1):
                jishu+="第%s集:https://v.qq.com"%(str(i))+jishu_list1[i-1]+','
        elif jishu_list2:
            if len(jishu_list2):
                for i in range(1,len(jishu_list2)+1):
                    jishu+="第%s集:https://v.qq.com"%(str(i))+jishu_list2[i-1]+','
        else:
            jishu=''


        url_object_id=get_md5(response.url)
        play_time = response.xpath("//div[@class='figure_count']/span[@class='num']/text()").extract_first()

        item['url_object_id']=url_object_id
        item['jishu']=jishu
        item['tags'] = tags
        item['description'] = description
        item['play_time'] = play_time
        yield item
