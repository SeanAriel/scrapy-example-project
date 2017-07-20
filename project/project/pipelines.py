# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class TestPipeline(object):
    def process_item(self, item, spider):
        item['upper_name'] = item['name'].upper()
        return item
