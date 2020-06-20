# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from twisted.enterprise import adbapi


class MysqlPipeline(object):
    """
    同步操作
    """
    def __init__(self):
        # 建立连接
        self.conn = pymysql.connect('localhost','root','zz6369889','guba',3306,charset='utf8')  # 有中文要存入数据库的话要加charset='utf8'
        # 创建游标
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        # sql语句
        insert_sql = """
        insert into comment(url,name,stock_id,tag,author,read_count,comment_count,date,time,shebei,title,detail,
        send_count,user_year,user_power)
         VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        # 执行插入数据到数据库操作
        self.cursor.execute(insert_sql, ((item['url'],
                                    item['name'],
                                    item['stock_id'],
                                    item['tag'],
                                    item['author'],
                                    item['read_count'],
                                    item['comment_count'],
                                    item['date'],
                                    item['time'],
                                    item['shebei'],
                                    item['title'],
                                    item['detail'],
                                    item['send_count'],
                                    item['user_year'],
                                    item['user_power'])))
        #提交，不进行提交无法保存到数据库
        self.conn.commit()

    def close_spider(self, spider):
        # 关闭游标和连接
        self.cursor.close()
        self.conn.close()

