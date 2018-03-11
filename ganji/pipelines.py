# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import pymysql
import pymysql.cursors
import codecs
import json
from logging import log
from ganji import settings


class GanjiPipeline(object):
    def process_item(self, item, spider):
        return item


class ErShouFangPipeline(object):
    """
    二手房Pipeline
    将二手房item保存到item中
    """

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        """
        导入数据库配置
        :return:
        """
        dbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=False
        )
        dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)  # 调用插入的方法
        query.addErrback(self._handle_error, item, spider)  # 调用异常处理方法
        return item

    def _conditional_insert(self, tx, item):
        """
        将item写入到数据表中
        :param tx:
        :param item:
        :return:
        """
        print("数据库",item)
        sql = "insert into ershoufang(" \
              "price, avg_price, house, " \
              "area, orientation, floor, type, " \
              "elevator, build_age, quality, property, " \
              "decoration, village, subway, district, region, address, url) " \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        params = (item['price'],
                  item['avg_price'],
                  item['house'],
                  item['area'],
                  item['orientation'],
                  item['floor'],
                  item['type'],
                  item['elevator'],
                  item['build_age'],
                  item['quality'],
                  item['property'],
                  item['decoration'],
                  item['village'],
                  item['subway'],
                  item['district'],
                  item['region'],
                  item['address'],
                  item['url'])

        # print(params)
        # print(sql % params)

        # with open('test.txt', 'a') as f:
        #     f.write(sql%params)
        #     f.write('\n')

        tx.execute(sql, params)

    def _handle_error(selfself, failure, item, spider):
        print('database operation exeception'.center(50, '-'))
        print(''.center(50, '-'))
        print(failure)