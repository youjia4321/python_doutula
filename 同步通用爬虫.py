# -*- coding:utf-8 -*-
__author__ = 'youjia'
__date__ = '2018/8/4 20:41'
import requests
from lxml import etree
import re
import os
import urllib.request


def parse_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36'
                      ' (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
    }
    resp = requests.get(url, headers=headers)
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
            urllib.request.urlretrieve(img_url, 'images/'+filename)
            print(filename)


def main():
    for x in range(2, 101):
        url = 'http://www.doutula.com/photo/list/?page=%d' % x
        parse_page(url)
        break


if __name__ == '__main__':
    main()
