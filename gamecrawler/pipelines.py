# -*- coding: utf-8 -*-

from scrapy import signals
from scrapy.exporters import CsvItemExporter

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class GamecrawlerExportPipeline(object):
    # def process_item(self, item, spider):
    #    return item
    def __init__(self):
        self.file = None
        self.exporter = None

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        if spider.name == 'game_info':
            self.file = open('data/games_info.csv', 'a+b')
            self.exporter = CsvItemExporter(self.file,
                                            fields_to_export=['title', 'title_safe', 'platform', 'publisher',
                                                              'developer', 'release_date', 'score_metacritic',
                                                              'score_users', 'rating', 'genres', 'summary'],
                                            delimiter='|')

        elif spider.name == 'game_reviews':
            self.file = open('data/games_reviews.csv', 'a+b')
            self.exporter = CsvItemExporter(self.file,
                                            fields_to_export=['title', 'title_safe', 'platform', 'reviewer',
                                                              'reviewer_type', 'score', 'review_date', 'review',
                                                              'review_url'],
                                            delimiter='|')
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
