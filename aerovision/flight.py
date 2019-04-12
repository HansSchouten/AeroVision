from aerovision.interpolation import Spline

class Flight:
	def __init__(self, data):
		self.data = data
		self.duration = data.shape[0]
		self.icao24 = data.iloc[0].icao24
		self.id = str(data.iloc[0].flightId)
		self.latSpline = self.getSpline("lat", 0.1)
		self.lonSpline = self.getSpline("lon", 0.1)
		self.altSpline = self.getSpline("geoaltitude", 10000)

	def getSpline(self, col, s):
		values = self.data[[col]].values
		t = range(self.duration)
		return Spline(t, values, s)

	def getLat(self, t):
		return self.latSpline.interpolate(t)
	
	def getLon(self, t):
		return self.lonSpline.interpolate(t)
	
	def getAlt(self, t):
		return self.altSpline.interpolate(t)
		
	def dataPoints(self, index):
		return self.data.iloc[index]

	def medianAltitude(self):
		return self.data.loc[:,"geoaltitude"].median()