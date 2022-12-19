from collections import defaultdict
import numpy as np
from scipy import sparse
from numba import jit
from numba.typed import List
import copy

def moins_un():
  return -1

def trans_matrice(L,D,neighbours,p):
    I,J,V=[],[],[]
    n=len(L)
    for i in range(n):
        for k in range(len(neighbours)):
            l=neighbours[k]
            j=D[(L[i][0]+l[0],L[i][1]+l[1])]
            if j>=0:
                I.append(i+k*n)
                J.append(j+k*n)
                V.append(p)
                for h in range(1,4):   
                  I.append(i+n*((k+h)%4))
                  J.append(j+n*((k+h)%4))
                  V.append((1-p)/3)
    I=np.array(I)
    J=np.array(J)
    V=np.array(V)
    return(sparse.csc_matrix((V,(I,J)),shape=(4*n,4*n)))


neighbours=np.array([np.array([1,0]),np.array([-1,0]),np.array([0,1]),np.array([0,-1])])

@jit(nopython=True)
def lattice_n(n,neighbours,p): #Make a walk of size n,of dimension d and having steps neighbours
    c0=(1,0)
    pos=set()
    pos.add((0,0))
    pos.add((1,0))
    m=2
    lpos=List([(0,0),(1,0)])
    direction=0
    while m<n:
      U=np.random.random(n-m)
      Index=np.arange(n-m)
      for k in range(n-m):
          u=U[k]
          if u<p:
             Index[k]=direction
          elif u<p+(1-p)/3:
             direction=(direction+1)%4
             Index[k]=direction
          elif u<p+2*(1-p)/3:
             direction=(direction+2)%4
             Index[k]=direction
          else:
             direction=(direction+3)%4  
             Index[k]=direction
          c0=(c0[0]+neighbours[Index[k]][0],c0[1]+neighbours[Index[k]][1])
          if not (c0 in pos):
            lpos.append(c0)
            pos.add(c0)
            m+=1
    return(lpos,direction)




def exact_enum_pow(t0,n,neighbours,p,Times):
  L=List()
  for s in range(Times):
    lpos,direction=lattice_n(n,neighbours,p)
    D=defaultdict(moins_un)
    for i in range(n):
       D[lpos[i]]=i
    P=np.zeros(4*n)
    P[n*(direction+1)-1]=1.
    M=trans_matrice(lpos,D,neighbours,p)
    p_k=List()
    p_k.append(1.)
    for k in range(t0-1):
        P=M.dot(P)
        p_k.append(np.sum(P))
    L.append(p_k[:])
  return(L)





t0=2000
Times=10000
p=0.3
for counter in range(20):
  for n in [400,800,1600]:
      L=exact_enum_pow(t0,n,neighbours,p,Times)
      L=np.array(L)
      Ls=np.sum(L,axis=0)
      Ls2=np.sum(L**2,axis=0)
      np.save('LatticePers2d_3/'+str(n)+'/'+str(np.random.randint(10**8)),[Ls,Ls2])

