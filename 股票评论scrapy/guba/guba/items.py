# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GubaItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    author = scrapy.Field()
    tag = scrapy.Field()
    url = scrapy.Field()
    read_count = scrapy.Field()
    comment_count = scrapy.Field()
    title = scrapy.Field()
    stock_id = scrapy.Field()
    date = scrapy.Field()
    detail = scrapy.Field()
    shebei = scrapy.Field()
    time = scrapy.Field()
    send_count = scrapy.Field()
    user_year = scrapy.Field()
    user_power = scrapy.Field()

