# -*- coding: utf-8 -*-
# @Time    : 2020/6/19 23:31
# @Author  : QiBin Lin
# @Email   : lqb9988@gmail.com
# @File    : db.py

import pymysql

class dbmysql(object):
    def __init__(self):
        # 建立连接
        self.conn = pymysql.connect('localhost', 'root', 'zz6369889', 'guba', 3306, charset='utf8')
        # 有中文要存入数据库的话要加charset='utf8'
        # 创建游标
        self.cursor = self.conn.cursor()

    def process_item(self, user_name, stock_id, date, time, equip, content,
                     like_count, comment_count, user_power, view_count, share_count):
        # sql语句
        insert_sql = """
        insert into comment(`user_name`, `stock_id`, `date`, `time`, `equip`, `content`, `like_count`, `comment_count`, 
        `user_power`, `view_count`, `share_count`) 
        VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s');
        """ % (user_name, stock_id, date, time, equip, content, like_count, comment_count,
               user_power, view_count, share_count)

        # 执行插入数据到数据库操作
        self.cursor.execute(insert_sql)

        # 提交，不进行提交无法保存到数据库
        self.conn.commit()
        print("\r写入完成", stock_id, date, end='')

    def close_db(self):
        # 关闭游标和连接
        self.cursor.close()
        self.conn.close()

