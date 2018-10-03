# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import datetime
import re
import scrapy
from scrapy.loader.processors import MapCompose,TakeFirst,Join
from scrapy.loader import ItemLoader
from ArticalProject.utls.common import extract_num,remove_xiexian,get_finally,get_per_week,get_salary#这里的路径要弄清楚
from ArticalProject.settings import SQL_DATE_FORMAT, SQL_DATETIME_FORMAT#路径
class ArticalprojectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

def add_jobbole(value):
    return value


class ArticleItemLoder(ItemLoader):     #自定义输出
    pass

def date_convert(value):
        try:
            create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()#date类型不可调用json.dumps 进行序列化
        except Exception as e:
            create_date = datetime.datetime.now().date()
        return create_date

def get_nums(value):
        match_re = re.match(".*?(\d+).*", value)
        if match_re:
            nums = int(match_re.group(1))
        else:
            nums = 0
        return nums
def remove_comment_tags(value):
    if '评论' in value:
        return ''
    else:
        return value
def return_value(value):        #用来覆盖out_proecessor
    return value

def split_years(value):     #例如 经验1-5年 如何提取 1年
    math_re=re.match('.*(\d+).*?',value)    #把1提取+年
    if math_re:
        return math_re.group(1)+'年'


class JobboleArticalItem(scrapy.Item):
    title=scrapy.Field(   #可以对数据进行预处理 对每一个数据都进行自定义处理，可以传入多个函数
    )
    create_date=scrapy.Field(
        input_processor=MapCompose(date_convert),
        # output_processor=TakeFirst()        #from scrapy.loader.processor import TakeFirst() 只要第一个
    )
    url=scrapy.Field()
    url_object_id=scrapy.Field()
    front_image_url=scrapy.Field(
        output_processor=MapCompose(return_value)   #覆盖
    )
    front_image_path=scrapy.Field()
    praise_nums=scrapy.Field(
        input_processor=MapCompose(get_nums),
    )
    comment_nums=scrapy.Field(
        input_processor=MapCompose(get_nums),
    )
    fav_nums=scrapy.Field(
        input_processor=MapCompose(get_nums),
    )
    tags=scrapy.Field(
        input_processor=MapCompose(remove_comment_tags),
        output_processor=Join(',')
    )
    content=scrapy.Field(
        input_processor=MapCompose(return_value),
        out_processor=MapCompose(return_value)      #否则取值不全
    )
    def get_insert_sql(self):
        #插入表的sql语句
        insert_sql = """insert into article(title,create_date,url,url_object_id,front_image_url,front_image_path,comment_nums,fav_nums, praise_nums, tags,content) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
              ON DUPLICATE KEY UPDATE content=VALUES(content),praise_nums=VALUES(praise_nums),
              tags=VALUES(tags),comment_nums=VALUES(comment_nums)
        """
        title=''.join(self["title"])
        create_date=self["create_date"][0].strftime(SQL_DATE_FORMAT)
        url=''.join(self["url"])
        url_object_id=''.join(self["url_object_id"])
        front_image_url=''.join(self["front_image_url"])
        comment_nums=int(self["comment_nums"][0])
        fav_nums=int(self["fav_nums"][0])
        praise_nums=int(self["praise_nums"][0])
        tags=''.join(self["tags"])
        content=remove_xiexian(''.join(self['content']))
        # front_image_path=self["front_image_path"] if self["front_image_path"] else ''
        params = (
            title, create_date,url,
            url_object_id, front_image_url,'',
            comment_nums, fav_nums,
            praise_nums,tags,content
        )

        return insert_sql, params

#知乎问题
class ZhihuQuestionItem(scrapy.Item):
    #知乎的问题 item
    zhihu_id = scrapy.Field()
    topics = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    answer_num = scrapy.Field()
    comments_num = scrapy.Field()
    watch_user_num = scrapy.Field()
    click_num = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        #插入知乎question表的sql语句
        insert_sql = """
            insert into zhihu_question(zhihu_id, topics, url, title, content,answer_num,comment_num,
              watch_user_num, click_num, crawl_time
              )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE content=VALUES(content), answer_num=VALUES(answer_num), comment_num=VALUES(comment_num),
              watch_user_num=VALUES(watch_user_num), click_num=VALUES(click_num)
        """
        zhihu_id = self["zhihu_id"][0]
        topics = ",".join(self["topics"])
        url = self["url"][0]
        title = "".join(self["title"])
        if self["content"]:
            content = "".join(self["content"])
        else:
            content=''
        answer_num = extract_num("".join(self["answer_num"]))
        comments_num = extract_num("".join(self["comments_num"]))
        if len(self["watch_user_num"]) == 2:
            watch_user_num = extract_num(self["watch_user_num"][0])
            click_num = extract_num(self["watch_user_num"][1])
        else:
            watch_user_num = extract_num(self["watch_user_num"][0])
            click_num = 0
        crawl_time = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)
        params = (zhihu_id, topics, url, title, content, answer_num, comments_num,
                  watch_user_num, click_num, crawl_time)
        return insert_sql, params


