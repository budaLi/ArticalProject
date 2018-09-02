#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/10

from scrapy.cmdline import execute
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#通过main文件名找到父目录
# execute(['scrapy','crawl','jobble'])        #通过命令行运行爬虫
# execute(['scrapy','crawl','zhihu'])        #通过命令行运行爬虫
#execute(['scrapy','crawl','lagou'])        #通过命令行运行爬虫
# execute(['scrapy','crawl','tianyancha'])        #通过命令行运c行爬虫
# execute(['scrapy','crawl','zhilian'])        #通过命令行运c行爬虫
# execute(['scrapy','crawl','shixiseng'])        #通过命令行运c行爬虫
# execute(['scrapy','crawl','movie'])        #通过命令行运c行爬虫
# execute(['scrapy','crawl','meizi'])        #通过命令行运c行爬虫
# execute(['scrapy','crawl','chengren'])        #通过命令行运c行爬虫
# execute(['scrapy','crawl','qq'])        #通过命令行运c行爬虫
# execute(['scrapy','crawl','tc_cartoon'])        #通过命令行运c行爬虫
execute(['scrapy','crawl','doutu'])        #通过命令行运c行爬虫
