# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
import scrapy
from scrapy_redis.spiders import RedisCrawlSpider
from Snowball.items import SnowballItem

class RidesdemoSpider(RedisCrawlSpider):
    name = 'snowball'

    # scrapy_redis的调度器队列的名称，最终我们会根据该队列的名称向调度器队列中扔一个起始url
    redis_key = "snowball"
    # allowed_domains = ['xueqiu.com']
    # link = LinkExtractor(allow=r'https://dig.chouti.com/.*?/.*?/.*?/\d+')
    # link1 = LinkExtractor(allow=r'https://xueqiu.com/service/v5/stock/screener/quote/list?page=\d+&size=90&order=desc&order_by=amount&exchange=CN&market=CN&type=sha')
    # rules = (
    #     Rule(link, callback='parse_item', follow=True),
    #     Rule(link1, callback='parse_item', follow=True),
    # )
    # start_urls = ["r'https://xueqiu.com/service/v5/stock/screener/quote/list?page=\d+&size=90&order=desc&order_by=amount&exchange=CN&market=CN&type=sha'"]

    def start_requests(self):
            # 把所有的URL地址统一扔给调度器入队列
        for offset in range(1, 18, 1):
            url = 'https://xueqiu.com/service/v5/stock/screener/quote/list?page={}&size=90&order=desc&order_by=amount&exchange=CN&market=CN&type=sha'.format(offset)
            # 交给调度器
            yield scrapy.Request(
                url=url,
                callback=self.parse_item
            )



    def parse_item(self, response):
        print(response)
        # div_list = response.xpath('//*[@id="content-list"]/div')
        # for div in div_list:
        #     content = div.xpath('string(./div[@class="news-content"]/div[1]/a[1])').extract_first().strip().replace("\t","")
        #     print(content)
        #     item = RedisscrapyproItem()
        #     item['content'] = content
            # yield item