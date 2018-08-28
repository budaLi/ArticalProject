# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver  #再Python selenium官网中可以看到
from selenium.webdriver.support.ui import WebDriverWait
from ArticalProject.items import TianyanchaItem
from scrapy.loader import ItemLoader
from urllib import parse
import re


class TianyanchaSpider(scrapy.Spider):
    name = 'tianyancha'
    allowed_domains = ['www.tianyancha.com']
    start_urls = ['https://www.tianyancha.com/']

    headers = {
        "HOST": "www.tianyancha.com",
        "Referer": "https://www.tianyancha.com/",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
    }

    custom_settings = {
        "COOKIES_ENABLED": True,
        "DOWNLOAD_DELAY": 1.5,
    }

    def start_requests(self):   #登陆
        import time
        brower=webdriver.Chrome(executable_path=r"C:\Users\Lenovo\ArticalProject\ArticalProject\chromedriver.exe")
        brower.get('https://www.tianyancha.com/')
        time.sleep(3)
        brower.find_element_by_xpath('//*[@id="web-content"]/div/div[1]/div[1]/div/div/div[2]/div[1]/a').click()
        time.sleep(3)
        brower.find_element_by_xpath('//*[@id="_modal_container"]/div/div/div[2]/div/div/div[3]/div[2]/div[1]').click()
        brower.find_element_by_xpath('//*[@id="_modal_container"]/div/div/div[2]/div/div/div[3]/div[1]/div[2]/input').send_keys('15735656005')
        brower.find_element_by_xpath('//*[@id="_modal_container"]/div/div/div[2]/div/div/div[3]/div[1]/div[3]/input').send_keys('zslswmz1')
        brower.find_element_by_xpath('//*[@id="_modal_container"]/div/div/div[2]/div/div/div[3]/div[1]/div[5]').click()

        time.sleep(3)
        #获取cookie
        cookie_dict = {}
        Cookies=brower.get_cookies()
        for cookie in Cookies:
            cookie_dict[cookie['name']] = cookie['value']
        time.sleep(5)
        brower.close()
        print(cookie_dict)
        return [scrapy.Request(url=self.start_urls[0],cookies=cookie_dict,dont_filter=True,headers=self.headers)]       #此处设置请求头
    def parse(self, response):
        all_urls = response.css("a::attr(href)").extract()
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        all_urls = filter(lambda x: True if x.startswith("https") else False, all_urls)
        for url in all_urls:
            match_obj = re.match("(.*tianyancha.com/company/(\d+))(/|$).*", url)
            if match_obj:
                # 如果提取到company相关的页面则下载后交由提取函数进行提取
                request_url = match_obj.group(1)
                yield scrapy.Request(request_url, headers=self.headers, callback=self.parse_conpany)

    def parse_conpany(self,response):
        print(response.text)
        # itemloder=ItemLoader(item=TianyanchaItem(),response=response)
        # itemloder.add_css('company_name','.content .header .name::text')
        # itemloder.add_value('url',response.url)
        # itemloder.add_value('url_object_id','')
        # itemloder.add_css('tel','.content .detail .in-block span:nth-child(2)::text')
        # itemloder.add_css('email','.content .detail .email::text')
        # itemloder.add_css('address','.content .detail .address::attr(title)::text')
        # itemloder.add_css('info','.content .detail .sumary span::text')
        # itemloder.add_css('table','.table.-striped-col.-border-top-none')
        # itemloder.add_xpath('gong_shang_zhu_ce_hao','//*[@id="_container_baseInfo"]/table[2]/tbody/tr[1]/td[2]/text()')
        # itemloder.add_xpath('zu_zhi_ji_gou_dai_ma','//*[@id="_container_baseInfo"]/table[2]/tbody/tr[1]/td[4]/text()')
        # itemloder.add_xpath('tong_yi_xin_yong_dai_ma','//*[@id="_container_baseInfo"]/table[2]/tbody/tr[2]/td[2]/text()')
        # itemloder.add_xpath('na_shui_ren_shi_bie_hao','//*[@id="_container_baseInfo"]/table[2]/tbody/tr[3]/td[2]/text()')
        # itemloder.add_xpath('company_type','//*[@id="_container_baseInfo"]/table[2]/tbody/tr[2]/td[4]/text()')
        # itemloder.add_xpath('hang_ye','//*[@id="_container_baseInfo"]/table[2]/tbody/tr[3]/td[4]/text()')
        # itemloder.add_xpath('yin_ye_qi_xian','//*[@id="_container_baseInfo"]/table[2]/tbody/tr[4]/td[2]/span/text()')
        # itemloder.add_xpath('he_zhun_ri_qi','//*[@id="_container_baseInfo"]/table[2]/tbody/tr[4]/td[4]/text/text()')
        # itemloder.add_xpath('na_shui_ren_zi_zhi','//*[@id="_container_baseInfo"]/table[2]/tbody/tr[5]/td[2]/text()')
        # itemloder.add_xpath('ren_yuan_gui_mo','//*[@id="_container_baseInfo"]/table[2]/tbody/tr[5]/td[4]/text()')
        # itemloder.add_xpath('shi_jiao_zi_ben','//*[@id="_container_baseInfo"]/table[2]/tbody/tr[6]/td[2]/text()')
        # itemloder.add_xpath('deng_ji_ji_guan','//*[@id="_container_baseInfo"]/table[2]/tbody/tr[6]/td[4]/text()')
        # itemloder.add_xpath('can_bao_ren_shu','//*[@id="_container_baseInfo"]/table[2]/tbody/tr[7]/td[2]/text()')
        # itemloder.add_xpath('english_name','//*[@id="_container_baseInfo"]/table[2]/tbody/tr[7]/td[4]/text()')
        # itemloder.add_xpath('zhu_ce_di_zhi','//*[@id="_container_baseInfo"]/table[2]/tbody/tr[8]/td[2]/text()')
        # itemloder.add_xpath('jing_yin_fan_wei','//*[@id="_container_baseInfo"]/table[2]/tbody/tr[9]/td[2]/span/span/span[2]/text()')

        # item=itemloder.load_item()
        # return item
        pass
