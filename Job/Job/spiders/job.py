# -*- coding: utf-8 -*-
import scrapy
#导入items
from ..items import JobItem


class JobSpider(scrapy.Spider):
    name = 'job'
    allowed_domains = ['search.51job.com', 'jobs.51job.com']
    # start_urls = ['http://search.51job.com/']

    # def parse(self, response):
    #    pass

    #因为不想要先丢个url再爬取,所以这里要重写方法
    #重写Spider类中的start_requests方法
    def start_requests(self):
       
        key = input('请输入职位名称:')
        self.job_size = 1
        page = 1
        #先爬50页
        while page < 51:
            url = 'https://search.51job.com/list/000000%252C00,000000,0000,00,9,99,{},2,{}.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='.format(key, str(page))
            #把url地址入队列
            yield scrapy.Request(
                url=url,
                #解析函数
                callback=self.parse_job
            )
            page += 1

    #解析出一级页面
    def parse_job(self, response):
        # print(response.text)
        for i in range(1, 51):
            #每个工作的总列表
            one_job_list = response.xpath('//div[@class="dw_table"]/div[@class="el"][{}]'.format(str(i)))
            # print(one_job_list)
            #遍历工作列表
            for one_job in one_job_list:
                #创建item对象
                item = JobItem()
                item['job_name'] = one_job.xpath('./p//a/text()').extract_first().strip()
                item['job_url'] = one_job.xpath('./p//a/@href').extract_first().strip()
                item['company'] = one_job.xpath('./span/a[@target="_blank"]/text()').extract_first().strip()
                item['company_url'] = one_job.xpath('./span/a[@target="_blank"]/@href').extract_first().strip()
                item['address'] = one_job.xpath('./span[@class="t3"]/text()').extract_first().strip()
                wage = one_job.xpath('./span[@class="t4"]/text()')
                if wage:
                    item['wage'] = one_job.xpath('./span[@class="t4"]/text()').extract_first().strip()
                else:
                    item['wage'] = ''
                item['time'] = one_job.xpath('./span[@class="t5"]/text()').extract_first().strip()
                item['_id'] = item['job_name'] + str(self.job_size)
                # print(item)
                #把工作链接丢到队列中
                yield scrapy.Request(
                    item['job_url'],
                    # 传参
                    meta={'item': item},
                    # 解析函数
                    callback=self.parse_one_job
                )
                self.job_size += 1

    #解析二级界面,获取工作具体信息
    def parse_one_job(self, response):
        # print(response.text)
        #获取参数
        item = response.meta['item']
        job_list = response.xpath('//div[@class="tCompany_main"]//span[@class="bname"]/text()')
        for i in job_list:
            str_key = i.extract().strip()
            # print(str_key)
            if str_key == '职位信息':
                job_intro = response.xpath('//div[@class="tCompany_main"]//div[@class="bmsg job_msg inbox"]/p/text()').extract()
                # print(job_intro)
                job_str = ''
                for job in job_intro:
                    job_str += job
                # print(job_str)
                item['job_intro'] = job_str.strip()
            elif str_key == '联系方式':
                #
                telphone = response.xpath('//div[@class="tCompany_main"]//div[@class="bmsg inbox"]/p/text()').extract()
                telphone_str = ''
                for i in telphone:
                    telphone_str += i
                item['telphone'] = telphone_str.strip()
                # print(telphone_str.strip())
            elif str_key == '公司信息':
                #
                company_intro = response.xpath('//div[@class="tmsg inbox"]/text()').extract()
                company_str = ''
                for i in company_intro:
                    company_str += i
                # print(company_str.strip())
                item['company_intro'] = company_str.strip()
        yield item




