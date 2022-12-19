import numpy as np
from scipy import special
from numba import jit
from numba.typed import List

@jit(nopython=True)  #Draw the set of n visited sites
def levy_n(n,alpha):
    c0=0
    pos=set()
    pos.add(c0)
    lpos=List([c0])
    m=1
    while m<n:
        c0=c0+np.cumsum((2*np.random.randint(0,2,n-m)-1)*np.random.zipf(alpha+1,n-m))
        for c in c0:
            if not (c in pos):
              pos.add(c)
              lpos.append(c)
              m+=1
        c0=c0[-1]
    return(lpos)

@jit(nopython=True)
def trans_matrice(L,alpha,n,zet): #Build the adjacency matrix
    M=np.zeros((n,n))
    for i in range(n):
        for j in range(i+1,n):
            l=abs(L[i]-L[j])
            M[i,j]=1/2/zet/l**(alpha+1)
            M[j,i]=1/2/zet/l**(alpha+1)
    return(M)


@jit(nopython=True)
def exact_enum(alpha,t0,n,zet,Times): #Compute the distribution conditioned on the set of visited sites, exact enumeration
  L=List()
  for s in range(Times):
    lpos=levy_n(n,alpha)
    P=np.zeros(n)
    P[-1]=1.
    M=trans_matrice(lpos,alpha,n,zet)
    p_k=List()
    p_k.append(1.)
    for k in range(t0-1):
        P=M.dot(P)
        p_k.append(np.sum(P))
    L.append(p_k[:])
  return(L)




alpha=1 #Choose the value of alpha
t0=5000 #Time up to which the time distribution is computed
zet=special.zeta(alpha+1)
Times=100
for counter in range(10):
  for n in [800,1600,3200]:
      L=exact_enum(alpha,t0,n,zet,Times)
      L=np.array(L)
      Ls=np.sum(L,axis=0)
      Ls2=np.sum(L**2,axis=0)
      #np.save('Levy/'+str(n)+'/',[Ls,Ls2])

