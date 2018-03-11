# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GanjiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ErShouItem(scrapy.Item):
    """
    赶集网二手房Item
    """
    title = scrapy.Field()  # 标题
    price = scrapy.Field()  # 价格
    avg_price = scrapy.Field()  # 均价
    house = scrapy.Field()  # 户型
    area = scrapy.Field()  # 建面
    orientation = scrapy.Field()  # 朝向
    floor = scrapy.Field()  # 楼层
    type = scrapy.Field()  # 房屋情况
    elevator = scrapy.Field()  # 电梯情况
    build_age = scrapy.Field()  # 建筑年代
    quality = scrapy.Field()  # 房屋性质
    property = scrapy.Field()  # 产权
    decoration = scrapy.Field()  # 装修情况
    village = scrapy.Field()  # 小区名称
    subway = scrapy.Field()  # 地铁
    district = scrapy.Field() # 所在区域
    region = scrapy.Field() # 所在区域
    address = scrapy.Field()  # 所在地址
    url = scrapy.Field() # 连接url