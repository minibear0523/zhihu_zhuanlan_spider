# -*- coding: utf-8 -*-

from zhihu_zhuanlan.items import UserItem, PostItem
from scrapy.exceptions import DropItem
import psycopg2
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
InsertUserItemSql = "INSERT INTO author (hash, bio, name, slug, description) VALUES (%s, %s, %s, %s, %s);"
InsertPostItemSql = "INSERT INTO post (source_url, url, title, title_image, summary, content, href, slug, likes_count, comments_count, author) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"


def format_item_sql(item):
    if isinstance(item, UserItem):
        return item['hash'], item['bio'], item['name'], item['slug'], item['description']
    elif isinstance(item, PostItem):
        return item['source_url'], item['url'], item['title'], item['title_image'], item['summary'], item['content'], \
               item['href'], item['slug'], item['likes_count'], item['comments_count'], item['author_hash']
    else:
        return None


class DBPipeline(object):
    """
    Store items into postgreSQL database with psycopg2
    """
    def open_spider(self, spider):
        self.conn = psycopg2.connect('dbname=zhihu user=MiniBear')
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):
        # insert item into database table
        if isinstance(item, UserItem):
            try:
                self.cur.execute(InsertUserItemSql, format_item_sql(item))
                self.conn.commit()
            except psycopg2.DatabaseError:
                self.conn.rollback()
            return item

        elif isinstance(item, PostItem):
            try:
                self.cur.execute(InsertPostItemSql, format_item_sql(item))
                self.conn.commit()
            except psycopg2.DatabaseError:
                self.conn.rollback()
            return item

        else:
            raise DropItem('Item: %s class is incorrect' % item)


class DuplicatesPipeline(object):
    def __init__(self):
        self.authors = set()
        self.posts = set()

    def process_item(self, item, spider):
        if isinstance(item, UserItem):
            if item['hash'] in self.authors:
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.authors.add(item['hash'])
                return item
        elif isinstance(item, PostItem):
            if item['slug'] in self.posts:
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.posts.add(item['slug'])
                return item
        else:
            raise DropItem("Item: %s class is incorrect" % item)
