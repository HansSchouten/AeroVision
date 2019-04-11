from abc import ABC, abstractmethod

class KMLCameraInterface(ABC):
	@abstractmethod
	def setup(self, flight):
		pass
	
	@abstractmethod
	def step(self, dataPoint):
		pass
	
	@abstractmethod
	def finish(self, flight):
		pass


class TopViewKMLCamera(KMLCameraInterface):
	def setup(self, flight):
		return ""
	
	def step(self, dataPoint):
		return ""
	
	def finish(self, flight):
		return ""