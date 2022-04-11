"""
The object used to storage the information of item
"""
class item:
	
	def __init__(self, itemid, shopid, name, item_rating):

		self.itemid = itemid
		self.shopid = shopid
		self.name = name
		self.item_rating = item_rating

	def __str__(self):
		return f'itemid : {self.itemid}\nshopod : {self.shopid}\nname : {self.name}\nitem_rating : \n{self.item_rating}'


class item_rating:
	
	def __init__(self, rating_count, rating_star, rcount_with_context, rcount_with_image):
		self.rating_count = rating_count[0]
		self.rating1 = rating_count[1]
		self.rating2 = rating_count[2]
		self.rating3 = rating_count[3]
		self.rating4 = rating_count[4]
		self.rating5 = rating_count[5]
		self.rating_star = rating_star	
		self.rcount_with_context = rcount_with_context
		self.rcount_with_image = rcount_with_image

	def __str__(self):
		return f'rating_count : {self.rating_count}\nrating_star : {self.rating_star}'