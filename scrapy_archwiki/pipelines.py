# -*- coding: utf-8 -*-
from scrapy.exporters import JsonItemExporter

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

def item_type(item):
    return type(item).__name__.replace('Item', '').lower()

class ScrapyArchwikiPipeline(object):
    def process_item(self, item, spider):
        return item

class SaveItem2Files(object): 
    ItemTypes = ['archwikicategory', 'archwikipage']

    def open_spider(self, spider):
        self.files = dict([(name, open(name+'.json', 'w+b')) for name in self.ItemTypes])
        self.exporters = dict([(name, JsonItemExporter(self.files[name])) for name in self.ItemTypes])
        [e.start_exporting() for e in self.exporters.values()]

    def close_spider(self, spider):
        [e.finish_exporting() for e in self.exporters.values()]
        [f.close() for f in self.files.values()]

    def process_item(self, item, spider):
        what_item = item_type(item)
        if what_item in set(self.ItemTypes):
            self.exporters[what_item].export_item(item)
        return item
