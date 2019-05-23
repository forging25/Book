# !/usr/bin/env python
import os
import schedule
import sys
import time

os.environ['MODE'] = 'PRO'
sys.path.append('../../')

from Book.spiders import QidianRankingSpider, ZHRankingSpider


def start_spider():
    QidianRankingSpider.start()
    ZHRankingSpider.start()


# python novels_schedule.py
schedule.every(60).minutes.do(start_spider)

while True:
    schedule.run_pending()
    time.sleep(1)
