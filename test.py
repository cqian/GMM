import numpy as np
import matplotlib.pyplot as plt
# from matplotlib.colors import LogNorm

# multinomial = np.random.multinomial(1, [0.2,0.4], size=1)
# dirichlet = np.random.dirichlet((10, 5, 3), 20).transpose()


def loadTrueParams(fname):
	K = 1
	Pi = []
	means = []
	sigmas = []
	with open (fname, 'r') as f:
		lines = f.readlines();
	for l in range(len(lines)):
		if lines[l].find("K") == 0:
			l += 1
			K = int(lines[l])
		if lines[l].find("Pi") == 0:
			l += 1
			Pi = [float(x) for x in lines[l].split('\t')[:-1]];
		if lines[l].find("Means") == 0:
			l += 1
			means = [float(x) for x in lines[l].split('\t')[:-1]];
		if lines[l].find("Sigmas") == 0:
			l += 1
			sigmas = [float(x) for x in lines[l].split('\t')[:-1]];

	f.close();
	return K, Pi, means, sigmas


loadTrueParams('trueParams.dat')