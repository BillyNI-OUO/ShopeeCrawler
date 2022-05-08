"""
The object used to storage the information of comment
"""

class comment:
	def __init__(self, rating_star, cmtid, author_username, author_shopid, comment, mtime, itemid, shopid):
		self.rating_star = rating_star
		self.cmtid = cmtid
		self.author_username =  author_username
		self.author_shopid = author_shopid
		self.comment = comment
		self.mtime = mtime
		self.itemid = itemid
		self.shopid = shopid
	def __str__(self):
		return f'rating_star : {self.rating_star}\ncmtid : {self.cmtid}\nauthor_username : {self.author_username}\ncomment : {self.comment}\nmtime : {self.mtime}'