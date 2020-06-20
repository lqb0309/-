# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
from tqdm import tqdm
from guba.items import GubaItem
import redis
from datetime import datetime


class Guba1Spider(scrapy.Spider):
    name = 'guba1'
    conn = redis.StrictRedis(host='localhost', port=6379, db=12)

    def get_stock_ids(self):
        stock_ids = pd.read_excel(r"D:\data\stockCODE.xlsx",sheet_name=0)['id']
        stock_ids = stock_ids[:]
        return stock_ids

    def start_requests(self):
        stock_ids = self.get_stock_ids()

        for stock_id in tqdm(stock_ids):
            print('stock ->', stock_id)
            for page in range(1, 250):
                url = 'http://guba.eastmoney.com/list,{},f_{}.html'.format(stock_id, page)
                ex = self.conn.sadd('urls', url)
                if ex == 1:
                    yield scrapy.Request(url=url, callback=self.date_judge, dont_filter=True, meta={'stock_id': stock_id,
                                                                                               'urls': url})

    #检测符合日期的页数
    def date_judge(self,response):
        div = response.xpath('//*[@id="articlelistnew"]/div')[8]
        stock_id = response.meta['stock_id']
        url = response.meta['urls']
        date_url = 'http://guba.eastmoney.com' + str(div.xpath('./span[3]/a/@href').extract_first())
        yield scrapy.Request(url=date_url, callback=self.date_judge2, dont_filter=True, meta={'stock_id': stock_id,
                                                                                   'urls': url})

    def date_judge2(self, response):
        stock_id = response.meta['stock_id']
        url = response.meta['urls']
        date_shebei = response.xpath('//*[@id="zwconttb"]/div[2]/text()').getall()[0]
        date = date_shebei.split(' ')[1]
        date = datetime.strptime(date, '%Y-%m-%d')
        date_judge = datetime.strptime("2019-05-01", '%Y-%m-%d')
        if (date - date_judge).days > 0:
            print(date, "符合")
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True, meta={'stock_id': stock_id,
                                                                                            'urls': url})
        else:
            print(date, "不符合,pass")
            pass

    def parse(self, response):
        conn = redis.StrictRedis(host='localhost', port=6379, db=12)

        div_list = response.xpath('//*[@id="articlelistnew"]/div')
        url = response.meta['urls']
        for div in div_list:
            name = response.xpath('//*[@id="stockname"]/a/text()').extract_first()
            tag = div.xpath('./span[3]/em[1]/text()').extract_first()
            if name == "股民学校吧" and name == "财经评论吧":
                conn.srem('urls', url)
            if tag is None:
                read_count = div.xpath('./span[1]/text()').extract_first()
                comment_count = div.xpath('./span[2]/text()').extract_first()
                title = div.xpath('./span[3]/a/@title').extract_first()
                url = 'http://guba.eastmoney.com' + str(div.xpath('./span[3]/a/@href').extract_first())
                author = div.xpath('./span[4]/a/font/text()').extract_first()
                item = GubaItem()
                item['name'] = name
                item['tag'] = tag
                item['stock_id'] = response.meta['stock_id']
                item['read_count'] = read_count
                item['comment_count'] = comment_count
                item['title'] = title
                item['url'] = url
                item['author'] = author
                yield response.follow(url, callback=self.parse_content, meta=item)

    def parse_content(self, response):
        item = response.meta
        date_shebei = response.xpath('//*[@id="zwconttb"]/div[2]/text()').getall()[0]
        date = date_shebei.split(' ')[1]
        time = date_shebei.split(' ')[2]
        shebei = date_shebei.split(' ')[3]
        detail = response.xpath('//*[@id="zwconbody"]/div/div/p/text()').extract()
        detail = ''.join(detail)
        send_count = response.xpath('//*[@id="popperson"]/div/div[2]/span[1]/b/text()').extract_first()
        user_year = response.xpath('//*[@id="zwconttbn"]/div/@data-user_age').extract_first()
        user_power = response.xpath('//*[@id="zwconttbn"]/div/@data-user_level').extract_first()
        item['detail'] = detail
        item['date'] = date
        item['time'] = time
        item['shebei'] = shebei
        item['send_count'] = send_count
        item['user_year'] = user_year
        item['user_power'] = user_power
        print(item['name'], item['stock_id'], date, shebei, send_count, user_year, user_power)
        yield item

