from numba import jit
import numpy as np
from collections import Counter

def levy_n(n,alpha,Times):
  Rl=[]
  for i in range(Times):
    c0=0
    pos=set()
    pos.add(c0)
    m=len(pos)
    while m<n:
        c0=c0+np.cumsum((2*np.random.randint(0,2,n-m)-1)*np.random.zipf(alpha+1,n-m))
        pos.update(c0)
        c0=c0[-1]
        m=len(pos)
    L=list(pos)
    L=np.unique(L)
    R=1
    r=1
    for k in range(len(L)-1):
        if L[k+1]==L[k]+1:
            r+=1
            R=max(R,r)
        else:
            r=1
    Rl.append(R)
  return(Rl)

Count=10**1*2
alpha=1.5
N=[400,800,1600,3200,6400,12800,25600,51200,102400,204800,409600,819200,819200*2,819200*4,819200*8]
for n in N:
  L=levy_n(n,alpha,Count)
  Dic=Counter(L)
  np.save('densityC/'+str(n)+'/'+str(np.random.randint(10**5)),[Dic[k] for k in range(n+1)])
