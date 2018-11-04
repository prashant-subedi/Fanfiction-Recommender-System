# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient

class MinimalScraperMongoPipeline(object):
    def open_spider(self,spider):
        self.client = MongoClient()
        self.db = self.client.fanfiction_scrape

    def close_spider(self,spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db.minimal.update({'fanfic_id':item['fanfic_id']},dict(item),upsert=True)
