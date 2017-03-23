相关代码已经修改调试----2017-3-21
实现：千图网上高清图片的爬取
程序运行20小时，爬取大约162000张图片，一共49G,存入百度云
spider.py
# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from second.items import SecondItem
jishu=1
class QiantuSpider(scrapy.Spider):
    name = "qiantu"
    allowed_domains = ["58pic.com"]
    start_urls = (
        'http://www.58pic.com/new/',
    )

    #分析获取大类的url
    def parse(self, response):
        urldata=response.xpath('//div[@class="classify clearfix"]/a/@href').extract()  #一共是62种类别
        print urldata
        for i in range(0,len(urldata)):
            thisurldata=urldata[i]
            yield Request(url=thisurldata,callback=self.next1)
    #获取大类的每一页的url
    def next1(self,response):
        thisurl=response.url
        pagelist=response.xpath("//div[@id='showpage']/a/text()").extract()
        if(len(pagelist)>=3):
            page=pagelist[-3]
            for j in range(1,int(page) + 1):
                pageurl=thisurl.replace('day-1','day-'+str(j))
                yield Request(url=pageurl,callback=self.next2)
        else:
            pass
    #获取每一张图片，详细的url
    def next2(self,response):
        url_erery=response.xpath("//a[@class='thumb-box']/@href").extract()   #第一种
        if url_erery==[]:       #缩略图链接的网页结构有两种
            url_erery=response.xpath('//div[@class="list fl"]/a/@href').extract()   #第二种
        #print url_erery
        for k in url_erery:
            yield Request(url=k,callback=self.getimg)
    #得到高清图的url
    def getimg(self,response):
        global jishu
        print("此时正爬取第"+str(jishu)+"个图片---"+response.url+"----")
        item=SecondItem()
        #详细页有三种结构
        item['title']= response.xpath('//div[@class="show-area-pic"]/img/@title').extract() #第一种
        item['url']= response.xpath('//div[@class="show-area-pic"]/img/@src').extract()
        if item['title']==[]:
            item['title']= response.xpath('//div[@class="show-area-pic"]/div/img/@title').extract()#第二种
        if item['url']==[]:
            item['url']= response.xpath('//div[@class="show-area-pic"]/div/img/@src').extract()
        if item['title']==[]:
            item['title']= response.xpath('//div[@class="pic-show hidden"]/div/img/@title').extract() #第三种
        if item['url']==[]:
            item['url']= response.xpath('//div[@class="pic-show hidden"]/div/img/@src').extract()
        #print item['title'][0],item['url'][0]
        jishu+=1
        yield item
item.py
# -*- coding: utf-8 -*-
import scrapy
class SecondItem(scrapy.Item):
    url=scrapy.Field()
    title=scrapy.Field()
setting.py
# -*- coding: utf-8 -*-

# Scrapy settings for second project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'second'

SPIDER_MODULES = ['second.spiders']
NEWSPIDER_MODULE = 'second.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 20

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False  #不记录cookie

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
 #  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  # 'Accept-Language': 'en',
   # 'User-Agent':'',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'second.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'second.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'second.pipelines.SecondPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
pipelines.py
# -*- coding: utf-8 -*-
import urllib
import random
class SecondPipeline(object):
    def process_item(self, item, spider):
        try:
            title=item['title'][0].encode('gbk')
            file="E:/tupian/"+str(title)+str(int(random.random()*10000))+".jpg"
            urllib.urlretrieve(item['url'][0],filename=file)
        except Exception,e:
            print e
            pass
        return item


笔记：
一、scrapy图片爬虫构建思路
     1.分析网站
     2.选择爬取方式与策略
     3.创建爬虫项目 →定义items.py
     4.编写爬虫文件
     5.编写pipelines与setting
     6.调试

二、千图网难点（http://www.58pic.com/）
     1.要爬取全站的图片
     2.要爬取高清的图片------找出高清地址即可
     3要有相应的反爬虫机制------如模拟浏览器，不记录cookie等，只要相应注释去掉即可COOKIES_ENABLED = False

三、散点知识
   1.from scrapy.http import Request  #是回调函数用Request(url=...,callback=...)
   2.xpath的//表示提取所有符合的节点



