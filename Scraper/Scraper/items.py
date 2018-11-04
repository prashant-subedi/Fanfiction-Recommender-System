# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class MinimalScraperItem(scrapy.Item):
    # define the fields for your item here like:
    fanfic_id = scrapy.Field()
    author_id = scrapy.Field()   
    fanfic_name = scrapy.Field()
    author = scrapy.Field()
    summary = scrapy.Field()    
    rating = scrapy.Field()
    language = scrapy.Field()
    genere = scrapy.Field()
    chapters_count = scrapy.Field()
    word_count = scrapy.Field()
    review_count = scrapy.Field()
    fav_count = scrapy.Field()
    follow_count = scrapy.Field()
    update_date = scrapy.Field()
    publish_date = scrapy.Field()
    main_characters = scrapy.Field()   
    completion_status = scrapy.Field()
