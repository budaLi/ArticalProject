# # -*- coding: utf-8 -*-
# import scrapy
# import re
# import requests
# import json
# import time
# import PIL.Image as Image
# from urllib import parse
# #创建scrapy爬虫时 需进入虚拟环境下的项目目录
# #scrapy genspider 爬虫名称 网址
# cookies={}
# class ZhihuSpider(scrapy.Spider):
#     name = 'zhihu'
#     allowed_domains = ['www.zhihu.com/']
#     start_urls = ['https://www.zhihu.com/']
#     agent='Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'
#     headers={
#      "HOST": "www.zhihu.com",
#     "Referer": "https://www.zhizhu.com",
#     'Connection': 'keep - alive',  # 保持链接状态
#     'user-agent':agent
# }
#     def parse(self, response):
#         """
#         提取页面中所有url 并跟踪这些url 如果提取的url为/question/xxx 那么我们下载后进入解析函数进行入库处理
#         """
#         all_urls=response.css('a::attr(href)').extract()
#         all_urls=[parse.urljoin(response.url,url) for url in all_urls]  #将主域名和url进行拼接
#         print(all_urls)
#     def start_requests(self):   #由于知乎必须登陆 必须重写
#         #先访问知乎首页 获取csrf 再利用回调函数转入login
#        return [scrapy.Request('https://www.zhihu.com/signup?next=%2F',headers=self.headers,callback=self.login)]
#     def login(self,response):
#         captcha_url='https://www.zhihu.com/captcha.gif?r=%d&type=login' % (time.time() * 1000)
#         #获取csrf,_zap,tgw_l7_route
#         all_text=response.headers.getlist('Set-Cookie')
#         _xsrf_pat= re.match('.*?_xsrf=(.*?);',str(all_text[-1]))   #注意此处的获取
#         _xsrf=str(_xsrf_pat.group(1))
#         # _zap_pat= re.match('.*?_zap=(.*?);',str(all_text[1]))   #注意此处的获取
#         # _zap=str(_zap_pat.group(1))
#         # tgw_l7_route_pat= re.match('.*?tgw_l7_route=(.*?);',str(all_text[0]))   #注意此处的获取
#         # tgw_l7_route=str(tgw_l7_route_pat.group(1))
#         if _xsrf:
#             post_date={
#                     '_xsrf':_xsrf,
#                     # '_zap':_zap,
#                     #  'tgw_l7_route':tgw_l7_route,
#                     'username':'15735656005',
#                     'password':'zslswmz+',
#                      'captcha':'',
#                 }
#             yield scrapy.Request(captcha_url,headers=self.headers,meta={'post_data':post_date},dont_filter=True,callback=self.parse_captcha)
#     def parse_captcha(self,response):
#         post_data=response.meta.get('post_data',{})
#         print(post_data)
#         with open('capcha.jpg','wb') as f:
#             f.write(response.body)
#         try:
#             # 利用pillow打开验证码
#             im = Image.open('capcha.jpg')
#             im.show()
#             im.cloes()
#         except:
#             print('请打开文件%s自行输入'%("capcha.jpg"))
#         cap = input("请输入验证码>>")
#         post_data['captcha']=cap
#         log_url = "https://www.zhihu.com/signup?next=%2F"
#         return scrapy.FormRequest(url=log_url,formdata=post_data,headers=self.headers,dont_filter=True,callback=self.check_login)
#     def check_login(self,response):      #验证服务器的返回数据判断是否成功
#         # print(response.text)
#         # text_json = json.loads(response.text)
#         # if "msg" in text_json and text_json["msg"] == "登录成功":
#         #     print('登陆成功')
#         #     for url in self.start_urls:
#         #         yield scrapy.Request(url, dont_filter=True, headers=self.headers,callback=self.parse)
#         with open('login_sucess.html','w',encoding='utf-8') as f :
#             f.write(response.text)
#         for url in self.start_urls:
#             yield scrapy.Request(url, dont_filter=True, cookies=cookies,headers=self.headers) #如果不定义回调函数，转到Parse函数解析





# -*- coding: utf-8 -*-

import re
import json
import datetime
try:
    import urlparse as parse
except:
    from urllib import parse

import scrapy
from scrapy.loader import ItemLoader
from ArticalProject.items import ZhihuQuestionItem,ZhihuAnswerItem


