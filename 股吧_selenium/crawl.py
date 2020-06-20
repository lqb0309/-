# -*- coding: utf-8 -*-
# @Time    : 2020/6/18 22:18
# @Author  : QiBin Lin
# @Email   : lqb9988@gmail.com
# @File    : crawl.py


from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.options import Options
import time
import re
from datetime import datetime
import redis
import pandas as pd
from lxml import etree
from db import dbmysql
from multiprocessing import Pool

# C:\Users\49296\anaconda3
    # 1.创建浏览器对象

conn = redis.StrictRedis(host='localhost', port=6379, db=12)


def get_url():
    stock_url = {}
    stock_ids = pd.read_excel(r"D:\data\stockCODE.xlsx", sheet_name=0)['id']
    stock_ids = stock_ids[:4]
    for stock_id in stock_ids:
        url = 'http://guba.eastmoney.com/concept/list,{}.html'.format(stock_id)
        # ex = conn.sadd('urls', url)
        # if ex == 1:
        stock_url[stock_id] = url
    return stock_url


# 2.请求页面
def parse(url):
    # 实现无可视化界面的操作
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    # 实现规避检测
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])

    # driver = webdriver.Chrome(chrome_options=chrome_options, options=option)
    driver = webdriver.Chrome()
    driver.get(url)
    database = dbmysql()

    # 3.页面基本操作(点击\输入)
    driver.find_element_by_xpath('//*[@id="guide_wrap"]/div[1]').click()
    driver.find_element_by_xpath('//*[@id="guide_wrap"]/div[2]').click()
    diff = 1
    i = 1
    while diff > 0:
        try:
            driver.find_element_by_xpath('//*[@id="list_cont"]/div[2]/div[1]/div').click()
            time.sleep(0.2)
            date = driver.find_element_by_xpath(
                '//*[@id="list_cont"]/div[1]/div[%s]/div[1]/div[1]/div/div[1]/span[2]/span' % (i)).text
            date = re.findall("(\d{4}-\d{1,2}-\d{1,2})", date)[0]
            date = datetime.strptime(date, '%Y-%m-%d')
            date_judge = datetime.strptime('2019-01-01', '%Y-%m-%d')
            diff = (date - date_judge).days
            print("\r", date, end='')
            i += 1
            if i % 200 == 0:
                time.sleep(10)
        except:
            pass
        continue

    # 获取item
    source = driver.page_source
    tree = etree.HTML(source)
    stock_id = tree.xpath('//*[@id="stock_quote"]/div[1]/h2/text()')[0]
    stock_id = re.findall('(\d{6})', stock_id)[0]
    item_list = tree.xpath('//*[@id="list_cont"]/div[1]/div')
    for item in item_list:
        div_list = item.xpath('./div')
        # 解析内容
        for div in div_list:
            user_name =div.xpath('.//a[@class="user_name"]/text()')[0]
            equip = div.xpath('.//div[@class="publish_from"]/text()')[0]
            equip = equip.split(" ")[1]
            user_power = div.xpath('.//div[@class="influence"]/span/@class')[0]
            content = div.xpath('.//div[@class="post_cont"]/a/text()')
            content2 = div.xpath('.//div[@class="post_cont"]/text()')
            if content and content[0] != "[查看全文]":
                content = content
            else:
                content = content2
            if content:
                content = content[0]
            date_time = div.xpath('.//span[@class="publish_info"]/span/text()')[0]
            date = re.findall("(\d{4}-\d{1,2}-\d{1,2})", date_time)[0]
            time1 = re.findall("(\d{2}:\d{1,2}:\d{1,2})", date_time)[0]
            comment_count = div.xpath('./ul[@class="social clearfix"]/li[4]/@data-replycount')[0]
            like_count = div.xpath('./ul[@class="social clearfix"]/li[5]/a/span/text()')[0]
            share_count = div.xpath('./ul[@class="social clearfix"]/li[3]/a/text()')[0]
            view_count = div.xpath('./ul[@class="social clearfix"]/li[1]/a/text()')[0]
            database.process_item(user_name, stock_id, date, time1, equip, content, like_count,
                                  comment_count, user_power, view_count, share_count)
    database.close_db()
    driver.close()  # 关闭页面
    driver.quit()


# url = get_url().values()
# for url in url:
#     print(url)
#     parse(url)


if __name__ == '__main__':
    start_time = time.time()
    print('mainProcess start:', start_time)
    url = get_url().values()
    pool = Pool(4)  # 开了10个进程，同时执行的只有4个，其它6个处于挂起状态
    for i in url:
        pool.apply_async(func=parse, args=(i,))
    pool.close()
    pool.join()  # 必须等待所有子进程结束
    print('mainProcess done time:%s s' % (time.time() - start_time))
