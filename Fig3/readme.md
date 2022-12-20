**Python programs to generate data:**

- Levy_exact_enum.py: obtain the distribution of \tau_n by exact enumeration for 1d Lévy flights.

- Lattice_exact_enum.py: obtain the distribution of \tau_n by exact enumeration for nearest neighbour random walk on hypercubic lattice.

- MC_WangLandau.py: obtain the approximate energy density of the Monte Carlo Wang Landau algorithm for the hypercubic lattice.

- Avec_density.py: obtain the distribution of \tau_n from the Monte Carlo distribution via the bias/energy density obtained from the Wang-Landau algorithm.

- Persist_exact_enum_d2.py: obtain the distribution of \tau_n by exact enumeration for persistent random walk on 2d lattice.

- Persist_exact_enum_d3.py: obtain the distribution of \tau_n by exact enumeration for persistent random walk on 3d lattice.

- Percolation_exact_enum.py: obtain the distribution of \tau_n by exact enumeration for 2d critical percolation clusters from data in the file Percolation_data which contains sets of visited sites.

- Sierpinski_exact_enum.py: obtain the distribution of \tau_n by exact enumeration for Sierpinski gasket from data in the file Sierpinski_data which contains sets of visited sites.

**Mathematica program:**

- SierpDistinctSitesVisited.nb: mathematica program to generate the territory visited by a random walker on a Sierpinski gasket.

**C program:**

- GeneratePerc: this folder contains the C code necesary to generate the percolation clusters.

**Data**

- Percolation_data.zip: contains the 3 files about the visited territory of size n=100, 500 and 1000 which we use in the code Percolation_exact_enum.py.

- Sierpinski_data.zip: contains the 3 files about the visited territory of size n=100, 500 and 1000 which we use in the code Sierpinski_exact_enum.py.

- DataFig3.zip: contains the distributions associated to each figure presented in Fig.3 of the main text. The left column represents the time \tau, the right column is the value of F_n(\tau). The format is *3'number of subfigure'_n'number of distinct sites visited'. The exception are the files 'ln_density3i_n*' which are the densities associated to the energy histogram/MC bias we used to obtain the figure 3i.  
