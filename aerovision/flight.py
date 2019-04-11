class Flight:
	def __init__(self, data):
		self.data = data
		
	def dataPoint(self, index):
		return self.data.iloc[index]