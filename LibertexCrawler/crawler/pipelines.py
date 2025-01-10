# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from scrapy.exporters import JsonItemExporter
import datetime

class CrawlerPipeline:
    def process_item(self, item, spider):
        return item

#class JsonExportPipeline(object):
#    def __init__(self):
#        timestamp = datetime.datetime.now()
#        timestamp = timestamp.strftime('%d-%m-%Y_%H-%M-%S')
#        self.file = open("output_" + timestamp + ".json", 'wb')
#        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
#        self.exporter.start_exporting()

#    def close_spider(self, spider):
#        self.exporter.finish_exporting()
#        self.file.close()

#    def process_item(self, item, spider):
#        self.exporter.export_item(item)
#        return item
