from abc import ABC, abstractmethod

from aerovision.kml.cameras import TopViewKMLCamera
from aerovision.kml.components import *

class KMLAnimator(ABC):
	def __init__(self, data):
		self.data = data
		self.configure()
		
	@abstractmethod
	def configure(self):
		pass

	def generateKML(self, outFile):		
		file = open(outFile, "w")
		file.write('<kml xmlns="http://www.opengis.net/kml/2.2" '
			'xmlns:atom="http://www.w3.org/2005/Atom" '
			'xmlns:gx="http://www.google.com/kml/ext/2.2" '
			'xmlns:kml="http://www.opengis.net/kml/2.2">\n')
		file.write('<Document>\n')
		
		# camera setup
		file.write(self.camera.setup(self.data))
		
		# write the pre-animation configuration of each component
		for component in self.components:
			file.write(component.setup(self.data))
		
		# write animation
		self.writeAnimation(file)
		
		# write the post-animation configuration of each component
		for component in self.components:
			file.write(component.finish(self.data))
		
		file.write('</Document>\n')
		file.write('</kml>')
		file.close()
		
	@abstractmethod
	def writeAnimation(self, file):
		pass


class MultiFlightKMLAnimator(KMLAnimator):
	def configure(self):
		self.camera = TopViewKMLCamera()
		self.components = [MultiTrajectoryLine3DKMLComponent()]
		
	def writeAnimation(self, file):
		flights = self.data
		
		file.write('<gx:Tour><name>Flights Animation</name><gx:Playlist>\n');
		
		# loop through all flights
		for id in flights:
			flight = flights[id]

			# animate camera to current flight
			file.write(self.camera.step(flight))
			
			file.write('''
<gx:AnimatedUpdate>
	<gx:duration>0</gx:duration>
	<Update>
		<Change>
			''')
			
			# animate each component based on current flight
			for component in self.components:
				file.write(component.step(flight))
			
			file.write('''
		</Change>
	</Update>
</gx:AnimatedUpdate>
			''')
		
		file.write('</gx:Playlist></gx:Tour>\n');


class SingleFlightKMLAnimator(KMLAnimator):
	def configure(self):
		self.camera = TopViewKMLCamera()
		self.components = [FilledTrajectoryKMLComponent()]
		
	def writeAnimation(self, file):
		flight = self.data
		
		file.write('<gx:Tour><name>Flight Animation</name><gx:Playlist>\n');
		
		# loop through all flight datapoints
		for t in range(flight.data.shape[0]):

			# animate camera to current datapoint
			file.write(self.camera.step(t))
			
			file.write('''
<gx:AnimatedUpdate>
	<gx:duration>1.0</gx:duration>
	<Update>
		<Change>
			''')
			
			# animate each component based on current datapoint
			for component in self.components:
				file.write(component.step(t))
			
			file.write('''
		</Change>
	</Update>
</gx:AnimatedUpdate>
			''')
		
		file.write('</gx:Playlist></gx:Tour>\n');