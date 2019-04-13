from abc import ABC, abstractmethod

from aerovision.kml.generator import KMLGenerator
from aerovision.kml.cameras import *
from aerovision.kml.components import *

class KMLAnimationGenerator(KMLGenerator):
	"""
	This abstract class defines the structure of a KML Animation Generator.

	"""

	@abstractmethod
	def configure(self):
		"""
		Configure the KML Animation Generator.

		"""
		pass

	def writeDocumentBody(self, file):
		"""
		Write the body of the KML document.

		"""
		# camera setup
		file.write(self.camera.setup())
		
		# write the pre-animation configuration of each component
		for component in self.components:
			file.write(component.setup())
		
		# write animation
		self.writeAnimation(file)
		
	@abstractmethod
	def writeAnimation(self, file):
		"""
		Write the animation.

		"""
		pass
	

class FlightsKMLAnimation(KMLAnimationGenerator):
	"""
	This class can create multi-flight KML animations.

	"""

	def configure(self):
		"""
		Configure the multi-flight animation.

		"""
		self.camera = FixedKMLCamera({}, {})
		self.components = [
			TrajectoryLine3DKMLComponent(self.data, {})
		]
		
	def writeAnimation(self, file):
		"""
		Write the multi-flight animation.

		"""
		flights = self.data
		
		file.write('<gx:Tour><name>Flights Animation</name><gx:Playlist>\n')
		
		# loop through all flights
		for flightId in flights:
			flight = flights[flightId]

			# animate camera to current flight
			file.write(self.camera.timeStep(flight))
			
			file.write('''
<gx:AnimatedUpdate>
	<gx:duration>0</gx:duration>
	<Update>
		<Change>
			''')
			
			# animate each component based on current flight
			for component in self.components:
				file.write(component.timeStep(flight, flight.duration))
			
			file.write('''
		</Change>
	</Update>
</gx:AnimatedUpdate>
			''')
		
		file.write('</gx:Playlist></gx:Tour>\n')


class FlightKMLAnimation(KMLAnimationGenerator):
	"""
	This class can create single-flight KML animations.

	"""

	def configure(self):
		"""
		Configure the single-flight animation.

		"""
		self.camera = FixedKMLCamera({}, {})
		flight = self.data
		self.components = [
			TrajectoryLine3DKMLComponent({flight.id: flight}, {}),
			FilledFlightpathKMLComponent({flight.id: flight}, {})
		]
		
	def writeAnimation(self, file):
		"""
		Write the single-flight animation.

		"""
		flight = self.data
		
		file.write('<gx:Tour><name>Flight Animation</name><gx:Playlist>\n')
		
		# loop through all flight datapoints
		for t in range(flight.data.shape[0]):

			# animate camera to current datapoint
			file.write(self.camera.timeStep(t))
			
			file.write('''
<gx:AnimatedUpdate>
	<gx:duration>1.0</gx:duration>
	<Update>
		<Change>
			''')
			
			# animate each component based on current datapoint
			for component in self.components:
				file.write(component.timeStep(flight, t))
			
			file.write('''
		</Change>
	</Update>
</gx:AnimatedUpdate>
			''')
		
		file.write('</gx:Playlist></gx:Tour>\n')