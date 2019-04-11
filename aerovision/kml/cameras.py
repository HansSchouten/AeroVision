from abc import ABC, abstractmethod

class KMLCamera(ABC):
	@abstractmethod
	def setup(self, flight):
		pass
	
	@abstractmethod
	def step(self, dataPoint):
		pass


class TopViewKMLCamera(KMLCamera):
	def __init__(self):
		self.firstStep = True

	def setup(self, flight):
		self.firstDataPoint = flight.dataPoint(0)
		return '''
<LookAt>
	<latitude>''' + str(self.firstDataPoint.lat) + '''</latitude>
	<longitude>''' + str(self.firstDataPoint.lon) + '''</longitude>
	<altitude>''' + str(self.firstDataPoint.geoaltitude + 500) + '''</altitude>
	<altitudeMode>absolute</altitudeMode>
	<heading>0</heading>
	<tilt>0</tilt>
</LookAt>
		'''
	
	def step(self, dataPoint):
		if self.firstStep:
			self.firstStep = False
			return '''
<gx:FlyTo>
    <gx:duration>1.0</gx:duration>
    <LookAt>
		<latitude>''' + str(self.firstDataPoint.lat) + '''</latitude>
		<longitude>''' + str(self.firstDataPoint.lon) + '''</longitude>
		<altitude>''' + str(self.firstDataPoint.geoaltitude + 500) + '''</altitude>
        <altitudeMode>absolute</altitudeMode>
        <heading>0</heading>
        <tilt>0</tilt>
    </LookAt>
</gx:FlyTo>
			'''
		else:
			return '''
<gx:FlyTo>
    <LookAt>
		<latitude>''' + str(self.firstDataPoint.lat) + '''</latitude>
		<longitude>''' + str(self.firstDataPoint.lon) + '''</longitude>
		<altitude>''' + str(self.firstDataPoint.geoaltitude + 500) + '''</altitude>
        <altitudeMode>absolute</altitudeMode>
        <heading>0</heading>
        <tilt>0</tilt>
    </LookAt>
</gx:FlyTo>
			'''