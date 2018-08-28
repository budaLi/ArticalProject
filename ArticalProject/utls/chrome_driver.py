#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/18
from selenium import webdriver


#不加载图片
# chrome_opt=webdriver.ChromeOptions()
# pres={'profile.managed_default_content_settings.images':2}
# chrome_opt.add_experimental_option('prefs',pres)
# browser=webdriver.Chrome(chrome_options=chrome_opt)
# browser.get('https://www.taobao.com')


browser=webdriver.PhantomJS()       #phantomJs
browser.get('https://www.taobao.com')
print(browser.page_source)
browser.quit()