class ZhihuAnswerItem(scrapy.Item):
    #知乎的问题回答item
    zhihu_id = scrapy.Field()
    url = scrapy.Field()
    question_id = scrapy.Field()
    author_id = scrapy.Field()
    content = scrapy.Field()
    parise_num = scrapy.Field()
    comments_num = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        #插入知乎answer表的sql语句
        insert_sql = """
            insert into zhihu_answer(zhihu_id,url,question_id,author_id,content,praise_num, comment_num,
              create_time, update_time, crawl_time
              ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
              ON DUPLICATE KEY UPDATE content=VALUES(content), comment_num=VALUES(comment_num), praise_num=VALUES(praise_num),
              update_time=VALUES(update_time)
        """

        create_time = datetime.datetime.fromtimestamp(self["create_time"]).strftime(SQL_DATE_FORMAT)
        update_time = datetime.datetime.fromtimestamp(self["update_time"]).strftime(SQL_DATE_FORMAT)
        params = (
            self["zhihu_id"], self["url"], self["question_id"],
            self["author_id"], self["content"], self["parise_num"],
            self["comments_num"], create_time, update_time,
            self["crawl_time"].strftime(SQL_DATETIME_FORMAT),
        )

        return insert_sql, params

class LagouJobItemLoader(ItemLoader):
    #自定义itemloader
    # default_output_processor = TakeFirst()
    pass




class LagouJobItem(scrapy.Item):
    title=scrapy.Field()
    url=scrapy.Field()
    url_object_id=scrapy.Field()
    salary_min=scrapy.Field()
    salary_max=scrapy.Field()
    job_city=scrapy.Field()
    work_years_min=scrapy.Field()
    work_years_max=scrapy.Field()
    degree_need=scrapy.Field()
    work_type=scrapy.Field()
    tags=scrapy.Field(
         out_processor=MapCompose(return_value)      #否则取值不全
    )
    publish_time=scrapy.Field()
    job_addvantage=scrapy.Field(
        out_processor=MapCompose(return_value)      #否则取值不全
    )
    job_desc=scrapy.Field(
         out_processor=MapCompose(return_value)
    )
    company_name=scrapy.Field()
    company_area=scrapy.Field(
        out_processor=MapCompose(return_value)
    )
    company_develop_state=scrapy.Field()
    company_url=scrapy.Field()
    company_scale=scrapy.Field()
    crawl_time = scrapy.Field()


    def get_insert_sql(self):
        if self['salary_min']:
            self['salary_min']=''.join(self['salary_min'])
            salary_min=remove_xiexian(self['salary_min'].split('-')[0]) if self['salary_min'].split('-')[0] else self['salary_min']
            salary_max=remove_xiexian(self['salary_min'].split('-')[1]) if self['salary_min'].split('-')[1] else self['salary_min']
        else:
            salary_min=salary_max=0
        try:
            job_city=remove_xiexian(''.join(self['job_city'])) if self['job_city'] else None
        except Exception as e:
            print(e)
            job_city=None
        try:
            work_years_min=split_years(''.join(self['work_years_min']).split('-')[0]) if ''.join(self['work_years_min']).split('-')[0] else '经验不限'
        except Exception as e:
            print(e)
            work_years_min='经验不限'
        try:
            work_years_max=remove_xiexian(''.join(self['work_years_min']).split('-')[1]) if ''.join(self['work_years_min']).split('-')[1] else '经验不限'
        except Exception as e:
            print(e.args)
            work_years_max='经验不限'
        try:
            tags=remove_xiexian('-'.join(self['tags']))
        except:
            tags=''
        publish_time=''.join(self['publish_time']).split(' ')[0] if ''.join(self['publish_time']).split(' ')[0] else self['publish_time']
        try:
            degree_need=remove_xiexian(''.join(self['degree_need']))
        except:
            degree_need='学历不限'
        try:
            job_desc=remove_xiexian(''.join(self['job_desc']))
        except:
            job_desc=None
        job_addvantage=''.join(self['job_addvantage'])
        try:
            work_type=self['work_type']
        except:
            work_type=''
        try:
            company_name=remove_xiexian(''.join(self['company_name']))
        except:
            company_name=''
        try:
            company_area='-'.join(self['company_area'][:-1])
        except:
            company_area=''
        try:
            company_url=''.join(self['company_url']) if self['company_url'] else None
        except:
            company_url=''
        try:
            company_scale=remove_xiexian(''.join(self['company_scale'])) if self['company_scale'] else None
        except:
            company_scale=''
        try:
            company_develop_state=remove_xiexian(''.join(self['company_develop_state']))
        except:
            company_develop_state=''
        crawl_time=datetime.datetime.now().strftime(SQL_DATE_FORMAT)
        insert_sql="""
                insert into lagou_job(title,url,url_object_id,salary_min,salary_max,job_city,work_years_min,work_years_max,degree_need,work_type,tags,publish_time,job_addvantage,job_desc,company_name,
                company_area,company_develop_state,company_url,company_scale,crawl_time) VALUE (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
               on DUPLICATE KEY UPDATE job_addvantage=VALUES(job_addvantage),job_desc=VALUES(job_desc),crawl_time=VALUES(crawl_time)
                """
        params=(
            self['title'],self['url'],self['url_object_id'],salary_min,salary_max,job_city,work_years_min,work_years_max,degree_need,
            work_type,tags,publish_time,job_addvantage,job_desc,company_name,company_area,
            company_develop_state,company_url,company_scale,crawl_time
        )


        return insert_sql,params

