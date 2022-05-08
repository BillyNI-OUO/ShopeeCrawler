"""
The object used to storage the information of label
"""
class label:
	def __init__(self, name, label_id):

		self.name = name
		self.label_id = label_id

	def __str__(self):
		
		return f'name: {self.name}\nlabel_id: {self.label_id}'