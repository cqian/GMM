import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from joblib import Parallel, delayed  


# Gibbs Sampling
def sampling(data, K, maxIter, hyperMu, hyperSigma):
	N = len(data);

	# init constants
	Pi = [1.0/K]*K;

	# init prior
	mu = np.random.normal(hyperMu, hyperSigma, K);
	
	### using true parameters for debug
	z = np.random.multinomial(1, Pi, N).tolist(); 
	print "Init means";
	print mu;

	# assign data class based on z
	for i in range(N):
		data[i][2] = np.nonzero(z[i])[0].tolist()[0];

	const = hyperSigma*np.sqrt(2*np.pi);
	Approx_mu = [([0]*(K+1))]*maxIter;
	lnls = [([0]*2)]*maxIter;
	for iter in range(maxIter):
		if iter > 0 and lnls[iter][1]-lnls[iter-1][1] < 1e-5:
			print "Converged"
			break;

		if iter % (0.1*maxIter) == 0:
			print str(100*iter/maxIter) + "% is done";
		
		Approx_mu[iter] = mu.tolist();

		# sampling on means, U
		for k in range(K):
			nk = np.count_nonzero(data[:,2]==k);
			nk = nk if nk > 0 else 1;
			dk = data[data[:,2]==k];
			ave = np.average(dk, axis=0) if dk.size > 0 else [0]*3;
			ave = np.average(ave[0:2]);
			mu[k] = np.random.normal(ave, hyperSigma/np.sqrt(nk));

		# sampling on data labels, Z
		lnl = err = 0;
		for i in range(N):
			pz = [0]*K;

			# update z_i using logarithm
			sumExpPz = 0;
			for k in range(K):
				coff = np.log(Pi[k]/const);
				temp = coff - np.power(data[i][0:2]-mu[k],2)/(2*np.power(hyperSigma,2));
				pz[k] = sum(temp);
				sumExpPz += np.exp(pz[k]);

			pz = np.exp(pz)/sumExpPz if sumExpPz != 0 else 0;
			z[i] = np.random.multinomial(1, pz, size=1).tolist()[0];
			data[i][2] = np.nonzero(z[i])[0].tolist()[0];
			
			# compute complete log- likelihood
			k = int(data[i][2]);
			coff = np.log(Pi[k]/const);
			temp = coff - np.power(data[i][0:2]-mu[k],2)/(2*np.power(hyperSigma,2));
			lnl += sum(temp);

		lnls[iter] = [iter, lnl];
		
	return [data, lnls, Approx_mu, Pi];


