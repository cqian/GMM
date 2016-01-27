import argparse
import sys
from gmm import *
from gibbs import *


def simGMM(rep, K, N, hyperMu, hyperSigma, outputPrefix):
	# sim multiple times
	Pi = buildPi(0, 1, K);
	[means, sigmas] = buildSubModels(hyperMu, hyperSigma, K);
	data = drawFromGMM(Pi, means, sigmas, N);

	# output sim data
	print 'Pi: ';
	print Pi*100;
	print 'Means: ';
	print means;
	print 'Sds: '
	print sigmas;
	f = open(outputPrefix+'Params'+str(rep)+'.dat', 'wb');
	f.write("K\n%d" % K);
	f.write("\nPi\n");
	for item in Pi:
		f.write("%f\t" % item);
	f.write("\nMeans\n");
	for item in means:
		f.write("%f\t" % item);
	f.write("\nSigmas\n");
	for item in sigmas:
		f.write("%f\t" % item);
	f.close();

	np.savetxt(outputPrefix+'Data'+str(rep)+'.dat', data, fmt="%.5f\t");
	plotData2D(data, K);
	plotGMM(data, means, sigmas, Pi, K);
	plt.draw();
	plt.savefig(outputPrefix+'Data'+str(rep)+'.pdf');
	plt.show();
	

def gibbs(inputData, K, maxIter, hyperMu, hyperSigma, outputPrefix):
	# load data
	data = np.loadtxt(inputData);
	N = len(data);

	print 'Start Gibbs Sampling';
	[data, lnls, Approx_mu, Pi] = sampling(data, K, maxIter, hyperMu, hyperSigma);
	print "Sampled means";
	print np.average(Approx_mu, axis=0);
	np.savetxt(outputPrefix+'Data.dat', data, fmt="%.5e\t");
	np.savetxt(outputPrefix+'lnls.log', lnls, fmt="%d\t%.5f", header=str("T\tLnL"),comments='');	
	
	plt.plot([x[0] for x in lnls], [x[1] for x in lnls]);
	plt.xlabel('Iteration')
	plt.ylabel('Log likelihood')
	plt.savefig(outputPrefix+'lnl.pdf');

	x = np.arange(1,maxIter+1);
	approx_mu = np.column_stack((x,np.asarray(Approx_mu)));
	np.savetxt(outputPrefix+'Means.log', approx_mu, fmt="%.5f\t", comments='');

	plt.figure();
	plotData2D(data,K);
	plotGMM(data, np.average(Approx_mu, axis=0), [hyperSigma]*K, Pi, K);
	plt.savefig(outputPrefix+'Data.pdf');
	plt.show();


# build commandline parser
# code is from Stackflow
class commandlineParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


# Main function
def main():
	parser=commandlineParser()
	parser.add_argument('(1) If run GMM simulation: 0, If run Gibbs Samling: 1', nargs='+')
	parser.add_argument('(2) 0: the number of replicates, 1: input data', nargs='+')
	parser.add_argument('(3) 0: the number of data points, 1: the maximum number of iteration', nargs='+')
	parser.add_argument('(4) The number of components K', nargs='+')
	parser.add_argument('(5) Hyperparameter mu', nargs='+')
	parser.add_argument('(6) Hyperparameter sigma', nargs='+')
	parser.add_argument('(7) Prefix of output files', nargs='+')
	args=parser.parse_args()

	K = int(sys.argv[4])
	hyperMu = float(sys.argv[5])
	hyperSigma = float(sys.argv[6]);
	outputPrefix = sys.argv[7]
	prog = int(sys.argv[1]);
	if prog == 0:
		rep = int(sys.argv[2])
		N = int(sys.argv[3])
		for i in range(rep):
			simGMM(i, K, N, hyperMu, hyperSigma, outputPrefix);
	else:
		inputData = sys.argv[2]
		maxIter = int(sys.argv[3])
		gibbs(inputData, K, maxIter, hyperMu, hyperSigma, outputPrefix);


if __name__ == "__main__":
	main()


