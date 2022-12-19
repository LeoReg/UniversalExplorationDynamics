from numba import jit
import numpy as np

@jit(nopython=True)
def NStar(x):
    tau=1
    t=0
    c=(0,0)
    pos=set()
    pos.add(c)
    U=np.random.randint(0,4,2*x)
    index=0
    while tau<x:
      t+=1  
      u=U[index]
      index+=1
      if index==2*x:
          index=0
          U=np.random.randint(0,4,2*x)
      if u<2:
        c=(c[0]+2*u-1,c[1])
      else:
        c=(c[0],c[1]+2*(u-2)-1)
      tau+=1
      if not (c in pos):
            pos.add(c[:])
            tau=1
    return len(pos),t

@jit(nopython=True)
def RStar(x):
    tau=1
    t=0
    c=(0,0)
    pos=set()
    pos.add(c)
    U=np.random.randint(0,4,2*x)
    index=0
    while tau<x:
      t+=1
      u=U[index]
      index+=1
      if index==2*x:
          index=0
          U=np.random.randint(0,4,2*x)
      if u<2:
        c=(c[0]+2*u-1,c[1])
      else:
        c=(c[0],c[1]+2*(u-2)-1)
      tau+=1
      if not (c in pos):
            pos.add(c[:])
            tau=1
    return np.sqrt(c[0]**2+c[1]**2)


L=[]
r=np.random.randint(10**4)
lS=np.int64(2*np.logspace(2,5,30))
for S in lS:
  L.append([RStar(S) for k in range(50)])
  np.save('RStarv/2d/'+str(r),L)
