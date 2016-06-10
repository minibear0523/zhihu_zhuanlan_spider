# -*- coding: utf-8 -*-
# 先请求专栏首页, 获得其中的postCount, 然后再去访问对应的url来获取post list, 最后存入数据库.
import scrapy
import json
from zhihu_zhuanlan.items import UserItem, PostItem


HOST = 'https://zhuanlan.zhihu.com/api/columns/{}/posts?limit={}'
LIMIT_MAX = 100


class ZhuanlanSpider(scrapy.Spider):
    name = "zhuanlan"
    allowed_domains = ["zhihu.com"]
    start_urls = (
        'https://zhuanlan.zhihu.com/api/columns/eateateatonlyknoweat',
        'https://zhuanlan.zhihu.com/api/columns/eatalone',
        'https://zhuanlan.zhihu.com/api/columns/eatright',
        'https://zhuanlan.zhihu.com/api/columns/oh-hard',
        'https://zhuanlan.zhihu.com/api/columns/xiepanda',
        'https://zhuanlan.zhihu.com/api/columns/huizi',
        'https://zhuanlan.zhihu.com/api/columns/luzern',
        'https://zhuanlan.zhihu.com/api/columns/vivivvv',
    )

    def parse(self, response):
        """
        Parse columns data of zhuanlan, and then get postCounts, yield a new request for post list at last.
        """
        columns_data = json.loads(response.body)
        # User Item
        item = UserItem()
        item['profile_url'] = columns_data['creator']['profileUrl']
        item['bio'] = columns_data['creator']['bio']
        item['hash'] = columns_data['creator']['hash']
        item['name'] = columns_data['creator']['name']
        item['slug'] = columns_data['creator']['slug']
        item['description'] = columns_data['creator']['description']
        yield item

        # Yield Posts List Request
        post_count = columns_data['postsCount']
        slug = columns_data['slug']
        url = ''
        if post_count <= LIMIT_MAX:
            url = HOST.format(slug, post_count)
            yield scrapy.Request(url, callback=self.parse_posts_list)
        else:
            # postsCount > 100, split posts
            # yield request less than 100
            url = HOST.format(slug, LIMIT_MAX)
            yield scrapy.Request(url, callback=self.parse_posts_list)

            # yield request more than 100
            count = post_count / 100
            for i in range(1, count):
                url = HOST.format(slug, LIMIT_MAX) + "&offset=" + str(i * LIMIT_MAX)
                yield scrapy.Request(url, callback=self.parse_posts_list)

            # yield the rest request
            url = HOST.format(slug, post_count - count * 100) + "&offset=" + str(count * LIMIT_MAX)
            yield scrapy.Request(url, callback=self.parse_posts_list)

    def parse_posts_list(self, response):
        """
        Parse posts list data
        """
        posts_data = json.loads(response.body)
        for post in posts_data:
            item = PostItem()
            item['source_url'] = post['sourceUrl']
            item['url'] = post['url']
            item['title'] = post['title']
            item['title_image'] = post['titleImage']
            item['summary'] = post['summary']
            item['content'] = post['content']
            item['href'] = post['href']
            item['slug'] = post['slug']
            item['likes_count'] = post['likesCount']
            item['comments_count'] = post['commentsCount']
            item['author_hash'] = post['author']['hash']
            print item
            yield item
