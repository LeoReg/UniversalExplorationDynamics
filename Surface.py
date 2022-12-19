import numpy as np
from collections import Counter
from numba import jit

@jit(nopython=True)
def surface(S0): #Make a walk of size n,of dimension d and having steps neighbours
    neighbours=[np.array([0,1]),np.array([0,-1]),np.array([1,0]),np.array([-1,0])]
    pos=set()
    pos.add((0,0))
    c0=np.array([0,0])
    Ind=np.random.randint(0,4,10**4)
    index=0
    S=4
    tau=0
    Tr=False
    while S<S0+2:
      i=Ind[index]
      index+=1
      if index==len(Ind):
        index=0
        Ind=np.random.randint(0,4,10**4)
      c0=c0+neighbours[i]
      if (not (c0[0],c0[1]) in pos):
        S+=4 
        for k in range(4):
          c=c0+neighbours[k]
          if (c[0],c[1]) in pos:
             S-=2
        pos.add((c0[0],c0[1])) 
      if S==S0 or Tr:
            tau+=1
            Tr=True
    return(tau)

Dlis=np.array([50,100,200])
for d in Dlis:
    Lis=[surface(d) for k in range(4000000)]
    D=Counter(Lis)
    M=max(D.keys())
    np.save('Surface/'+str(d)+'/'+str(np.random.randint(10**5)),[D[k] for k in range(1,M+1)])


