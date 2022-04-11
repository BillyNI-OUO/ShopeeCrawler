import requests
import urllib
import src.crawler as crawler
import json
from src.crawler.product import item
from src.crawler.product import item_rating
keyword = '女生衣著'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
    'x-api-source': 'pc',
    'referer': f'https://shopee.tw/{urllib.parse.quote(keyword)}'
}

#https://shopee.tw/-cat.11040765?page=2
s = requests.Session()
url = 'https://shopee.tw/api/v4/search/product_labels'
r = s.get(url, headers=headers)

#https://shopee.tw/api/v4/search/search_items?by=relevancy&fe_categoryids=11040765&limit=60&newest=120&order=desc&page_type=search&scenario=PAGE_OTHERS&version=2

base_url = 'https://shopee.tw/api/v2/search_items/'
query = f"by=relevancy&fe_categoryids=11040765&limit=2&newest=0&order=desc&page_type=search&version=2"
url = base_url + '?' + query
r = s.get(url, headers=headers)
data = r.json()
"""if r.status_code == requests.codes.ok:
    data = r.json()
    # with open('shopee.json', 'w', encoding='utf-8') as f:
    #     f.write(r.text)"""

itemsList = []

for i in data["items"]:
    itemRating = item_rating(i["item_rating"]['rating_count'], i["item_rating"]['rating_star'], i["item_rating"]['rcount_with_context'], i["item_rating"]['rcount_with_image'])
    #Product = product(i["itemid"],i["shopid"],i["name"],itemRating)
    itemsList.append(item(i["itemid"],i["shopid"],i["name"],itemRating))

for i in itemsList:
    print(i)
"""
for i in data["items"]:
    print(i["itemid"])
    print(i["shopid"])
    print(i["name"])
    print(i["item_rating"])
    print('\n\n\n')
"""

#https://shopee.tw/api/v4/search/search_items?by=relevancy&fe_categoryids=11040765&limit=60&newest=60&order=desc&page_type=search&scenario=PAGE_OTHERS&version=2
#https://shopee.tw/api/v4/search/search_items?by=relevancy&fe_categoryids=11040765&limit=60&newest=0&order=desc&page_type=search&scenario=PAGE_OTHERS&version=2
#https://shopee.tw/api/v4/search/search_items?by=relevancy&fe_categoryids=11040765&limit=60&newest=120&order=desc&page_type=search&scenario=PAGE_OTHERS&version=2


