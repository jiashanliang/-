# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AutohomeAppItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    brand_id = scrapy.Field()
    brand_name = scrapy.Field()
    serialId = scrapy.Field()
    serialName = scrapy.Field()
    AverageRating = scrapy.Field()
    ResultBad = scrapy.Field()
    ResultGood = scrapy.Field()
    Koubeiid = scrapy.Field()
    goodContent = scrapy.Field()
    badContent = scrapy.Field()