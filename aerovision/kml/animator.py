from abc import ABC, abstractmethod

from aerovision.kml.cameras import TopViewKMLCamera
from aerovision.kml.components import TrajectoryKMLComponent

class KMLAnimatorInterface(ABC):
	def __init__(self, data):
		self.data = data
		self.configure()
		
	@abstractmethod
	def configure(self):
		pass

	def generateKML(self, outFile):		
		f = open(outFile, "w")
		f.write('<kml xmlns="http://www.opengis.net/kml/2.2" '
			'xmlns:atom="http://www.w3.org/2005/Atom" '
			'xmlns:gx="http://www.google.com/kml/ext/2.2" '
			'xmlns:kml="http://www.opengis.net/kml/2.2">')
		f.write('<Document>')
		
		# camera setup
		f.write(self.camera.setup(self.data))
		
		# setup each component
		for component in self.components:
			f.write(component.setup(self.data))
			
		self.writeAnimation(f)
		
		f.write('</Document>')
		f.write('</kml>')
		f.close()
		
	@abstractmethod
	def writeAnimation(self, file):
		pass


class SingleFlightKMLAnimator(KMLAnimatorInterface):
	def configure(self):
		self.camera = TopViewKMLCamera()
		self.components = [TrajectoryKMLComponent()]
		
	def writeAnimation(self, f):
		flight = self.data
		
		for dataPoint in flight.data.iterrows():
			f.write('''
<gx:AnimatedUpdate>
	<gx:duration>1.0</gx:duration>
	<Update>
		<Change>
			''')
			
			for component in self.components:
				f.write(component.step(dataPoint))
			
			f.write('''
		</Change>
	</Update>
</gx:AnimatedUpdate>
			''')