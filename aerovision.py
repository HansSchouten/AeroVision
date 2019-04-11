import sys

from aerovision.parsers import FlightParser
from aerovision.kml.animator import SingleFlightKMLAnimator

def main(argv):
	parser = FlightParser()
	flights = parser.getFlights("data/flights.csv")
	flight = flights['4844c6']
	
	animator = SingleFlightKMLAnimator(flight)
	animator.generateKML("output/animation.kml")

if __name__ == "__main__":
	main(sys.argv)