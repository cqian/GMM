from __future__ import division
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


# build stationary distribution Pi of each sub-model
# Pi can be viewed as weights of each sub-model
def buildPi(start, end, k):
	# using dirichlet distro
	Pi = np.random.dirichlet(([1]*k), 1)[0];
	return Pi;


# build sub-models
# each model is generated randomly from a given normal distribution.
def buildSubModels(mu, sigma, K):
	means = np.random.normal(mu, sigma, K);
	sds = abs(np.random.normal(mu, sigma, K));
	return [means, sds];


# Simulate data from the Gaussian Mixture Model
# The model is built with given sub-models and their weights
# GMM = Pi_1 * N(mu_1, sigma_1) + .. + Pi_k * (mu_k, sigma_k)
def drawFromGMM(Pi, means, sds, N):
	data = np.empty([N,3]);

	# using numpy multinomial dist
	z = np.random.multinomial(1, Pi, N).tolist();
	for i in range(N):
		k = np.nonzero(z[i])[0].tolist()[0];
		data[i:,] = np.random.normal(means[k], sds[k], 3);
		data[i,2] = k;
	return data;


# Plot True Gaussian Mixture Model (GMM)
# The model is built with given sub-models and their weights
# GMM = Pi_1 * N(mu_1, sigma_1) + .. + Pi_k * (mu_k, sigma_k)
def gaussian_1d(data, Pi, means, sds, N, K):
	x = np.linspace(min(data), max(data), N);
	gmm = 0*mlab.normpdf(x,0,1);
	for i in range(len(Pi)):
		gmm += Pi[i]*mlab.normpdf(x,means[i],sds[i]);
	
	plt.plot(x, gmm);
	

# Plot 2d data
def plotData2D(data, K):
	for i in range(K):
		component = data[data[:,2]==i];
		plt.scatter(component[:,0], component[:,1], 
			c=[np.random.uniform(0,1,3)], alpha=0.8);
		

# Represent GMM in 2D
def gaussian_2d(x, y, x0, y0, xsig, ysig):
	return 1/(2*np.pi*xsig*ysig) \
		* np.exp(-0.5*(((x-x0) / xsig)**2 + ((y-y0) / ysig)**2))


# Plot 2D GMM with eclipse
def plotGMM(data, means, sds, Pi, K):
	delta = 0.025;
	x = np.arange(min(data[:,0]), max(data[:,0]), delta);
	y = np.arange(min(data[:,1]), max(data[:,1]), delta);
	X, Y = np.meshgrid(x, y);

	for i in range(K):
		Z = Pi[i]*gaussian_2d(X, Y,means[i], means[i], sds[i], sds[i]);
		plt.contour(x, y, Z, linewidths=0.5);



