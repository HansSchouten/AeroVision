from abc import ABC, abstractmethod
import matplotlib.pyplot as plt

from aerovision.colors import Gradient

class KMLComponent(ABC):
	"""
	This abstract class defines the structure of a KML Component.

	"""

	def __init__(self, flights, config):
		self.flights = flights
		self.config = config

	def setup(self):
		"""
		Return the KML Component structure setting up this component.

		"""
		return ""

	def allCoordinates(self, flight):
		"""
		Return the coordinates for plotting the entire flight at once.

		"""
		coordinates = ''
		for t in range(flight.data.shape[0]):
			coordinates += str(flight.getLon(t)) + "," + str(flight.getLat(t)) + "," + str(flight.getAlt(t)) + '\n'
		return coordinates
	
	def timeStep(self, flight, t):
		"""
		Return the KML Component structure for a given animation timeframe (sec).

		"""
		return ""

	def toXMLTime(self, timestamp):
		"""
		Transform a datetime object into an XML time string.
		See: https://developers.google.com/kml/documentation/time?csw=1#how-to-specify-time
		
		"""
		return timestamp.strftime('%Y-%m-%dT%H:%M:%S')
	

class TrajectoryLine3DKMLComponent(KMLComponent):
	"""
	This KML Component class creates 3D lines for trajectories.

	"""

	def setup(self):
		"""
		Return the KML structure defining the styling and initial setup of the trajectory 3D lines.

		"""
		# create a color gradient between two altitude levels
		gradient = Gradient([500, 2000], ['#FF0000', '#FFFF00', '#00FF00'])

		setup = '''
<Folder> 
	<open>0</open>
	<name>Trajectory Line3D</name>
		'''
		
		# loop through all flights and define the 3D line style
		for flightId in self.flights:
			flight = self.flights[flightId]

			opacity = '80'
			color = opacity + gradient.getColor(flight.medianAltitude())

			# define the timespan, if enabled
			timespan = ''
			coordinates = ''
			if 'useTimespan' in self.config:
				timespan = '''
		<TimeSpan>
			<begin>''' + self.toXMLTime(flight.startTime()) + '''</begin>
			<end>''' + self.toXMLTime(flight.endTime()) + '''</end>
		</TimeSpan>
				'''
				# preload coordinates of the entire flight
				coordinates = self.allCoordinates(flight)

			# append the setup with data for this flight
			setup += '''
	<Placemark id="trajectory_line_3D_placemark">
		<name>Flight ''' + flightId + ''' - ICAO24 ''' + flight.icao24 + '''</name>
		''' + timespan + '''
		<Style>
			<LineStyle>
				<color>''' + color + '''</color>
				<width>3</width>
			</LineStyle>
		</Style>
		<LineString id="trajectory_line_3D_''' + flightId + '''">
			<extrude>0</extrude>
			<tesselate>0</tesselate>
			<altitudeMode>absolute</altitudeMode>
			<coordinates>
				''' + coordinates + '''
			</coordinates>
		</LineString>
	</Placemark>
			'''

		setup += '''
</Folder>
		'''
		return setup

	def timeStep(self, flight, tMax):
		"""
		Return the KML structure defining the 3D line up to the given moment in time.

		"""
		coordinates = ''
		for t in range(tMax):
			coordinates += str(flight.getLon(t)) + "," + str(flight.getLat(t)) + "," + str(flight.getAlt(t)) + '\n'

		return '''
<LineString targetId="trajectory_line_3D_''' + flight.id + '''">
	<coordinates>
		''' + coordinates + '''
	</coordinates>
</LineString>
		'''


class FilledFlightpathKMLComponent(KMLComponent):
	"""
	This KML Component class creates filled areas below flightpaths.

	"""

	def setup(self):
		"""
		Return the KML structure defining styling and the initial setup for the filled vertical flightpaths.

		"""
		# create a color gradient between two altitude levels
		gradient = Gradient([500, 2000], ['#FF0000', '#FFFF00', '#00FF00'])

		setup = '''
<Folder> 
    <open>0</open>
    <name>Trajectory Vertical Flightpath</name>
		'''

		# loop through all flights and define the filled flightpath style
		for flightId in self.flights:
			flight = self.flights[flightId]
			
			opacity = '60'
			color = opacity + gradient.getColor(flight.medianAltitude())

			# define the timespan, if enabled
			timespan = ''
			coordinates = ''
			if 'useTimespan' in self.config:
				timespan = '''
		<TimeSpan>
			<begin>''' + self.toXMLTime(flight.startTime()) + '''</begin>
			<end>''' + self.toXMLTime(flight.endTime()) + '''</end>
		</TimeSpan>
				'''
				# preload coordinates of the entire flight
				coordinates = self.allCoordinates(flight)

			setup += '''
	<Placemark id="trajectory_filled_placemark">
		<name>Flight ''' + flightId + ''' - ICAO24 ''' + flight.icao24 + '''</name>
		<Style>
			<LineStyle>
				<width>0</width>
			</LineStyle>
			<PolyStyle>
				<color>''' + color + '''</color>
				<colorMode>normal</colorMode>
				<fill>1</fill>
			</PolyStyle>
		</Style>
		<LineString id="trajectory_filled_''' + flightId + '''">
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
	
	def timeStep(self, flight, tMax):
		"""
		Return the KML structure defining the filled vertical flightpath up to the given moment in time.

		"""
		coordinates = ''
		for t in range(tMax):
			coordinates += str(flight.getLon(t)) + "," + str(flight.getLat(t)) + "," + str(flight.getAlt(t)) + '\n'

		return '''
<LineString targetId="trajectory_filled_''' + flight.id + '''">
	<coordinates>
		''' + coordinates + '''
	</coordinates>
</LineString>
		'''