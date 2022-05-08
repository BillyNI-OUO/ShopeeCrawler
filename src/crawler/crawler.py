import requests
import sys
from src import constants
from src.crawler.label import label
from src.crawler.product import item
from src.crawler.product import item_rating
from src.crawler.comment import comment
from src.crawler.category import category
def GetLabel():
	s = requests.Session()
	r = s.get(constants.LABEL_URL, headers=constants.HEADERS)
	data = r.json()
	res = []
	for i in data['data']:
		res.append(label(i['name'],i['label_id']))
	return res

def GetItem(catid):
	itemsList = []
	s = requests.Session()
	for i in range(100):
		url = constants.ITEM_URL(catid, 100, 100*i)
		
		r = s.get(url, headers=constants.HEADERS)
		data = r.json()
		try:
			for i in data["items"]:
			    itemRating = item_rating(i["item_rating"]['rating_count'], i["item_rating"]['rating_star'], i["item_rating"]['rcount_with_context'], i["item_rating"]['rcount_with_image'])
			    #Product = product(i["itemid"],i["shopid"],i["name"],itemRating)
			    itemsList.append(item(i["itemid"], i["shopid"], catid, i["name"], itemRating, i['images']))
		except Exception as e:
			sys.stderr.write(str(e)+"\n")
			return itemsList
		return itemsList

def GetComment(shopid, itemid, count=5000):
	s = requests.Session()
	commentList = []
	for i in range(int(count/50)):
		try:
			url = constants.COMMENT_URL(shopid, itemid, i)
			r = s.get(url, headers=constants.HEADERS)
			data = r.json()
			for i in data['data']['ratings']:
				commentList.append(comment(i['rating_star'], i['cmtid'], i['author_username'], i['author_shopid'], i['comment'], i['mtime'], i['itemid'], i['shopid']))
		except Exception as e:
			sys.stderr.write(str(e)+"\n")
	return commentList

def GetCategoryTree():
	s = requests.Session()
	url = constants.CATEGORYTREE_URL()
	r = s.get(url, headers=constants.HEADERS)
	data = r.json()
	CategoryList = []
	for i in data['data']['category_list']:
		children = []
		for j in i['children']:
			children.append(category(j['catid'], j['parent_catid'], j['name'], j['display_name'], j['level'], j['children']))
		CategoryList.append(category(i['catid'], i['parent_catid'], i['name'], i['display_name'], i['level'], children))
	return CategoryList	