class TianyanchaItem(scrapy.Item):
    company_name=scrapy.Field()
    url=scrapy.Field()
    url_object_id=scrapy.Field()
    tel=scrapy.Field()
    email=scrapy.Field()
    address=scrapy.Field()
    info=scrapy.Field()
    gong_shang_zhu_ce_hao=scrapy.Field()
    zu_zhi_ji_gou_dai_ma=scrapy.Field()
    tong_yi_xin_yong_dai_ma=scrapy.Field()
    company_type=scrapy.Field()
    na_shui_ren_shi_bie_hao=scrapy.Field()
    hang_ye=scrapy.Field()
    yin_ye_qi_xian=scrapy.Field()
    he_zhun_ri_qi=scrapy.Field()
    na_shui_ren_zi_zhi=scrapy.Field()
    ren_yuan_gui_mo=scrapy.Field()
    shi_jiao_zi_ben=scrapy.Field()
    deng_ji_ji_guan=scrapy.Field()
    can_bao_ren_shu=scrapy.Field()
    english_name=scrapy.Field()
    zhu_ce_di_zhi=scrapy.Field()
    jing_yin_fan_wei=scrapy.Field()

    def get_insert_sql(self):
        insert_sql="""insert into tianyancha(company_name,url,url_object_id,tel,email,address,info,gong_shang_zhu_ce_hao,
zu_zhi_ji_gou_dai_ma,tong_yi_xin_yong_dai_ma,na_shui_ren_shi_bie_hao,company_type,hang_ye,yin_ye_qi_xian,he_zhun_ri_qi,na_shui_ren_zi_zhi,ren_yuan_gui_mo,shi_jiao_zi_ben,deng_ji_ji_guan,can_bao_ren_shu,english_name,zhu_ce_di_zhi,jing_yin_fan_wei)
VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,)"""
        params=()
        return insert_sql,params

