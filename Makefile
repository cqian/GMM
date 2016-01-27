MU = 0
SIGMA = 1
K = 3
SIZE = 1000
MAXITER = 100

sim:
	python main.py 0 1 $(SIZE) $(K) $(MU) $(SIGMA) sim

sample:
	python main.py 1 simData0.dat $(MAXITER) $(K) $(MU) $(SIGMA) sampled

store:
	mv *.dat *.log *.pdf ../dat/GMM-GS

clean:
	rm *.log *.dat *.pdf *.pyc *.*~ *~
