from abc import ABC, abstractmethod
import matplotlib.pyplot as plt

from aerovision.colors import Gradient

class KMLComponent(ABC):
	@abstractmethod
	def setup(self, flight):
		pass
	
	@abstractmethod
	def step(self, dataPoint):
		pass
	
	@abstractmethod
	def finish(self, flight):
		pass


class MultiTrajectoryLine3DKMLComponent(KMLComponent):
	def setup(self, flights):
		gradient = Gradient([500, 2000], ['#FF0000', '#FFFF00', '#00FF00'])

		setup = '''
<Folder> 
    <open>0</open>
    <name>3D Trajectories</name>
		'''

		for id in flights:
			flight = flights[id]

			opacity = '80'
			hue = gradient.getColor(flight.medianAltitude())
			color = opacity + hue
			setup += '''
<Placemark id="multi_trajectory_line_3D_placemark">
    <name>Flight ''' + id + ''' - ICAO24 ''' + flight.icao24 + '''</name>
    <Style>
		<LineStyle>
			<color>''' + color + '''</color>
			<width>3</width>
		</LineStyle>
		<PolyStyle>
			<color>''' + color + '''</color>
			<colorMode>normal</colorMode>
		</PolyStyle>
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
		coordinates = ''
		for index in range(0, flight.data.shape[0]):
			dataPoint = flight.dataPoints(index)
			coordinates += str(dataPoint.lon) + "," + str(dataPoint.lat) + "," + str(dataPoint.geoaltitude) + '\n'

		return '''
<LineString targetId="multi_trajectory_line_3D_''' + flight.id + '''">
	<coordinates>
		''' + coordinates + '''
	</coordinates>
</LineString>
		'''
	
	def finish(self, flight):
		return ""


class TrajectoryLine3DKMLComponent(KMLComponent):
	def __init__(self):
		self.coordinates = ""

	def setup(self, flight):
		return '''
<Style id='trajectory_line_3D_style'>
    <LineStyle>
        <color>60F0B414</color>
        <width>10</width>
    </LineStyle>
    <PolyStyle>
        <color>60F0B414</color>
        <colorMode>normal</colorMode>
    </PolyStyle>
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
	
	def step(self, dataPoint):
		self.coordinates += str(dataPoint.lon) + "," + str(dataPoint.lat) + "," + str(dataPoint.geoaltitude) + '\n'
		return '''
<LineString targetId='trajectory_line_3D'>
	<coordinates>
		''' + self.coordinates + '''
	</coordinates>
</LineString>
		'''
	
	def finish(self, flight):
		return ""


class FilledTrajectoryKMLComponent(KMLComponent):
	def __init__(self):
		self.coordinates = ""

	def setup(self, flight):
		return '''
<Style id='filled_trajectory_style'>
    <LineStyle>
        <color>60F0B414</color>
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
	
	def step(self, dataPoint):
		self.coordinates += str(dataPoint.lon) + "," + str(dataPoint.lat) + "," + str(dataPoint.geoaltitude) + '\n'
		return '''
<LineString targetId='filled_trajectory'>
	<coordinates>
		''' + self.coordinates + '''
	</coordinates>
</LineString>
		'''
	
	def finish(self, flight):
		return ""