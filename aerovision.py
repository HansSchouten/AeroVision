import sys, getopt

from aerovision.parsers import FlightParser
from aerovision.kml.generators.animation import *
from aerovision.kml.generators.timespan import *

def main(argv):
	"""
	AeroVision entry point.

	"""
	# default arguments
	flightsFile = "data/flights.csv"
	outFile = "output/flights.kml"
	visualisation = "animation"

	# parse command line arguments
	try:
		opts, args = getopt.getopt(argv,"hf:o:v:",["flights=","out=","visualisation="])
	except getopt.GetoptError:
		print('aerovision.py -f <flightsFile> -o <outputfile> -v timespan|animation')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('aerovision.py -f <flightsFile> -o <outputfile> -v timespan|animation')
			sys.exit()
		if opt in ('-f', '--flights'):
			flightsFile = arg
		elif opt in ('-o', '--out'):
			outFile = arg
		elif opt in ('-v', '--visualisation'):
			visualisation = arg
			
	parser = FlightParser()
	flights = parser.getFlights(flightsFile)
	
	generator = FlightsKMLAnimation(flights)
	if visualisation == 'timespan':
		generator = FlightsKMLTimespan(flights)

	generator.generateKML(outFile)


if __name__ == "__main__":
	main(sys.argv[1:])