class ZhilianzhaopinItem(scrapy.Item):
    # url = scrapy.Field()
    # pname = scrapy.Field()
    # smoney = scrapy.Field()
    # emoney = scrapy.Field()
    # location = scrapy.Field()
    # syear = scrapy.Field()
    # eyear = scrapy.Field()
    # degree = scrapy.Field()
    # ptype = scrapy.Field()
    # tags = scrapy.Field()
    # date_pub = scrapy.Field()
    # advantage = scrapy.Field()
    # jobdesc = scrapy.Field()
    # jobaddr = scrapy.Field()
    # company = scrapy.Field()
    # crawl_time = scrapy.Field()


    def get_insert_sql(self):
        '''
        原来使用itemloader获取数据不太理想
        '''
        # salary_min,salary_max,work_min_years,work_max_years=0,0,0,0
        # url=self['url']
        # url_object_id=self['url_object_id']
        # title=self['all'][2]
        # if self['all'][3]:
        #     salary=''.join(self['all'][3])
        #     salary_min=salary.split('-')[0] if salary.split('-')[0] else 0
        #     salary_max=salary.split('-')[1] if salary.split('-')[1] else 0
        # years=''.join(self['all'][5])
        # work_min_years=years.split('-')[0] if years.split('-')[0] else '学历不限'
        # work_max_years=years.split('-')[1] if years.split('-')[1] else '学历不限'
        # # job_city=''.join(self['job_city'])
        # degree_need=''.join(self['all'][6])
        # job_addvantage=''.join(self['job_addvantage'])
        # job_info=''.join(self['job_addvantage'])
        # # company_name=''.join(self['company_name'])
        # # tags=('-'.join(self['tags']))
        # work_address=''.join(self['all'][10])
        # company_scale=''.join(self['all'][8])
        pass
        sql="""insert into zhilianzhaopin(url,url_object_id,pname,smoney,emoney,location,syear,eyear,degree,ptype,tags,date_pub,advantage,jobdesc,jobaddr,company,crawl_time)' \
            'VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        params=(self['url'],self['pname'],self['smoney'],self['emoney'],self['location'],self['syear'],self['eyear'],self['degree'],self['ptype'],self['tags'],self['date_pub'],self['advantage'],self['jobdesc'],self['jobaddr'],self['company'],self['crawl_time'])

        return sql,params


class ShixisengItem(scrapy.Item):
    url=scrapy.Field()
    url_object_id=scrapy.Field()
    title=scrapy.Field()
    upgrade_time=scrapy.Field()
    salary_min=scrapy.Field()
    salary_max=scrapy.Field()
    job_city=scrapy.Field()
    degree_need=scrapy.Field()
    work_per_week=scrapy.Field()
    shixi_time=scrapy.Field()
    job_addvantage=scrapy.Field()
    job_info=scrapy.Field()
    company_name=scrapy.Field()
    company_url=scrapy.Field()
    work_address=scrapy.Field()
    tags=scrapy.Field()
    company_scale=scrapy.Field()
    end_time=scrapy.Field()
    crawl_time=scrapy.Field()


    def get_insert_sql(self):
        url=''.join(self['url'])
        url_object_id=''.join(self['url_object_id'])
        if self['title']:
            title=remove_xiexian(''.join(self['title']))
        else:
            title=self['title']
        try:
            upgrade_time=get_finally(self['upgrade_time'])[10:]
        except:
            upgrade_time=0
        try:
            work_perweek=get_per_week(self['work_per_week'])
        except:
            work_perweek=0
        try:
            end_time=get_finally(self['end_time']).replace(',','')
        except:
            end_time=None
        try:
            shixi_time=get_finally(self['shixi_time']).replace('-','')+'个月'
        except:
            shixi_time=None
        try:
            salary=get_salary(self['salary_min'])
            salary_min=salary.split('-')[0] if salary.split('-')[0] else 0
            salary_max=salary.split('-')[1] if salary.split('-')[1] else 0
        except:
            salary_min=0
            salary_max=0
        try:
            company_url=''.join(self['company_url'])
        except:
            company_url=None
        job_city=''.join(self['job_city'])
        degree_need=''.join(self['degree_need'])
        job_addvantage=''.join(self['job_addvantage'])
        job_info=remove_xiexian(''.join(self['job_info']))
        company_name=''.join(self['company_name'])
        try:
            company_url=''.join(self['company_url'])
        except:
            company_url=None
        try:
            work_address=''.join(self['work_address'])
        except:
            work_address=None
        try:
            tags=self['tags'][1]+'-'+self['tags'][2]
            need_nums=self['tags'][1]
        except:
            tags=''.join(self['tags'])
            need_nums=0
        crawl_time=datetime.datetime.now().strftime(SQL_DATE_FORMAT)

        sql="""insert into shixiseng(url,url_object_id,title,upgrade_time,salary_min,salary_max,job_city,degree_need,work_perweek,shixi_time,job_addvantage,job_info,company_name,company_url,work_address,tags,need_nums,end_time,crawl_time) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        params=(url,url_object_id,title,upgrade_time,salary_min,salary_max,job_city,degree_need,work_perweek,shixi_time,job_addvantage,job_info,company_name,company_url,work_address,tags,need_nums,end_time,crawl_time)

        return sql,params


