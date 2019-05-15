# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

#导入mongodb
import pymongo
#导入设置文件
from . import settings

class JobPipeline(object):
    def process_item(self, item, spider):
        print(dict(item))
        return item

#新建管道类,存入mongodb
class JobMongoPipeline(object):
    # 在开启爬虫时执行,只执行一次
    # 一般用于开启数据库
    def open_spider(self, spider):
        print('我是open_spider函数')
        # 变量引用自settings
        self.conn = pymongo.MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)
        #库对象
        self.db = self.conn[settings.MONGO_DB]
        #集合对象
        self.myset = self.db['job']

    def process_item(self, item, spider):
        #插入数据
        self.myset.insert_one(item)
        return item

    # 爬虫结束时,只执行一次
    # 一般用于断开数据库连接
    def close_spider(self, spider):
        self.conn.close()
        print('我是close_spider函数')
