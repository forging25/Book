# -*- coding:utf-8 -*-
# !/usr/bin/env python
import asyncio
import time

from pprint import pprint

from ruia import Spider, Item, TextField, AttrField

from ruia_ua import middleware as ua_middleware

from Book.database.mongodb import MotorBase
from Book.spiders.middlewares import owl_middleware

try:
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

loop = asyncio.get_event_loop()
asyncio.set_event_loop(loop)


class ZHNovelInfoItem(Item):
    """
    定义继承自item的Item类
    """
    novel_name = TextField(css_select='div.main div.status h1 a')
    author = TextField(css_select='div.main div.status div.booksub a')
    # 当提取的值是属性的时候，要定义AttrField
    cover = AttrField(css_select='div.main div.book_cover img', attr='src')
    abstract = TextField(css_select='div.main div.status div.info_con p')
    status = AttrField(css_select='div.main div.status h1 em', attr='title')
    novels_type = TextField(css_select='div.main div.status div.booksub a')
    novel_chapter_url = AttrField(css_select='div.main div.status div.book_btn span.list a', attr='href')

    async def clean_author(self, author):
        if isinstance(author, list):
            return author[0].text
        else:
            return author

    async def clean_status(self, status):
        """
        当目标值的对象只有一个，默认将值提取出来，否则返回list，可以在这里定义一个函数进行循环提取
        :param ele_tag:
        :return:
        """
        if isinstance(status, list):
            return '#'.join([i.get('title').strip().replace('作品', '') for i in status])
        else:
            return status

    async def clean_novels_type(self, novels_type):
        if isinstance(novels_type, list):
            try:
                return novels_type[1].text
            except:
                return ''
        else:
            return ''


class ZHNovelInfoSpider(Spider):
    start_urls = []
    request_config = {
        'RETRIES': 3,
        'DELAY': 2,
        'TIMEOUT': 10
    }
    motor_db = MotorBase(loop=loop).get_db()

    async def parse(self, res):
        item = await ZHNovelInfoItem.get_item(html=res.html)

        item_data = {
            'novel_name': item.novel_name,
            'author': item.author,
            'cover': item.cover,
            'abstract': item.abstract,
            'status': item.status,
            'novels_type': item.novels_type,
            'novel_chapter_url': item.novel_chapter_url,
            'target_url': res.url,
            'spider': 'zongheng',
            'updated_at': time.strftime("%Y-%m-%d %X", time.localtime()),
        }

        print('获取 {} 小说信息成功'.format(item_data['novel_name']))
        print(item_data)
        await self.motor_db.all_novels_info.update_one(
            {'novel_name': item_data['novel_name'], 'spider': 'zongheng'},
            {'$set': item_data},
            upsert=True)


if __name__ == '__main__':
    import random

    ZHNovelInfoSpider.start_urls = ['http://book.zongheng.com/book/672340.html']
    ZHNovelInfoSpider.start(middleware=[ua_middleware, owl_middleware])

    # def all_novels_info():
    #     all_urls = []
    #
    #     for each in ZHNovelInfoSpider.all_novels_col.find({'spider': 'zongheng'}):
    #         if 'zongheng' in each['novel_url']:
    #             all_urls.append(each['novel_url'])
    #     random.shuffle(all_urls)
    #
    #     ZHNovelInfoSpider.start_urls = all_urls
    #     ZHNovelInfoSpider.start()
    #
    #
    # all_novels_info()
