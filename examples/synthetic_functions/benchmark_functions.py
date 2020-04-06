#!/usr/bin/env python

import numpy as np 

#=========================================================================

class CategoricalEvaluator(object):

	def __init__(self, num_dims = 2, num_opts = 10):
		self.num_dims = num_dims
		self.num_opts = num_opts

	def __call__(self, *args, **kwargs):
		if 'sample' in kwargs:
			sample = kwargs['sample']
		else:
			sample = args[0]
		vector = np.array([round(float(entry[2:])) for entry in np.squeeze(sample)])
		return self.evaluate(sample = vector)

#=========================================================================

class Ackley(CategoricalEvaluator):
	'''
		Ackley is to be evaluated on the hypercube 
		x_i in [-32.768, 32.768] for i = 1, ..., d
	'''
	def ackley(self, vector, a = 20., b = 0.2, c = 2. * np.pi):
		result = - a * np.exp( - b * np.sqrt( np.sum(vector**2) / self.num_dims ) ) - np.exp( np.sum(np.cos(c * vector)) ) + a + np.exp(1)
		return result

	def evaluate(self, sample):	
		# map sample onto hypercube
		vector = np.zeros(self.num_dims)	
		for index, element in enumerate(sample):
			vector[index] = 65.536 * ( element / float(self.num_opts - 1) ) - 32.768
		return self.ackley(vector)

#=========================================================================

class Camel(CategoricalEvaluator):
	'''
		Camel is to be evaluated on the hypercube 
		x_i in [-3, 3] for i = 1, ..., d
	'''
	def camel(self, vector):
		result = 0.

		# global minima
		loc_0 = np.array([-1., 0.])
		loc_1 = np.array([ 1., 0.])		
		weight_0 = np.array([4., 1.])
		weight_1 = np.array([4., 1.])

		# local minima
		loc_2  = np.array([-1., 1.5])
		loc_3  = np.array([ 1., -1.5])
		loc_5  = np.array([-0.5, -1.0])
		loc_6  = np.array([ 0.5,  1.0])
		loss_0 = np.sum(weight_0 * (vector - loc_0)**2) + 0.01 + np.prod(vector - loc_0)
		loss_1 = np.sum(weight_1 * (vector - loc_1)**2) + 0.01 + np.prod(vector - loc_1)
		loss_2 = np.sum((vector - loc_2)**2) + 0.075
		loss_3 = np.sum((vector - loc_3)**2) + 0.075
		loss_5 = 3000. * np.exp( - np.sum((vector - loc_5)**2) / 0.25)
		loss_6 = 3000. * np.exp( - np.sum((vector - loc_6)**2) / 0.25)
		result = loss_0 * loss_1 * loss_2 * loss_3 + loss_5 + loss_6
		return result

	def evaluate(self, sample):	
		# map sample onto hypercube
		vector = np.zeros(self.num_dims)
		for index, element in enumerate(sample):
			vector[index] = 6 * ( element / float(self.num_opts) ) - 3
		return self.camel(vector)

#=========================================================================

class Dejong(CategoricalEvaluator):
	'''
		Dejong is to be evaluated on the hypercube 
		x_i in [-5.12, 5.12] for i = 1, ..., d
	'''
	def dejong(self, vector):
		result = np.sum(vector**2)
		return result


	def evaluate(self, sample):	
		# map sample onto hypercube
		vector = np.zeros(self.num_dims)
		for index, element in enumerate(sample):
			vector[index] = 10.24 * ( element / float(self.num_opts - 1) ) - 5.12
		return self.dejong(vector)

#=========================================================================

class Michalewicz(CategoricalEvaluator):
	'''
		Michalewicz is to be evaluated on the hypercube 
		x_i in [0, pi] for i = 1, ..., d
	'''

	def michalewicz(self, vector, m = 10.):
		result = 0.
		for index, element in enumerate(vector):
			result += - np.sin(element) * np.sin( (index + 1) * element**2 / np.pi)**(2 * m)
		return result

	def evaluate(self, sample):	
		# map sample onto hypercube
		vector = np.zeros(self.num_dims)
		for index, element in enumerate(sample):
			vector[index] = np.pi * element / float(self.num_opts - 1)
		return self.michalewicz(vector)

#=========================================================================


class Slope(CategoricalEvaluator):
	'''
		Response sampled from standard normal distribution 
		with correlation
	'''
	def random_correlated(self, vector):
		seed   = 0
		vector = np.array(vector)
		for index, element in enumerate(vector):
			seed += self.num_opts**index * element
		result = np.sum(vector / self.num_opts)
		return result

	def evaluate(self, sample):
		return self.random_correlated(sample)

#=========================================================================

class RandomCorrelated(CategoricalEvaluator):
	'''
		Response sampled from standard normal distribution 
		with correlation
	'''

	correlation = 2.0

	def random_correlated(self, vector):
		seed = 0
		for index, element in enumerate(vector):
			seed += self.num_opts**index * element
		np.random.seed(seed)
		result = np.random.normal() + np.sum(vector / self.num_opts) * self.correlation
		return result

	def evaluate(self, sample):
		return self.random_correlated(sample)

#=========================================================================

class RandomUncorrelated(CategoricalEvaluator):
	'''
		Response sampled from standard normal distribution 
		without correlation
	'''
	def random_uncorrelated(self, vector):
		seed = 0
		for index, element in enumerate(vector):
			seed += self.num_opts**index * element
		np.random.seed(seed)
		result = np.random.normal()
		return result

	def evaluate(self, sample):
		return self.random_uncorrelated(sample)

#=========================================================================

if __name__ == '__main__':

	import matplotlib.pyplot as plt 
	import seaborn as sns

	# choose your favorite benchmark function
	benchmark = Ackley
#	benchmark = Camel
#	benchmark = Dejong
#	benchmark = Michalewicz
#	benchmark = Slope
#	benchmark = RandomCorrelated
#	benchmark = RandomUncorrelated

	num_opts  = 21
	func      = benchmark(num_dims = 2, num_opts = num_opts)

	domain = np.arange(num_opts)
	Z      = np.zeros((num_opts, num_opts))
	for x_index, x in enumerate(domain):
		for y_index, y in enumerate(domain):
			Z[y_index, x_index] = func(np.array([x, y]))

	plt.imshow(Z, origin = 'lower', cmap = plt.get_cmap('YlGnBu'))
	plt.colorbar()
	plt.title(func.__class__.__name__)
	plt.xlabel('x0')
	plt.ylabel('x1')
	plt.show()


