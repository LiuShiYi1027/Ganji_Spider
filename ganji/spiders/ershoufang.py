# -*- coding: utf-8 -*-
# @Time    : 2018/3/1 下午9:00
# @Author  : LiuShiYi
# @Site    : 
# @File    : ershoufang.py
from scrapy import Spider
from scrapy import Request
from ganji.items import ErShouItem
import re


class ErShouFangSpider(Spider):
    """
    赶集网二手房爬虫
    """
    name = "ershoufang"
    allowed_domains = ["ganji.com"]
    start_urls = ["http://sh.ganji.com/fang5/"]  # 入口

    site_url = "http://sh.ganji.com"

    def parse(self, response):

        # 获取每一个二手房的入口url
        title_url_list = response.xpath(
            ".//div[@class='f-main-list']//div[@class='f-list-item ershoufang-list']/@href").extract()

        # 获取二手房item
        for url in title_url_list:
            url = self.site_url + url
            yield Request(url, callback=self.parse_item)

        # 检测下一页标签是否存在
        if response.xpath(".//div[@class='pageBox']//li[last()]/a/span/text()").extract_first() == "下一页 >":
            next_page_url = response.xpath(".//div[@class='pageBox']//li[last()]/a/@href").extract_first()
            next_page_url = self.site_url + next_page_url
            yield Request(next_page_url, callback=self.parse)

    def parse_item(self, response):
        """
        获取二手房item
        :param response:
        :return:
        """
        item = ErShouItem()

        try:
            item['title'] = response.xpath(
                ".//div[@class='card-info f-fr']//p[@class='card-title']/i/text()").extract_first(default='N/A')
            # print(item['title'])
            item['price'] = response.xpath(
                ".//div[@class='er-card-pay']/div/span[@class='price']/text()").extract_first(
                default='N/A')
            # print(item['price'])
            item['avg_price'] = re.findall("\d+.*", response.xpath(
                ".//div[@class='er-card-pay']/div/span[@class='unit']/text()").extract_first(
                default='N/A'))[0]
            # print(item['avg_price'])
            item['house'] = response.xpath(
                ".//ul[@class='er-list f-clear']/li[1]/span[@class='content']/text()").extract_first(
                default='N/A')
            # print(item['house'])
            item['area'] = response.xpath(
                ".//ul[@class='er-list f-clear']/li[2]/span[@class='content']/text()").extract_first(
                default='N/A')
            # print(item['area'])
            item['orientation'] = response.xpath(
                ".//ul[@class='er-list f-clear']/li[3]/span[@class='content']/text()").extract_first(default='N/A')
            item['floor'] = response.xpath(
                ".//ul[@class='er-list f-clear']/li[4]/span[@class='content']/text()").extract_first(
                default='N/A')
            item['type'] = response.xpath(
                ".//ul[@class='er-list f-clear']/li[5]/span[@class='content']/text()").extract_first(
                default='N/A').strip()
            item['elevator'] = response.xpath(
                ".//ul[@class='er-list f-clear']/li[6]/span[@class='content']/text()").extract_first(
                default='N/A').strip()
            item['build_age'] = response.xpath(
                ".//ul[@class='er-list f-clear']/li[7]/span[@class='content']/text()").extract_first(
                default='N/A').strip()
            item['quality'] = response.xpath(
                ".//ul[@class='er-list f-clear']/li[8]/span[@class='content']/text()").extract_first(
                default='N/A').strip()
            item['property'] = response.xpath(
                ".//ul[@class='er-list f-clear']/li[9]/span[@class='content']/text()").extract_first(
                default='N/A').strip()
            item['decoration'] = response.xpath(
                ".//ul[@class='er-list f-clear']/li[10]/span[@class='content']/text()").extract_first(default='N/A')
            item['village'] = response.xpath(
                ".//ul[@class='er-list-two f-clear']/li[1]/span[@class='content']/a[1]/text()").extract_first(
                default='N/A')
            item['subway'] = response.xpath(
                ".//ul[@class='er-list-two f-clear']//div[@class='subway-wrap']/span[1]/text()").extract_first(
                default='N/A')
            item['district'] = response.xpath(
                ".//ul[@class='er-list-two f-clear']/li[@class='er-item f-fl']/span[@class='content']/a/text()").extract()[
                -2]
            item['region'] = response.xpath(
                ".//ul[@class='er-list-two f-clear']/li[@class='er-item f-fl']/span[@class='content']/a/text()").extract()[
                -3]
            item['address'] = '-'.join(
                response.xpath(
                    ".//ul[@class='er-list-two f-clear']/li[@class='er-item f-fl']/span[@class='content']/a/text()").extract()[
                -3:])
            if len(item['address']) == 0:
                item['address'] = 'N/A'
            item['url'] = re.findall("h.*htm", response.url)[0]

            print(''.center(10, '-'))

            for key, value in item.items():
                print(key + ':' + value)

            print('保存成功'.center(50, '-'))

            yield item

        except Exception as e:
            with open('Exception.txt', 'a+') as exception_logger:
                exception_logger.write(response.url)
                exception_logger.write(' ')
                exception_logger.write(str(e))
                exception_logger.write('\n')
