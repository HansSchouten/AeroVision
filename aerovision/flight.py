class Flight:
	def __init__(self, data):
		self.data = data
		self.id = data.iloc[0].icao24
		
	def dataPoints(self, index):
		return self.data.iloc[index]