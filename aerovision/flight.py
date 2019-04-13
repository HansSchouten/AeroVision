from aerovision.interpolation import Spline

class Flight:
	"""
	This class represents a single flight.

	"""

	def __init__(self, data):
		self.data = data
		self.duration = data.shape[0]
		self.icao24 = data.iloc[0].icao24
		self.id = str(data.iloc[0].flightId)
		self.latSpline = self.getSpline("lat", 0.1)
		self.lonSpline = self.getSpline("lon", 0.1)
		self.altSpline = self.getSpline("geoaltitude", 10000)

	def getSpline(self, col, s):
		"""
		Return a spline object for a flightdata column.

		Parameters
		----------
		col : str
			The column of flightdata to create the spline for.
		s : float
			Smoothing factor. A non-zero smoothing factor allows for a
			loose fit through the datapoints.

		"""
		values = self.data[[col]].values
		t = range(self.duration)
		return Spline(t, values, s)

	def getLat(self, t):
		"""
		Return the latitude at the given moment in time.

		"""
		return self.latSpline.interpolate(t)
	
	def getLon(self, t):
		"""
		Return the longitude at the given moment in time.

		"""
		return self.lonSpline.interpolate(t)
	
	def getAlt(self, t):
		"""
		Return the geo altitude at the given moment in time.

		"""
		return self.altSpline.interpolate(t)

	def medianAltitude(self):
		"""
		Return the median of all altitudes throughout this flight.

		"""
		return self.data.loc[:,"geoaltitude"].median()