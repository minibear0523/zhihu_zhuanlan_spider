# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class UserItem(Item):
    profile_url = Field()
    bio = Field()
    hash = Field()
    name = Field()
    slug = Field()
    description = Field()


class PostItem(Item):
    source_url = Field()
    url = Field()
    title = Field()
    title_image = Field()
    summary = Field()
    content = Field()
    href = Field()
    slug = Field()
    likes_count = Field()
    comments_count = Field()
    # author域记录user的hash
    author_hash = Field()
