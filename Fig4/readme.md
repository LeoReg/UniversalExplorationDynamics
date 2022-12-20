**Python programs to generate data:**

- Surface.py: to obtain the elapsed time between increments first observation of a surface S and S+2 for a 2d random walk.

- Islands.py: to obtain the elapsed time between increments first observation of a I and I+1 islands for a 1d Lévy flight.

- Starvation2d.py: to obtain the starvation time T_S on the 2d square lattice.

- Cov.py: to obtain the 2, 3 and 4 time covariance of a 1d Lévy flight.

- frBm.py: to obtain the \tau_n variables for fractional brownian motion. 

- TSAW.py: to obtain the \tau_n variables for true self avoiding random walks. 

**Data:**

> One can also find the data used to plot the different subfigures in Fig. 4 of the main text in DataFig4.zip (the subfigure associated to the data is indicated by the small letter after the 4):

- Perim4b_n*: left column is time t, right column is the probability of having \tau_P=t. * indicates the perimeter P (50, 100, 200) 

- Islands4c_n*: left column is time t, right column is the probability of having \tau_I=t. * indicates the number of islands I (50, 100, 200)

- Cov4d: the first column indicates t1, the second column t2/t1 and the third column the covariance at t1 and t2 of the number of distinct sites visited divided by the product of the expectations (Lévy flight 1d, \alpha=1.5).   

- Cov4e: the first column indicates t1, the second column t2, the third column t4/t3 and the fourth column the covariance at t1, t2, t3 and t4 of the number of distinct sites visited divided by the product of the expectations (Lévy flight 1d, \alpha=1.3).

- Starving4f: the first column indicates the metabolic time S, the second column the mean starvation time T_S for a 2d starving random walk.

- fbm4g_n*: left column is time t, right column is the probability of having \tau_n=t. * indicates the number of sites n (or in the case of the FBM of index H=0.4, the number of intervals) visited (20, 40, 80).

- fbm4h_n*: left column is time t, right column is the probability of having \tau_n=t. * indicates the number of sites n (or in the case of the FBM of index H=0.75, the number of intervals) visited (20, 40, 80).

- TSAW4i_n*: left column is time t, right column is the probability of having \tau_n=t. * indicates the number of sites visited (200, 400, 800) by the True Self Avoiding Walk.
