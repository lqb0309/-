# -*- coding: utf-8 -*-
# @Time    : 2020/6/13 2:13
# @Author  : QiBin Lin
# @Email   : lqb9988@gmail.com
# @File    : main.py


from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy","crawl","guba1"])