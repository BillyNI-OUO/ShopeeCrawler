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

KEYWORDS = {
    'quality': [
        "商品", "CP", "好看", "好用", "大小", "適當", "瑕疵", "優點", "缺點", "品質" ,"舒適", "適合", "色差", "顏色",
        "版型", "尺寸", "重量", "厚度", "彈性", "質感", "材質", "衣服", "外套", "褲子", "內衣", "胸罩", "包覆", "身材",
        "質感", "材質", "味道", "香味", "洋裝", "套裝", "腰身", "皮帶", "衣服", "西裝", "牛仔褲", "短裙", "黑色", "紫色",
        "藍色", "紅色", "重量", "百搭", "軍綠色", "棕色", "白色", "喜歡", "討厭", "香", "臭", "難看", "難用", "難聞", "顯瘦",
        "顯胖", "設計", "質量", "好評", "差評", "美", "毛茸茸", "長度", "顏色", "可愛", "粉色", "商品", "雷", "設計", "功能", 
        "米色", "黃色", "綠色", "圖片", "影片", "東西", "食物", "實物", "長褲", "布料", "雪紡紗", "棉麻", "差距", "外套",
        "新衣", "貨品", "奶油", '好吃', '新鮮', '味道', '麻辣', '舌頭', '菜餚', '嚼勁', '肚子', '風味', '豐富', '餐點',
        '口感', '必吃', '菜色', '精緻', '樣式', '廉價', '食材', '食物', '油膩', '軟嫩', '熟食',
        '生食', '腥味', '可口', '好聞', '芳香',
        '入味', '五味俱全', '甘美', '合口', '回味', '多汁', '好吃', '好味', '利口', '美味',
        '美味可口', '香', '脆', '夠味', '清口', '清爽', '爽口', '爽脆', '甜爽', '酥',
        '酥脆', '順口', '新鮮', '對味', '胃口', '適口', '膽美', '鮮', '鬆脆', '缺漏', '少', '多'
    
    ],
    'service': [
        '服務', '粗魯', '溝通', '訂位', '感受', '預約', '人員', '溫暖', '耐心', '馬上', '態度',
        '用餐品質', '帶位', '道歉', '招待', '差勁', '友善', '臭臉', '店員', '動線', '盡職', '耐煩',
        '耐性', '暴躁', '煩躁', '急躁', '冒失', '輕率', '勝任', '客服', '回應', '店家', '人好', '闆娘', '小禮物',
        '活動', '回應', '回復', '回覆', '速度', '快', '退貨', '處理', '迅速', '老闆', '小編', '回答', '耐煩', '粗糙',
        '聊聊', '介紹', '文字', '態度', '細心', '賣家', '愛心', '敷衍', '緩慢', '心得'
    ],
    'value': [
        '價格', '合理', '實惠', 'cp', '超值', '豐富', '貴', '平價', '豐盛', '划算', 'CP', '昂貴', '值得', 
        '少', '多', '價錢', '錢'
    ],
    'delivery': [
        '迅速', '物流', '緩慢', '快', '慢', '等待', '退貨', '包裝', '外殼', '缺漏'
    ]
}

ASPECTS = ['quality', 'service', 'value', 'delivery']
