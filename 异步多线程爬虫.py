# -*- coding:utf-8 -*-
__author__ = 'youjia'
__date__ = '2018/8/4 21:03'
import requests
import threading
import re
from queue import Queue
from lxml import etree
import os
import urllib.request


class Producer(threading.Thread):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36'
                      ' (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
    }

    def __init__(self, page_queue, img_queue, *args, **kwargs):
        super(Producer, self).__init__(*args, **kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        while True:
            if self.page_queue.empty():
                break
            url = self.page_queue.get()
            self.parse_page(url)

    def parse_page(self, url):
        resp = requests.get(url, headers=self.headers)
        if resp.status_code == 200:
            text = resp.text
            html = etree.HTML(text)
            imgs = html.xpath("//div[@class='page-content text-center']//img[@class!='gif']")
            for img in imgs:
                img_url = img.get('data-original')
                title = img.get('alt')
                title = re.sub(r'[\?？！!,，\.。…#\*]', '', title)  # 替换掉图片标题中的不可用字符
                suffix = os.path.splitext(img_url)[1]  # 后缀名
                filename = title + suffix
                self.img_queue.put((img_url, filename))


class Consumer(threading.Thread):
    def __init__(self, page_queue, img_queue, *args, **kwargs):
        super(Consumer, self).__init__(*args, **kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        while True:
            if self.page_queue.empty() and self.img_queue.empty():
                break
            img_url, filename = self.img_queue.get()
            urllib.request.urlretrieve(img_url, 'images1/'+filename)
            print(filename+'  下载完成')


def main():
    page_queue = Queue(100)
    img_queue = Queue(2000)
    for x in range(2, 100):
        url = 'http://www.doutula.com/photo/list/?page=%d' % x
        page_queue.put(url)

    for x in range(5):
        t = Producer(page_queue, img_queue)
        t.start()

    for x in range(5):
        t = Consumer(page_queue, img_queue)
        t.start()


if __name__ == '__main__':
    main()
