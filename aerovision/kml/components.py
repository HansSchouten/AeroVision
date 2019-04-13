from abc import ABC, abstractmethod
import matplotlib.pyplot as plt

from aerovision.colors import Gradient

class KMLComponent(ABC):
	"""
	This abstract class defines the structure of a KML Component.

	"""

	@abstractmethod
	def setup(self, data):
		"""
		Return the KML Component structure setting up this component.

		"""
		return ""
	
	@abstractmethod
	def step(self, data):
		"""
		Return the KML Component structure added for each (animation, timespan, ..) step.

		"""
		return ""
	
	@abstractmethod
	def finish(self, data):
		"""
		Return the KML Component structure added to the bottom of a KLM file.

		"""
		return ""


class MultiTrajectoryLine3DKMLComponent(KMLComponent):
	"""
	This KML Component class creates 3D lines for multiple trajectories.

	"""

	def setup(self, flights):
		"""
		Return the KML structure defining styling for the multi-trajectory 3D lines.

		"""
		# create a color gradient between two altitude levels
		gradient = Gradient([500, 2000], ['#FF0000', '#FFFF00', '#00FF00'])

		setup = '''
<Folder> 
    <open>0</open>
    <name>Trajectories Line3D</name>
		'''
		
		# loop through all flights and define the 3D line style
		for id in flights:
			flight = flights[id]

			opacity = '80'
			color = opacity + gradient.getColor(flight.medianAltitude())
			setup += '''
<Placemark id="multi_trajectory_line_3D_placemark">
    <name>Flight ''' + id + ''' - ICAO24 ''' + flight.icao24 + '''</name>
    <Style>
		<LineStyle>
			<color>''' + color + '''</color>
			<width>3</width>
		</LineStyle>
    </Style>
    <LineString id="multi_trajectory_line_3D_''' + id + '''">
        <extrude>0</extrude>
        <tesselate>0</tesselate>
        <altitudeMode>absolute</altitudeMode>
        <coordinates>
        </coordinates>
    </LineString>
</Placemark>
			'''

		setup += '''
</Folder>
		'''
		return setup
	
	def step(self, flight):
		"""
		Return the KML structure defining the 3D line for the given flight.

		"""
		# add coordinates for each moment in time
		coordinates = ''
		for t in range(flight.data.shape[0]):
			coordinates += str(flight.getLon(t)) + "," + str(flight.getLat(t)) + "," + str(flight.getAlt(t)) + '\n'

		return '''
<LineString targetId="multi_trajectory_line_3D_''' + flight.id + '''">
	<coordinates>
		''' + coordinates + '''
	</coordinates>
</LineString>
		'''


class MultiTrajectoryFilledKMLComponent(KMLComponent):
	"""
	This KML Component class creates filled areas below multiple flightpaths.

	"""

	def setup(self, flights):
		"""
		Return the KML structure defining styling for the multi-trajectory filled vertical flightpaths.

		"""
		# create a color gradient between two altitude levels
		gradient = Gradient([500, 2000], ['#FF0000', '#FFFF00', '#00FF00'])

		setup = '''
<Folder> 
    <open>0</open>
    <name>Trajectories Filled</name>
		'''

		# loop through all flights and define the filled flightpath style
		for id in flights:
			flight = flights[id]

			color = gradient.getColor(flight.medianAltitude())
			setup += '''
<Placemark id="multi_trajectory_filled_placemark">
    <name>Flight ''' + id + ''' - ICAO24 ''' + flight.icao24 + '''</name>
    <Style>
		<LineStyle>
			<width>0</width>
		</LineStyle>
		<PolyStyle>
			<color>20''' + color + '''</color>
			<colorMode>normal</colorMode>
			<fill>1</fill>
		</PolyStyle>
    </Style>
    <LineString id="multi_trajectory_filled_''' + id + '''">
        <extrude>1</extrude>
        <tesselate>1</tesselate>
        <altitudeMode>absolute</altitudeMode>
        <coordinates>
        </coordinates>
    </LineString>
</Placemark>
			'''

		setup += '''
</Folder>
		'''
		return setup
	
	def step(self, flight):
		"""
		Return the KML structure defining the filled vertical flightpath for the given flight.

		"""
		# add coordinates for each moment in time
		coordinates = ''
		for t in range(flight.data.shape[0]):
			coordinates += str(flight.getLon(t)) + "," + str(flight.getLat(t)) + "," + str(flight.getAlt(t)) + '\n'

		return '''
<LineString targetId="multi_trajectory_filled_''' + flight.id + '''">
	<coordinates>
		''' + coordinates + '''
	</coordinates>
</LineString>
		'''


class TrajectoryLine3DKMLComponent(KMLComponent):
	"""
	This KML Component class create a 3D line for a single trajectory.

	"""

	def setup(self, flight):
		"""
		Return the KML structure defining styling for the single-trajectory 3D line.

		"""
		self.flight = flight
		self.coordinates = ""
		return '''
<Style id='trajectory_line_3D_style'>
    <LineStyle>
        <color>60F0B414</color>
        <width>10</width>
    </LineStyle>
</Style>
<Placemark id='trajectory_line_3D_placemark'>
    <name>TrajectoryLine3D</name>
    <styleUrl>#trajectory_line_3D_style</styleUrl>
    <LineString id='trajectory_line_3D'>
        <extrude>0</extrude>
        <tesselate>0</tesselate>
        <altitudeMode>absolute</altitudeMode>
        <coordinates>
        </coordinates>
    </LineString>
</Placemark>
		'''
	
	def step(self, t):
		"""
		Return the KML structure defining the 3D line for the given moment in time.

		"""
		self.coordinates += str(self.flight.getLon(t)) + "," + str(self.flight.getLat(t)) + "," + str(self.flight.getAlt(t)) + '\n'
		return '''
<LineString targetId='trajectory_line_3D'>
	<coordinates>
		''' + self.coordinates + '''
	</coordinates>
</LineString>
		'''


class FilledTrajectoryKMLComponent(KMLComponent):
	"""
	This KML Component class create a filled area below a single flightpath.

	"""

	def setup(self, flight):
		"""
		Return the KML structure defining styling for the single-trajectory filled vertical flightpath.

		"""
		self.flight = flight
		self.coordinates = ""
		return '''
<Style id='filled_trajectory_style'>
    <LineStyle>
        <width>0</width>
    </LineStyle>
    <PolyStyle>
        <color>60F0B414</color>
        <colorMode>normal</colorMode>
        <fill>1</fill>
    </PolyStyle>
</Style>
<Placemark id='filled_trajectory_placemark'>
    <name>FilledTrajectory</name>
    <styleUrl>#filled_trajectory_style</styleUrl>
    <LineString id='filled_trajectory'>
        <extrude>1</extrude>
        <tesselate>1</tesselate>
        <altitudeMode>absolute</altitudeMode>
        <coordinates>
        </coordinates>
    </LineString>
</Placemark>
		'''
	
	def step(self, t):
		"""
		Return the KML structure defining the filled vertical flightpath for the given moment in time.

		"""
		self.coordinates += str(self.flight.getLon(t)) + "," + str(self.flight.getLat(t)) + "," + str(self.flight.getAlt(t)) + '\n'
		return '''
<LineString targetId='filled_trajectory'>
	<coordinates>
		''' + self.coordinates + '''
	</coordinates>
</LineString>
		'''