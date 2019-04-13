from abc import ABC, abstractmethod

from aerovision.kml.cameras import *
from aerovision.kml.components import *

class KMLGenerator(ABC):
	"""
	This abstract class defines the structure of a KML Generator.

	"""

	def __init__(self, data):
		self.data = data
		self.configure()
		
	@abstractmethod
	def configure(self):
		"""
		Configure the KML Generator.

		"""
		pass
	
	def generateKML(self, outFile):
		"""
		Generate a KML file at the given path.

		"""
		file = open(outFile, "w")
		self.writeDocumentStart(file)
		self.writeDocumentBody(file)
		self.writeDocumentEnd(file)
		file.close()

	def writeDocumentStart(self, file):
		"""
		Write the document start to the file.

		"""
		file.write('<kml xmlns="http://www.opengis.net/kml/2.2" '
			'xmlns:atom="http://www.w3.org/2005/Atom" '
			'xmlns:gx="http://www.google.com/kml/ext/2.2" '
			'xmlns:kml="http://www.opengis.net/kml/2.2">\n')
		file.write('<Document>\n')

	@abstractmethod
	def writeDocumentBody(self, file):
		"""
		Write the document body to the file.

		"""
		pass

	def writeDocumentEnd(self, file):
		"""
		Write the document end to the file.

		"""
		file.write('</Document>\n')
		file.write('</kml>')