# -*- coding: utf-8 -*-
import os
# Scrapy settings for ArticalProject project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'ArticalProject'

SPIDER_MODULES = ['ArticalProject.spiders']
NEWSPIDER_MODULE = 'ArticalProject.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'ArticalProject (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
HTTPERROR_ALLOWED_CODES = [404]
# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'ArticalProject.middlewares.ArticalprojectSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'ArticalProject.middlewares.RandomUserAgentMiddleware': 543, #在这里设置useer agent
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
  #'ArticalProject.pipelines.MysqlTwistedPipeline': 2,      #数字大小决定执行顺序，越小越先执行
   #  'ArticalProject.pipelines.ArticalImagePipeline':1,  #重写管道
    'ArticalProject.pipelines.MovieImagePipeline':1,  #重写管道
    #  'ArticalProject.pipelines.TianyanchaPipeline':1,  #重写管道
    #'ArticalProject.pipelines.MeiziImagePipeline':1,  #重写管道

}


#这儿是 images_urls_field 和images_store
# IMAGES_URLS_FIELD='front_image_url'  #指向items下的一个字段 指明所要下载的图片的url
IMAGES_URLS_FIELD='image_url'  #指向items下的一个字段 指明所要下载的图片的url
# os.path.dirname(__file__)     #获取当前文件的文件名
project_dir=os.path.abspath(os.path.dirname(__file__))  #根据文件名获取绝对路径
# IMAGES_STORE=os.path.join(project_dir,'images') #配置图片的存放路径  在此配置相对路径
IMAGES_STORE='E:\data\images\ss'
# IMAGES_MIN_HEIGHT=240      #设置图片大小
# IMAGE_MIN_WIDTH=240
# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
MYSQL_HOST='127.0.0.1'  #在setting中配置数据库文件
MYSQL_DBNAME='movie'
MYSQL_USER='root'
MYSQL_PASSWORD='123'

SQL_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
SQL_DATE_FORMAT = "%Y-%m-%d"

RANDOM_USER_AGENT='random'    #我们可以在此处设置使用哪个浏览器的user agent