class ZhihuSpider(scrapy.Spider):
    name = "zhihu"
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/']

    # question的第一页answer的请求url
    start_answer_url = "https://www.zhihu.com/api/v4/questions/{0}/answers?sort_by=default&include=data%5B%2A%5D.is_normal%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccollapsed_counts%2Creviewing_comments_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Crelationship.is_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.author.is_blocking%2Cis_blocked%2Cis_followed%2Cvoteup_count%2Cmessage_thread_token%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit={1}&offset={2}"

    headers = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhizhu.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
    }

    custom_settings = {
        "COOKIES_ENABLED": True,
        "DOWNLOAD_DELAY": 1.5,
    }

    def parse(self, response):
        """
        提取出html页面中的所有url 并跟踪这些url进行一步爬取
        如果提取的url中格式为 /question/xxx 就下载之后直接进入解析函数
        """
        all_urls = response.css("a::attr(href)").extract()
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        all_urls = filter(lambda x: True if x.startswith("https") else False, all_urls)
        for url in all_urls:
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", url)
            if match_obj:
                # 如果提取到question相关的页面则下载后交由提取函数进行提取
                request_url = match_obj.group(1)
                yield scrapy.Request(request_url, headers=self.headers, callback=self.parse_question)

            else:
                #此处可能会导致问题过少而答案过多
                # 如果不是question页面则直接进一步跟踪
                yield scrapy.Request(url, headers=self.headers, callback=self.parse)

    def parse_question(self, response):
        # 处理question页面， 从页面中提取出具体的question item
        if "QuestionHeader-title" in response.text:
            # 处理新版本
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", response.url)
            if match_obj:
                question_id = int(match_obj.group(2))

            item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
            item_loader.add_css("title", ".QuestionHeader-title::text")
            item_loader.add_css("content", ".QuestionHeader-detail .RichText.ztext::text")
            item_loader.add_value("url", response.url)
            item_loader.add_value("zhihu_id", question_id)
            item_loader.add_css("answer_num", ".List-headerText span::text")
            item_loader.add_css("comments_num", ".QuestionHeader-Comment button::text")
            item_loader.add_css("watch_user_num", ".NumberBoard-itemValue::text")
            item_loader.add_css("topics", ".QuestionHeader-topics .Popover div::text")

            question_item = item_loader.load_item()
        else:
            # 处理老版本页面的item提取
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", response.url)
            if match_obj:
                question_id = int(match_obj.group(2))

            item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
            item_loader.add_xpath("title",
                                  "//*[@id='zh-question-title']/h2/a/text()|//*[@id='zh-question-title']/h2/span/text()")
            item_loader.add_css("content", "#zh-question-detail")
            item_loader.add_value("url", response.url)
            item_loader.add_value("zhihu_id", question_id)
            item_loader.add_css("answer_num", "#zh-question-answer-num::text")
            item_loader.add_css("comments_num", "#zh-question-meta-wrap a[name='addcomment']::text")
            item_loader.add_xpath("watch_user_num",
                                  "//*[@id='zh-question-side-header-wrap']/text()|//*[@class='zh-question-followers-sidebar']/div/a/strong/text()")
            item_loader.add_css("topics", ".zm-tag-editor-labels a::text")

            question_item = item_loader.load_item()

        yield scrapy.Request(self.start_answer_url.format(question_id, 20, 0), headers=self.headers,
                             callback=self.parse_answer)
        yield question_item

    def parse_answer(self, reponse):
        #处理questiona的answer
        ans_json = json.loads(reponse.text)
        is_end = ans_json["paging"]["is_end"]
        next_url = ans_json["paging"]["next"]

        #提取answer的具体字段
        for answer in ans_json["data"]:
            answer_item = ZhihuAnswerItem()
            answer_item["zhihu_id"] = answer["id"]
            answer_item["url"] = answer["url"]
            answer_item["question_id"] = answer["question"]["id"]
            answer_item["author_id"] = answer["author"]["id"] if "id" in answer["author"] else 0
            #用户匿名时id这个字段就为空
            answer_item["content"] = answer["content"] if "content" in answer else None
            #有些情况下cotent字段也为空
            answer_item["parise_num"] = answer["voteup_count"]
            answer_item["comments_num"] = answer["comment_count"]
            answer_item["create_time"] = answer["created_time"]
            answer_item["update_time"] = answer["updated_time"]
            answer_item["crawl_time"] = datetime.datetime.now()
            yield answer_item
        if not is_end:
            yield scrapy.Request(next_url, headers=self.headers, callback=self.parse_answer)
            #异步I/O，通过callback执行下一步


    def start_requests(self):
        from selenium import webdriver
        browser = webdriver.Chrome(executable_path=r"C:\Users\Lenovo\ArticalProject\ArticalProject\chromedriver.exe")

        browser.get("https://www.zhihu.com/signin")
        browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper Input").send_keys(
            "15735656005")
        browser.find_element_by_css_selector(".SignFlow-password Input").send_keys(
            "zslswmz+")
        browser.find_element_by_css_selector(".Button.SignFlow-submitButton").click()

        import time
        time.sleep(10)
        Cookies = browser.get_cookies()
        print(Cookies)
        cookie_dict = {}
        import pickle
        for cookie in Cookies:
            # 写入文件
            f = open(r'C:\Users\Lenovo\ArticalProject' + cookie['name'] + '.zhihu', 'wb')
            pickle.dump(cookie, f)
            f.close()
            cookie_dict[cookie['name']] = cookie['value']
        browser.close()
        print(cookie_dict)
        return [scrapy.Request(url=self.start_urls[0], dont_filter=True, cookies=cookie_dict, headers=self.headers)]

