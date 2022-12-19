import numpy as np
from numba import jit
from collections import Counter

@jit(nopython=True)
def taun(n,beta,kap):
  L=np.zeros(2*n+2)
  m,M=0,0
  c=0
  tau=0
  while M-m+1<n:
     if M-m+1==n-1:
         tau+=1
     u=np.random.random()
     p1,p2=L[n+c-1]**kap,L[n+c+1]**kap
     p1=np.exp(-beta*p1)
     p2=np.exp(-beta*p2)
     p1=p1/(p1+p2)
     if u<p1:
         c-=1
         L[n+c]+=1
         m=min(c,m)
     else:
         c+=1
         L[n+c]+=1
         M=max(c,M)
  return tau

beta=1
kap=0.5
for n in [200,400,800]:
    L=[taun(n,beta,kap) for k in range(10000)]
    D=Counter(L)
    np.save('TSARW_kap05/'+str(n)+'/'+str(np.random.randint(10**4)),[D[k] for k in range(1,max(L)+1)])

