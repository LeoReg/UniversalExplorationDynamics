from numba import jit
import numpy as np



@jit(nopython=True)
def Nt1t2(t1,t2,alpha):
    N2=np.cumsum((2*np.random.randint(0,2,t2)-1)*np.random.zipf(1+alpha,size=t2))
    return(len(np.unique(N2[:t1])),len(np.unique(N2)))


@jit(nopython=True)
def Nt1t2t3(t1,t2,t3,alpha):
    N2=np.cumsum((2*np.random.randint(0,2,t3)-1)*np.random.zipf(1+alpha,size=t3))
    return(len(np.unique(N2[:t1])),len(np.unique(N2[:t2])),len(np.unique(N2)))

@jit(nopython=True)
def Nt1t2t3t4(t1,t2,t3,t4,alpha):
    N2=np.cumsum((2*np.random.randint(0,2,t4)-1)*np.random.zipf(1+alpha,size=t4))
    return(len(np.unique(N2[:t1])),len(np.unique(N2[:t2])),len(np.unique(N2[:t3])),len(np.unique(N2)))


#s=str(np.random.randint(10**4))
#Z=np.logspace(0,2,15)
#N=[]
#for t1 in [10,100,1000]:
#    for t2 in np.int64(Z*t1):
#      N.append([Nt1t2(t1,t2,alpha) for k in range(10000)])
#    np.save('Cov2times_13/'+s,N)



#s=str(np.random.randint(10**4))
#Z=np.logspace(0,2,15)
#alpha=1.7
#N=[]
#for t1 in [10,100]:
#    for t2 in [2*t1,4*t1]:
#      for t3 in [4*t2]:
#        for t4 in np.int64(t3*Z):
#          N.append([Nt1t2t3t4(t1,t2,t3,t4,alpha) for k in range(10000)])
#          np.save('Cov4times_17/'+s,N)

s=str(np.random.randint(10**4))
alpha=1.3
Z=np.logspace(0,2,15)
N=[]
for t1 in [10,100]:
    for t2 in [2*t1,4*t1]:
        for t3 in np.int64(t2*Z):
          N.append([Nt1t2t3(t1,t2,t3,alpha) for k in range(400000)])
          np.save('Cov3times_13/'+s,N)

