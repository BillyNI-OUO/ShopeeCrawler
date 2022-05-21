#! /home/user/anaconda3/envs/billy/bin/python
# -*- coding: utf-8 -*-
from rating.model import RatingModel
import mysql.connector
from bert_serving.client import BertClient
import re
import numpy as np
import math
import time
from collections import defaultdict
import sys

BATCH_SIZE = 1000
count = 0
last_id = 0
if len(sys.argv) > 1:
    if sys.argv[1] != '-f':
        last_id = int(sys.argv[1])
print('start from:', last_id)

rm = RatingModel()

con = mysql.connector.connect(
    host= '140.114.53.129',        	# 主機名稱
	database= 'shopee',		# 資料庫名稱
	user= 'smartuser',            	# 帳號
	password= 'pp253&$@'  			# 密碼
)

bc = BertClient(check_length=False)

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


def is_aspect(aspect, sentence):
    global KEYWORDS
    for keyword in KEYWORDS[aspect]:
        if keyword in sentence:
            return True
    return False

def split_review_text_iter(review_text):
    if review_text is None:
        return
    for line in review_text.splitlines():
        stripped_line = line.strip()
        if len(stripped_line) == 0:
            continue

        for sep_line in re.split('。|，|；|﹐|！|\!|,|\?|？|；|;|\t|:|：', stripped_line):
            sep_line = sep_line.strip()
            if len(sep_line) > 20 or len(sep_line) <= 2:
                continue
            yield sep_line

print('starting...')

while True:
    st = time.time()
    cur = con.cursor(dictionary=True, buffered=True)
    cur.execute(f'''
    SELECT
        A.`id`, B.`comment`, A.`is_quality`,
        A.`is_service`, A.`is_value`, A.`is_delivery`
    FROM `reviews_aspect` AS A
    LEFT JOIN `comments` AS B ON A.`id` = B.`id`
    WHERE
        A.`id` > {last_id} AND
        (
            A.`is_quality` = 1 OR
            A.`is_service` = 1 OR
            A.`is_value` = 1 OR
            A.`is_delivery` = 1 OR
        )
    LIMIT {BATCH_SIZE};
    ''')
    reviews = cur.fetchall()
    if reviews is None or len(reviews) == 0:
        print('finish')
        break
    last_id = reviews[-1]['id']
    cur.close()
    
    splitted_sen = []
    sid = 0
    for review in reviews:
        text = str.lower(review['comment'])
        #print(text)
        review['aspects'] = defaultdict(list)
        review_aspects = tuple(filter(lambda v: review[f'is_{v}'] == 1, ASPECTS))
        for sen in split_review_text_iter(text):
            s_aspects = tuple(filter(lambda v: is_aspect(v, sen), review_aspects))
            if not any(s_aspects):
                continue
            splitted_sen.append(sen)
            
            for a in s_aspects:
                review['aspects'][a].append(sid)
            
            sid += 1
    
    if len(splitted_sen) == 0:
        print('skip!')
        print('count:', count, '\t', 'last index:', last_id)
        count += BATCH_SIZE
        continue
    splitted_emb = bc.encode(splitted_sen)
    splitted_rating = rm.predict_classes_embeddings(splitted_emb)
    
    results = []
    for review in reviews:
        ra = review['aspects']
        ar = list(np.average([splitted_rating[v] for v in ra[a]]) for a in ASPECTS)
        
        results.append(tuple(None if math.isnan(r) else r for r in ar) + (review['id'],))
    
    
    cur = con.cursor()
    cur.executemany(f'''
    UPDATE `reviews_aspect`
    SET
        `quality_rating` = %s,
        `service_rating` = %s,
        `value_rating` = %s,
        `delivery_rating` = %s,
    WHERE
        `id` = %s
    ;''', results)
    con.commit()
    cur.close()
    
    count += BATCH_SIZE
    
    et = time.time()
    print('count:', count, '\t', 'last index:', last_id, '\t', 'time:', et - st)
    
    del splitted_emb
    del splitted_rating
    del splitted_sen
    del results
