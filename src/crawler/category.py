"""
The object used to storage the information of category
"""

class category:
	def __init__(self, catid, parentid, name, display_name, level, children):
		self.catid = catid
		self.parentid = parentid
		self.name = name
		self.display_name = display_name
		self.level = level
		self.children = children


	def __str__(self):
		children = 'None'
		if self.children != None:
			children ='\n' + ' \n'.join(map(str, self.children))
		return f'catid : {self.catid}\nname : {self.name}\nchildren : {children}'