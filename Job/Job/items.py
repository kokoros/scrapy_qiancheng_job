# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

#要获取的字段
class JobItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job_name = scrapy.Field()
    job_url = scrapy.Field()
    company = scrapy.Field()
    company_url = scrapy.Field()
    address = scrapy.Field()
    #工资
    wage = scrapy.Field()
    #发布时间
    time = scrapy.Field()
    #职位信息
    job_intro = scrapy.Field()
    #联系方式
    telphone = scrapy.Field()
    #公司信息
    company_intro = scrapy.Field()
    #mongo
    _id = scrapy.Field()





