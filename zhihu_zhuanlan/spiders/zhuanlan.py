# -*- coding: utf-8 -*-
import scrapy


class ZhuanlanSpider(scrapy.Spider):
    name = "zhuanlan"
    allowed_domains = ["zhihu.com"]
    start_urls = (
        'http://www.zhihu.com/',
    )

    def parse(self, response):
        pass
