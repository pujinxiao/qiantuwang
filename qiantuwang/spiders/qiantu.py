# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from qiantuwang.items import QiantuwangItem
jishu=1

class QiantuSpider(scrapy.Spider):
    name = "qiantu"
    allowed_domains = ["58pic.com"]
    start_urls = (
        'http://www.58pic.com/new/',
    )

    # 分析获取大类的url
    def parse(self, response):
        urldata = response.xpath('//div[@class="classify clearfix"]/a/@href').extract()  # 一共是62种类别
        print urldata
        for i in range(0, len(urldata)):
            thisurldata = urldata[i]
            yield Request(url=thisurldata, callback=self.next1)

    # 获取大类的每一页的url
    def next1(self, response):
        thisurl = response.url
        pagelist = response.xpath("//div[@id='showpage']/a/text()").extract()
        if (len(pagelist) >= 3):
            page = pagelist[-3]
            for j in range(1, int(page) + 1):
                pageurl = thisurl.replace('day-1', 'day-' + str(j))
                yield Request(url=pageurl, callback=self.next2)
        else:
            pass

    # 获取每一张图片，详细的url
    def next2(self, response):
        url_erery = response.xpath("//a[@class='thumb-box']/@href").extract()  # 第一种
        if url_erery == []:  # 缩略图链接的网页结构有两种
            url_erery = response.xpath('//div[@class="list fl"]/a/@href').extract()  # 第二种
        # print url_erery
        for k in url_erery:
            yield Request(url=k, callback=self.getimg)

    # 得到高清图的url
    def getimg(self, response):
        global jishu
        print("此时正爬取第" + str(jishu) + "个图片---" + response.url + "----")
        item = QiantuwangItem()
        # 详细页有三种结构
        item['title'] = response.xpath('//div[@class="show-area-pic"]/img/@title').extract()  # 第一种
        item['url'] = response.xpath('//div[@class="show-area-pic"]/img/@src').extract()
        if item['title'] == []:
            item['title'] = response.xpath('//div[@class="show-area-pic"]/div/img/@title').extract()  # 第二种
        if item['url'] == []:
            item['url'] = response.xpath('//div[@class="show-area-pic"]/div/img/@src').extract()
        if item['title'] == []:
            item['title'] = response.xpath('//div[@class="pic-show hidden"]/div/img/@title').extract()  # 第三种
        if item['url'] == []:
            item['url'] = response.xpath('//div[@class="pic-show hidden"]/div/img/@src').extract()
        # print item['title'][0],item['url'][0]
        jishu += 1
        yield item
