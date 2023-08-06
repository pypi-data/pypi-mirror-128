import math

import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

path = os.path.dirname(__file__)


def count(url):
    try:
        rep = requests.get(url).text
        soup = BeautifulSoup(rep, 'lxml')
        counts = str(soup.select('.count')[0].text).split()[-1].strip('（）').replace(',', '').replace(' ', '').replace(
            '件', '')
        # 用正则
        return int(counts)
    except:
        return 100


def index(jp: str, zh, key, spider_url: str, min_price: str):
    count_url = spider_url.split('?')[0] + f'?p=1&min={min_price}'
    counts = count(count_url)
    min_price = int(min_price.rstrip('日元以上'))
    filename = jp.replace(".", "").replace("/", "").replace(":", "").replace("-", "")
    print(min_price)
    headers = ['jp', 'zh', 'key', 'title', 'price', 'image', 'points', 'url']
    for page in range(math.floor(counts / 45) + 1):
        # https://search.rakuten.co.jp/search/mall/%E3%82%A8%E3%82%B9%E3%83%88/?p=7&s=3
        try:
            url = spider_url.split('?')[0] + f'?p={page}&min={min_price}'
            rep = requests.get(url).text
            soup = BeautifulSoup(rep, 'lxml')
            cards = soup.select('.searchresultitem')
            for card in cards:
                title = card.select('.title > h2 > a')[0].get('title')
                price = card.select('.important')[0].text.replace('円', '').replace(",", "")
                img = card.select('.image > a > img')[0].get('src')
                points = card.select('.points > span')[0].text
                url = card.select('.image > a')[0].get('href')
                per = jp, zh, key, title, price, img, points, url
                # if int(price) >= 3000:
                one = dict(zip(headers, per))
                print(one)
                df = pd.DataFrame([one])
                df.to_csv(os.path.join(path, f'csv/{filename}.csv'), mode='a', header=False, index=None)

        except Exception as e:
            print(e)
            continue
    new_df = pd.read_csv(os.path.join(path, f'csv/{filename}.csv'))
    new_df.columns = headers
    new_df.to_excel(os.path.join(path, f'excel/{filename}.xlsx'))


def read():
    df = pd.read_excel(os.path.join(path, 'source.xlsx'))
    per = df[['品牌', '中文名称', '爬取关键字', '爬取地址', '爬取价格范围']].to_numpy()
    # 修改成 迭代器读取
    for item in per:
        new = list(item)
        jp, zh, key, url, min_price = new
        index(jp, zh, key, url, min_price)


if __name__ == '__main__':
    read()
