import urllib


KEYWORD = '女生衣著'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
    'x-api-source': 'pc',
    'referer': f'https://shopee.tw/{urllib.parse.quote(KEYWORD)}'
}

LABEL_URL = 'https://shopee.tw/api/v4/search/product_labels'
BASE_SEARCH_URL = 'https://shopee.tw/api/v2/search_items/'

SQLCONFIG={
    'host': '140.114.53.129',           # 主機名稱
    'database': 'shopee',               # 資料庫名稱
    'user': 'smartuser',                # 帳號
    'password': 'pp253&$@'              # 密碼
}



def ITEM_URL(catid, limit, start):
    return f'https://shopee.tw/api/v2/search_items/?by=relevancy&fe_categoryids={catid}&limit={limit}&newest={start}&order=desc&page_type=search&version=2'

def COMMENT_URL(shopid, itemid, time):
    return f"https://shopee.tw/api/v2/item/get_ratings?filter=1&flag=1&itemid={itemid}&limit=50&offset={50*time}&shopid={shopid}&type=0"

def CATEGORYTREE_URL():
    return "https://shopee.tw/api/v4/pages/get_category_tree"

