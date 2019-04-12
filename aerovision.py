import sys

from aerovision.parsers import FlightParser
from aerovision.kml.animator import MultiFlightKMLAnimator

def main(argv):
	parser = FlightParser()
	flights = parser.getFlights("data/flights.csv")
	
	animator = MultiFlightKMLAnimator(flights)
	animator.generateKML("output/flights.kml")

if __name__ == "__main__":
	main(sys.argv)