from abc import ABC, abstractmethod

class KMLComponentInterface(ABC):
	@abstractmethod
	def setup(self, flight):
		pass
	
	@abstractmethod
	def step(self, dataPoint):
		pass
	
	@abstractmethod
	def finish(self, flight):
		pass


class TrajectoryKMLComponent(KMLComponentInterface):
	def setup(self, flight):
		return ""
	
	def step(self, dataPoint):
		return ""
	
	def finish(self, flight):
		return ""