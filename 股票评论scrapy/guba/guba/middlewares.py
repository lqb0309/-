# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import UserAgent
import random
import requests

class GubaDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    def process_request(self, request, spider):
        # proxy = requests.get("http://127.0.0.1:5010/get/").json().get("proxy")
        header = UserAgent()
        request.headers['User-Agent'] = header.random
        # request.meta['proxy'] = "http://{}".format(proxy)

        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # current_proxy = request.meta.get('proxy', False)
        # requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(current_proxy))
        #
        # proxy = requests.get("http://127.0.0.1:5010/get/").json().get("proxy")
        # header = UserAgent()
        # request.headers['User-Agent'] = header.random
        # request.meta['proxy'] = "http://{}".format(proxy)
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
