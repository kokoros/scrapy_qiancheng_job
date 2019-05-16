# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

#导入mongodb
import pymongo

#导入redis
import redis
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
        # 变量引用自settings
        self.conn = pymongo.MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)
        #库对象
        self.db = self.conn[settings.MONGO_DB]
        #集合对象
        self.myset = self.db['job']
        #清除集合
        self.myset.remove()
        print('删除mongo中job集合完毕,准备录入新数据...')

        # 连接redis
        # 连接redis数据库 设为存入的是字符串
        pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0, decode_responses=True)
        r = redis.Redis(connection_pool=pool)

        # 查询集合所有元素
        set_list = r.smembers('ip_port')
        # print(set_list)
        #把可用ip 存入proxylist文件
        with open('./Job/proxylist.py', 'w') as f:
            f.write("proxy_list = [")
            print("??")
            for set in set_list:
                #转为元祖
                i = eval(set)
                # print(type(i))
                ip = i[0]
                port = i[1]
                # print(ip, port)
                f.write("'http://{}:{}',".format(ip, port))
            f.write("]")
        print('成功导入可用ip')

    def process_item(self, item, spider):
        #插入数据
        self.myset.insert_one(item)
        return item

    # 爬虫结束时,只执行一次
    # 一般用于断开数据库连接
    def close_spider(self, spider):
        self.conn.close()
        print('我是close_spider函数')
