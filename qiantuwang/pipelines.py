# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import urllib
import random
class QiantuwangPipeline(object):
    def process_item(self, item, spider):
        try:
            title = item['title'][0].encode('gbk')
            file = "E:/tupian/" + str(title) + str(int(random.random() * 10000)) + ".jpg"
            urllib.urlretrieve(item['url'][0], filename=file)
        except Exception, e:
            print e
            pass
        return item