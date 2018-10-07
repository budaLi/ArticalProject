爬虫集合
==============
scrapy爬虫的一些小项目。
更新了数据库文件，需要在自己本地建对应的数据库进行配置，运行对应的sql文件即可。
由于已经配置好了请求头伪造和ip更换，下面的项目无特殊说明均是在scrapy基础上的，请您在有一定的scrapy基础上使用该项目。

#伯乐在线爬虫
[伯乐](https://github.com/152056208/ArticalProject/blob/master/ArticalProject/spiders/jobble.py)
#存储图片时需要在settings中设置pipeline 取消注释即可


#知乎爬虫
[知乎](https://github.com/152056208/ArticalProject/blob/master/ArticalProject/spiders/zhilian.py)
#有对应的问题爬虫和答案爬虫，登陆时使用selenium登陆，需耐心等待。

#腾讯视频爬虫
[腾讯视频](https://github.com/152056208/ArticalProject/blob/master/ArticalProject/spiders/movie.py)
#爬取腾讯视频，并使用第三方视频播放地址拼接播放地址，会员视频也可以看的哦
[福利](http://yun.baiyug.cn/)
腾讯，爱奇艺各大视频网站视频均可以解析,会员视频免费看~~~


#实习僧爬虫
[实习僧](https://github.com/152056208/ArticalProject/blob/master/ArticalProject/spiders/shixiseng.py)
#爬取实习僧网站的招聘信息，不过职位好像比其他招聘网站少
#发现实习僧网站对显示的数字和字体做了一定的加密，有时需要自己更改对应的字典信息。在这里修改。
[配置对应字体](https://github.com/budaLi/ArticalProject/blob/master/ArticalProject/utls/common.py)

如图:

![Image text](https://github.com/budaLi/ArticalProject/blob/master/tools/QM%40DG1O~%245XOKP127WXI4%7DJ.png)



#拉钩网爬虫
[拉钩](https://github.com/152056208/ArticalProject/blob/master/ArticalProject/spiders/lagou.py)

#爬取西刺免费ip代理
[西刺](https://github.com/152056208/ArticalProject/blob/master/tools/crawl_xici_ip.py)
#还是挺好用的，先用自己的ip爬几个ip，然后暂停，再次运行即可使用爬取的ip再次爬取,注意不要用自己ip爬取太多次，不然会被封

#美女写真图片 
[美女写真](https://github.com/budaLi/ArticalProject/blob/master/ArticalProject/spiders/meizi_pic.py)
#能爬5000张左右

#小说爬取
[小说](https://github.com/budaLi/ArticalProject/blob/master/ArticalProject/spiders/xiaoshuo.py)
#佛曰不可说，别举报我

#qq好友爬虫
[qq好友爬虫](https://github.com/budaLi/ArticalProject/blob/master/tools/get_qq.py)
#抓取自己的所有qq好友信息，将对应信息入库，方便以后对空间说说进行爬取或者分析好友关系等。

#bilibili用户爬虫
[bilibili用户爬虫](https://github.com/budaLi/ArticalProject/tree/master/bilibili-user-master)
#发现B站的用户id是从1开始的，然后自己穷举，可以在文件中设置要爬取的id范围，由于此文件是clone别人的，请求头伪造和ip并没有使用scrapy中配置好的信息。

#github模拟登陆
[github模拟登陆](https://github.com/budaLi/ArticalProject/blob/master/tools/github%E7%99%BB%E9%99%86.py）
#抱着坦白从宽的原则，在这里沉重道歉，以为自己发现了star的漏洞，刷了几十个star不久就全给消灭了，正所谓道高一尺魔高一丈，我服了。。老老实实敲自己的代码吧
