from abc import ABC, abstractmethod

from aerovision.kml.generator import KMLGenerator
from aerovision.kml.cameras import *
from aerovision.kml.components import *

class KMLTimespanGenerator(KMLGenerator):
	"""
	This abstract class defines the structure of a KML Timespan Generator.

	"""

	@abstractmethod
	def configure(self):
		"""
		Configure the KML Timespan Generator.

		"""
		pass

	def writeDocumentBody(self, file):
		"""
		Write the body of the KML document.

		"""
		# camera setup
		file.write(self.camera.setup())
		
		# write the timespan configuration of each component
		for component in self.components:
			file.write(component.setup())

	def toXMLTime(self, timestamp):
		"""
		Transform a datetime object into an XML time string.
		See: https://developers.google.com/kml/documentation/time?csw=1#how-to-specify-time
		
		"""
		return timestamp.strftime('%Y-%m-%dT%H:%M:%S')

	
class FlightsKMLTimespan(KMLTimespanGenerator):
	"""
	This class can create multi-flight KML timespans.

	"""

	def configure(self):
		"""
		Configure the multi-flight timespan.

		"""
		self.camera = FixedKMLCamera({}, {})
		self.components = [
			TrajectoryLine3DKMLComponent(self.data, {'useTimespan': True})
		]