class MovieItem(scrapy.Item):
    url=scrapy.Field()
    url_object_id=scrapy.Field()
    main_title=scrapy.Field()
    title=scrapy.Field()
    tags=scrapy.Field()
    score1=scrapy.Field()
    score2=scrapy.Field()
    info=scrapy.Field()
    role=scrapy.Field()
    image_url=scrapy.Field()
    movie_url=scrapy.Field()

    def get_insert_sql(self):
        url=''.join(self['url'])
        url_object_id=self['url_object_id']
        try:
            main_title=remove_xiexian(''.join(self['main_title']))
        except:
            main_title=''
        try:
            title=main_title+remove_xiexian(''.join(self['title']))
        except:
            title=''
        try:
            tags=remove_xiexian(''.join(self['tags']))
        except:
            tags=''
        try:
            score=remove_xiexian(''.join(self['score1'])+''.join(self['score2']))
        except:
            score=0
        try:
            info=remove_xiexian(''.join(self['info']))
        except:
            info=0
        try:
            role='-'.join(self['role'])
        except:
            role=''
        try:
            image_url='--'.join(self['image_url'])
        except:
            image_url=''
        movie_url=self['movie_url']

        insert_sql="""insert into movie(url,url_object_id,title,tags,score,info,role,image_url,movie_url) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                   on duplicate KEY UPDATE info=VALUES(info) score=VALUES(score)"""
        params=(url,url_object_id,title,tags,score,info,role,image_url,movie_url)

        return insert_sql,params


class MeiziItem(scrapy.Item):
    image_url=scrapy.Field()
    front_image_path=scrapy.Field()


class XiaoshuoItem(scrapy.Item):
    title=scrapy.Field()
    content=scrapy.Field()

class VideoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 名字
    movie_name = scrapy.Field()
    # 一句话描述
    short_desc = scrapy.Field()
    # 评分
    score = scrapy.Field()
    # 主演
    stars = scrapy.Field()
    # 播放量
    hot = scrapy.Field()
    # 播放地址
    play_url = scrapy.Field()
    # 图片
    image_url = scrapy.Field()
    image_path=scrapy.Field()
    # 别名
    alias=scrapy.Field()
    # 导演
    director = scrapy.Field()
    # tag
    tags = scrapy.Field()
    # 简介
    description = scrapy.Field()
    # 播放时间
    play_time = scrapy.Field()
    crawl_time=scrapy.Field()
    def get_insert_sql(self):
        crawl_time=datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)
        description=remove_xiexian(self['description'])
        play_url='http://yun.baiyug.cn/vip/index.php?url='+self['play_url']
        insert_sql="""insert into tc_movie(movie_name,short_desc,score,stars,hot,play_url,image_url,image_path,alias,director,tags,description,play_time,crawl_time) VALUES
                      (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        params=[self['movie_name'],self['short_desc'],self['score'],self['stars'],self['hot'],play_url,self['image_url'],self['image_path'],self['alias'],self['director'],self['tags'],description,self['play_time'],crawl_time]

        return insert_sql,params


class CartoonItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url_object_id=scrapy.Field()
    # 名字
    movie_name = scrapy.Field()
    # 一句话描述
    short_desc = scrapy.Field()
    # 评分
    score = scrapy.Field()

    # 播放量
    hot = scrapy.Field()
    # 播放地址
    play_url = scrapy.Field()
    # 图片
    image_url = scrapy.Field()
    image_path=scrapy.Field()

    #集数
    jishu = scrapy.Field()

    # tag
    tags = scrapy.Field()
    # 简介
    description = scrapy.Field()
    # 播放时间
    play_time = scrapy.Field()
    crawl_time=scrapy.Field()
    def get_insert_sql(self):
        crawl_time=datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)
        description=remove_xiexian(self['description'])
        play_url='http://yun.baiyug.cn/vip/index.php?url='+self['play_url']
        insert_sql="""insert into cartoon_movie(url_object_id,movie_name,short_desc,score,hot,play_url,image_url,image_path,jishu,tags,description,play_time,crawl_time) VALUES
                      (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        params=[self['url_object_id'],self['movie_name'],self['short_desc'],self['score'],self['hot'],play_url,self['image_url'],self['image_path'],self['jishu'],self['tags'],description,self['play_time'],crawl_time]

        return insert_sql,params

class DoutuItem(scrapy.Item):
    image_title=scrapy.Field()
    image_url=scrapy.Field()
    image_path=scrapy.Field()

class WangyiyunItem(scrapy.Item):
    id=scrapy.Field()
    object_id=scrapy.Field()
    file_name=scrapy.Field()
    image_url=scrapy.Field()
    download_id=scrapy.Field()
    length=scrapy.Field()
    user=scrapy.Field()
    zhuanji=scrapy.Field()


