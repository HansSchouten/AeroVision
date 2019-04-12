class Flight:
	def __init__(self, data):
		self.data = data
		self.icao24 = data.iloc[0].icao24
		self.id = str(data.iloc[0].flightId)
		
	def dataPoints(self, index):
		return self.data.iloc[index]

	def medianAltitude(self):
		return self.data.loc[:,"geoaltitude"].median()