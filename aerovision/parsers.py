import pandas as pd

from aerovision.flight import Flight

class FlightParser:		
	def getFlights(self, dataFile):
		flightsDF = pd.read_csv(dataFile)
		aircraftIds = flightsDF.icao24.unique()
		flights = {el : pd.DataFrame for el in aircraftIds}
		for aircraftId in flights.keys():
			trajectory = flightsDF[:][flightsDF.icao24 == aircraftId]
			flights[aircraftId] = Flight(trajectory)
		return flights