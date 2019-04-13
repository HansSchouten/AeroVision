import sys

from aerovision.parsers import FlightParser
from aerovision.kml.generators.animation import *
from aerovision.kml.generators.timespan import *

def main(argv):
	"""
	AeroVision entry point.

	"""
	parser = FlightParser()
	flights = parser.getFlights("data/flights.csv")
	
	generator = FlightsKMLAnimation(flights)
	generator.generateKML("output/flights.kml")


if __name__ == "__main__":
	main(sys.argv)