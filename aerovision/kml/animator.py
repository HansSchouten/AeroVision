from abc import ABC, abstractmethod

from aerovision.kml.cameras import TopViewKMLCamera
from aerovision.kml.components import TrajectoryKMLComponent

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


class SingleFlightKMLAnimator(KMLAnimator):
	def configure(self):
		self.camera = TopViewKMLCamera()
		self.components = [TrajectoryKMLComponent()]
		
	def writeAnimation(self, file):
		flight = self.data
		
		file.write('<gx:Tour><name>Flight animation</name><gx:Playlist>\n');
		
		# loop through all flight datapoints
		for dataPoint in flight.data.iterrows():
			# animate camera to current datapoint
			file.write(self.camera.step(dataPoint))
			
			file.write('''
<gx:AnimatedUpdate>
	<gx:duration>1.0</gx:duration>
	<Update>
		<Change>
			''')
			
			# animate each component based on current datapoint
			for component in self.components:
				file.write(component.step(dataPoint))
			
			file.write('''
		</Change>
	</Update>
</gx:AnimatedUpdate>
			''')
		
		file.write('</gx:Playlist></gx:Tour>\n');