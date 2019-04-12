import scipy.interpolate as interpolate
import numpy as np
import pylab as plt

# based on https://stackoverflow.com/questions/17913330/fitting-data-using-univariatespline-in-scipy-python

class Spline:
	def __init__(self, x, y, s):
		self.spline = interpolate.UnivariateSpline (x, y, s=s)
		#self.plotSpline(x, y)

	def interpolate(self, x):
		return self.spline(x)

	def plotSpline(self, x, y):
		y2 = []
		for t in x:
			y2.append(self.interpolate(t))

		plt.plot(x, y)
		plt.plot(x, y2)
		plt.show()

	def test(self):
		x = np.array(range(0, 10))
		y = np.array([2.004070, 1.588134, 1.760112, 1.771360, 1.860087,
			1.955789, 1.910408, 1.655911, 1.778952, 2.19])

		xx = np.arange(0,10,0.1)
		s1 = interpolate.InterpolatedUnivariateSpline (x, y)
		s2 = interpolate.UnivariateSpline (x, y, s=0.3)

		plt.plot (x, y, 'bo', label='Data')
		plt.plot (xx, s1(xx), 'k--', label='Spline')
		plt.plot (xx, s2(xx), 'r-', label='Spline, fit')
		plt.minorticks_on()
		plt.legend()
		plt.xlabel('x')
		plt.ylabel('y')
		plt.show()