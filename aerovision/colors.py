import matplotlib

class Gradient:
	def __init__(self, valueRange, colorSequence):
		self.lowerBound = valueRange[0]
		self.upperBound = valueRange[1]
		self.colorSequence = colorSequence

	def getColor(self, value):
		if value <= self.lowerBound:
			factor = 0.00001
		elif value >= self.upperBound:
			factor = 0.99999
		else:
			factor = (value - self.lowerBound) / (self.upperBound - self.lowerBound)

		colors = []
		for index in range(len(self.colorSequence)):
			if index == 0:
				colorFraction = 0
			elif index == (len(self.colorSequence) - 1):
				colorFraction = 1
			else:
				colorFraction = index / (len(self.colorSequence) - 1)
			color = self.colorSequence[index]
			colors.append((colorFraction, color))

		cmap = matplotlib.colors.LinearSegmentedColormap.from_list('', colors, N=256)
		rgb = cmap(factor)[:3]
		bgr = rgb[::-1]
		hex = matplotlib.colors.rgb2hex(bgr)[1:]
		return hex