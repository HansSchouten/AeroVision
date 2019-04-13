import matplotlib

class Gradient:
	"""
	This class can create color gradients.

	"""

	def __init__(self, valueRange, colorSequence):
		self.lowerBound = valueRange[0]
		self.upperBound = valueRange[1]
		self.colorSequence = colorSequence

	def getColor(self, value):
		"""
		Return the BGR hex color code of the given value.

		"""
		# compute the factor of the given value between the pre-set bounds
		if value <= self.lowerBound:
			factor = 0.00001
		elif value >= self.upperBound:
			factor = 0.99999
		else:
			factor = (value - self.lowerBound) / (self.upperBound - self.lowerBound)

		# create a list of colors and their transition point based on the pre-set colors
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

		# create the gradient color map
		cmap = matplotlib.colors.LinearSegmentedColormap.from_list('', colors, N=256)
		# get RGB values
		rgb = cmap(factor)[:3]
		# create the BGR values
		bgr = rgb[::-1]
		# transform array of floats to hex and remove the # character
		hex = matplotlib.colors.rgb2hex(bgr)[1:]

		return hex