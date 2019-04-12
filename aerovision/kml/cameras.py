from abc import ABC, abstractmethod

class KMLCamera(ABC):
	@abstractmethod
	def setup(self, data):
		pass
	
	@abstractmethod
	def step(self, data):
		pass

class TopViewKMLCamera(KMLCamera):
	def __init__(self):
		self.lat = '52.216'
		self.lon = '4.516'
		self.geoaltitude = '1500'
		self.heading = '-137'
		self.tilt = '80'
		self.firstStep = True

	def setup(self, data):
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
	
	def step(self, data):
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