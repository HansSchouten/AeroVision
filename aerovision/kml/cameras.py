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
		self.lat = 52.185870
		self.lon = 4.473441
		self.geoaltitude = 8000
		self.firstStep = True

	def setup(self, data):
		return '''
<LookAt>
	<latitude>''' + str(self.lat) + '''</latitude>
	<longitude>''' + str(self.lon) + '''</longitude>
	<altitude>''' + str(self.geoaltitude) + '''</altitude>
	<altitudeMode>absolute</altitudeMode>
	<heading>0</heading>
	<tilt>0</tilt>
</LookAt>
		'''
	
	def step(self, data):
		if self.firstStep:
			self.firstStep = False
			return '''
<gx:FlyTo>
    <LookAt>
		<latitude>''' + str(self.lat) + '''</latitude>
		<longitude>''' + str(self.lon) + '''</longitude>
		<altitude>''' + str(self.geoaltitude) + '''</altitude>
        <altitudeMode>absolute</altitudeMode>
        <heading>0</heading>
        <tilt>0</tilt>
    </LookAt>
</gx:FlyTo>
			'''
		else:
			return '''
<gx:FlyTo>
    <gx:duration>1.0</gx:duration>
    <LookAt>
		<latitude>''' + str(self.lat) + '''</latitude>
		<longitude>''' + str(self.lon) + '''</longitude>
		<altitude>''' + str(self.geoaltitude) + '''</altitude>
        <altitudeMode>absolute</altitudeMode>
        <heading>0</heading>
        <tilt>0</tilt>
    </LookAt>
</gx:FlyTo>
			'''