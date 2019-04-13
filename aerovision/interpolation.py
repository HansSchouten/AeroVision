import scipy.interpolate as interpolate
import numpy as np
import pylab as plt

class Spline:
	"""
	This class can create a spline from a given dataset.

	"""

	def __init__(self, x, y, s):
		self.spline = interpolate.UnivariateSpline (x, y, s=s)
		#self.plotSpline(x, y)

	def interpolate(self, x):
		"""
		Calculate the spline interpolated value for the given x.

		"""
		return self.spline(x)

	def plotSpline(self, x, y):
		"""
		Plot the spline interpolation of the given x and y values.

		"""
		# compute fit
		yFit = []
		for v in x:
			yFit.append(self.interpolate(v))

		# plot results
		plt.plot (x, y, 'bo', label='Original')
		plt.plot (x, yFit, 'r-', label='Spline fit')
		plt.minorticks_on()
		plt.legend()
		plt.xlabel('x')
		plt.ylabel('y')
		plt.show()