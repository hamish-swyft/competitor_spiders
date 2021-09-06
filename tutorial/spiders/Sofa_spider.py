import scrapy
import csv
import pandas as pd
from datetime import datetime
from scrapy.http import FormRequest, JsonRequest

class SofaSpider(scrapy.Spider):
    name = "Swyfthome"

    def start_requests(self):
        urls = [
            'https://swyfthome.com/collections/model-00/',
            'https://swyfthome.com/collections/model-01',
            'https://swyfthome.com/collections/model-02',
            'https://swyfthome.com/collections/model-03',
            'https://swyfthome.com/collections/model-04/',

        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        thetime = datetime.now().strftime("%Y/%m/%d, %H:%M:%S")
        page = response.url.split("/")[-2]
        filename = f'{page}.csv'

        in_stock_items = response.xpath('//*[@class="product-grid-card-new-image-container "]//@alt').getall()
        in_stock_items = [[thetime, item.strip()] for item in in_stock_items]
        in_stock_df = pd.DataFrame(in_stock_items, columns=["Datetime", "Product"])
        in_stock_df["Availability"] = "available"
        in_stock_df.to_csv("dataframe.csv", mode='a', header=False, )

        oos_items = response.xpath(
            '//*[@class="product-grid-card-new-image-container product-grid-card-new-image-sold-out"]//@alt').getall()
        oos_items = [[thetime, item.strip()] for item in oos_items]
        oos_df = pd.DataFrame(oos_items, columns=["Datetime", "Product"])
        oos_df["Availability"] = "not available"
        oos_df.to_csv("dataframe.csv", mode='a', header=False)

        self.log(f'Saved file {filename}')

class LoafSpider(scrapy.Spider):
    name = "Loaf"

    def start_requests(self):
        urls = [
            'https://loaf.com/bag-a-bargain/sofas/all/all/all/all/all?ajax=Y&heros=6&stock=stock&oddbumps=N&product_url=https%3A%2F%2Floaf.com%2Fproducts%2Fsofas&page=1&request=3',
            "https://loaf.com/bag-a-bargain/sofas/all/all/all/all/all?ajax=Y&heros=6&stock=stock&oddbumps=N&product_url=https%3A%2F%2Floaf.com%2Fproducts%2Fsofas&page=2&request=1",
            "https://loaf.com/bag-a-bargain/sofas/all/all/all/all/all?ajax=Y&heros=6&stock=stock&oddbumps=N&product_url=https%3A%2F%2Floaf.com%2Fproducts%2Fsofas&page=3&request=1",
            'https://loaf.com/bag-a-bargain/sofas/all/all/all/all/all?ajax=Y&heros=6&stock=stock&oddbumps=N&product_url=https%3A%2F%2Floaf.com%2Fproducts%2Fsofas&page=4&request=3',
            "https://loaf.com/bag-a-bargain/sofas/all/all/all/all/all?ajax=Y&heros=6&stock=stock&oddbumps=N&product_url=https%3A%2F%2Floaf.com%2Fproducts%2Fsofas&page=5&request=1",
            "https://loaf.com/bag-a-bargain/sofas/all/all/all/all/all?ajax=Y&heros=6&stock=stock&oddbumps=N&product_url=https%3A%2F%2Floaf.com%2Fproducts%2Fsofas&page=6&request=1",
        ]
        payload = {'': ''}

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        thetime = datetime.now().strftime("%Y/%m/%d, %H:%M:%S")
        page = response.url.split("/")[-2]
        filename = f'{page}.csv'
        in_stock_items = response.xpath('//*[@class="grid__item l-one-third m-one-half xs-full js-product"]//@href').getall()
        in_stock_items = [[thetime, item.strip()] for item in in_stock_items]
        in_stock_df = pd.DataFrame(in_stock_items, columns=["Datetime", "Product"])
        in_stock_df["Availability"] = "available"
        in_stock_df.to_csv("loaf.csv", mode='a', header=False, )

        self.log(f'Saved file {filename}')


class SwoonSpider(scrapy.Spider):
    name = "Swoon"

    def start_requests(self):
        url = "https://www.swooneditions.com/graphql"
        payload = {
            "credentials": "include",
            "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
                "Accept": "*/*",
                "Accept-Language": "en-GB,en;q=0.5",
                "Content-Type": "application/json",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "authorization": ""
            },
            "referrer": "https://www.swooneditions.com/range/munich-range",
            "body": "{\"operationName\":\"getBreadcrumbData\",\"variables\":{\"category_id\":182},\"query\":\"query getBreadcrumbData($category_id: Int!) {\\n  storeConfig {\\n    id\\n    category_url_suffix\\n    __typename\\n  }\\n  category(id: $category_id) {\\n    breadcrumbs {\\n      category_level\\n      category_name\\n      category_url_path\\n      __typename\\n    }\\n    id\\n    name\\n    url_path\\n    __typename\\n  }\\n}\\n\"}",
            "method": "POST",
            "mode": "cors"
        }
        yield JsonRequest(url=url, data=payload, callback=self.parse)

    def parse(self, response):
        thetime = datetime.now().strftime("%Y/%m/%d, %H:%M:%S")
        page = response.url.split("/")[-2]
        filename = f'{page}.csv'
        in_stock_items = response.xpath('//@text').getall()
        in_stock_items = [[thetime, item.strip()] for item in in_stock_items]
        in_stock_df = pd.DataFrame(in_stock_items, columns=["Datetime", "Product"])
        in_stock_df["Availability"] = "available"
        in_stock_df.to_csv("loaf.csv", mode='a', header=False, )

        self.log(f'Saved file {filename}')
