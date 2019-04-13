from abc import ABC, abstractmethod

class KMLCamera(ABC):
	"""
	This abstract class defines the structure of a KML Camera.

	"""

	def __init__(self, data, config):
		self.data = data
		self.config = config

	@abstractmethod
	def setup(self):
		"""
		Return the KML Camera structure defining the initial camera viewpoint.

		"""
		return ""
	
	@abstractmethod
	def timeStep(self, timeData):
		"""
		Return the KML Camera structure added for each (animation, timespan, ..) step.

		"""
		return ""

class FixedKMLCamera(KMLCamera):
	"""
	This KML Camera class defines a camera at a fixed viewpoint.

	"""

	def setup(self):
		"""
		Return the KML structure defining the initial camera viewpoint.

		"""
		self.lat = '52.216'
		self.lon = '4.516'
		self.geoaltitude = '1500'
		self.heading = '-137'
		self.tilt = '80'
		self.firstStep = True

		return '''
<LookAt>
	<latitude>''' + self.lat + '''</latitude>
	<longitude>''' + self.lon + '''</longitude>
	<altitude>''' + self.geoaltitude + '''</altitude>
	<altitudeMode>absolute</altitudeMode>
	<heading>''' + self.heading + '''</heading>
	<tilt>''' + self.tilt + '''</tilt>
</LookAt>
		'''
	
	def timeStep(self, timeData):
		"""
		Return the KML structure defining a fixed camera viewpoint.

		"""
		if self.firstStep:
			self.firstStep = False
			return '''
<gx:FlyTo>
    <LookAt>
		<latitude>''' + self.lat + '''</latitude>
		<longitude>''' + self.lon + '''</longitude>
		<altitude>''' + self.geoaltitude + '''</altitude>
		<altitudeMode>absolute</altitudeMode>
		<heading>''' + self.heading + '''</heading>
		<tilt>''' + self.tilt + '''</tilt>
    </LookAt>
</gx:FlyTo>
			'''
		else:
			return '''
<gx:FlyTo>
    <gx:duration>1.0</gx:duration>
    <LookAt>
		<latitude>''' + self.lat + '''</latitude>
		<longitude>''' + self.lon + '''</longitude>
		<altitude>''' + self.geoaltitude + '''</altitude>
		<altitudeMode>absolute</altitudeMode>
		<heading>''' + self.heading + '''</heading>
		<tilt>''' + self.tilt + '''</tilt>
    </LookAt>
</gx:FlyTo>
			'''