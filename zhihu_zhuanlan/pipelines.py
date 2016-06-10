# -*- coding: utf-8 -*-

from zhihu_zhuanlan.items import UserItem, PostItem
from scrapy.exceptions import DropItem
import psycopg2
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DBPipeline(object):
    """
    Store items into postgreSQL database with psycopg2
    """
    InsertUserItemSql = ""
    InsertPostItemSql = ""

    def open_spider(self, spider):
        self.conn = psycopg2.connect('dbname=zhihu user=MiniBear')
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):
        # insert item into database table
        if isinstance(item, UserItem):
            self.cur.execute()
            return item
        elif isinstance(item, PostItem):
            return item
        else:
            raise DropItem('Item class is incorrect')
