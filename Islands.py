from numba import jit
import numpy as np
from collections import Counter

@jit(nopython=True)
def Islands_d(d,alpha): #Make a walk of size n,of dimension d and having steps neighbours
    pos=set()
    pos.add(0)
    c0=0
    I=0
    Index=(2*np.random.randint(0,2,10**4)-1)*np.random.zipf(1+alpha,10**4)
    index=0
    tau=0
    Overcame=False
    while I<d+1:
      if I==d or Overcame:
        tau+=1
        Overcame=True
      i=Index[index]
      index+=1
      if index==len(Index):
        Index=(2*np.random.randint(0,2,10**4)-1)*np.random.zipf(1+alpha,10**4)
        index=0
      c0=c0+i
      if (not c0 in pos):
        A=True
        for test in [-1,1]:
            c=c0+test
            A=A and (c in pos)
        if A:
            I-=1
        A=True
        for test in [-1,1]:
            c=c0+test
            A=A and (not (c in pos))
        if A:
          I+=1
        pos.add(c0)
    return(tau)

alpha=1.2
D=np.array([50,100,200])
for d in D:
    Lis=[Islands_d(d,alpha) for k in range(2000000)]
    D=Counter(Lis)
    M=max(D.keys())
    np.save('Islands/Levy_1_2/'+str(d)+'/'+str(np.random.randint(10**5)),[D[k] for k in range(1,M+1)])



