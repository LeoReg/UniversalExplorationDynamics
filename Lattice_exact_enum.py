from collections import defaultdict
import numpy as np
from scipy import sparse
from numba import jit

def trans_matrice(L,D,neighbours):
    d=len(neighbours)/2
    I,J,V=[],[],[]
    for i in range(len(L)):
        for l in neighbours:
            j=D[L[i]+l]
            if j>=0:
                I.append(i)
                J.append(j)
                V.append(1/2./d)
    I=np.array(I)
    J=np.array(J)
    V=np.array(V)
    return(sparse.csc_matrix((V,(I,J)),shape=(len(L),len(L))))

@jit(nopython=True)
def lattice_n(n,d,neighbours): #Make a walk of size n,of dimension d and having steps neighbours
    c0=0
    pos=set()
    pos.add(0)
    m=1
    while m<n:
      c0=c0+np.cumsum(np.random.choice(neighbours,size=n-m,replace=True))
      pos.update(c0)
      c0=c0[-1]
      m=len(pos)
    return(pos,c0)

def moins_un():
   return(-1)

def exact_enum_pow(d,t0,t1,n):
    neighbours=np.zeros(2*d, dtype='i')
    for k in range(0,d):
      neighbours[2*k]=n**k
      neighbours[2*k+1]=-n**k
    p_k=[]
    pos,c0=lattice_n(n,d,neighbours)
    pos_list=list(pos)
    i0=pos_list.index(c0)
    D=defaultdict(moins_un)
    for i in range(n):
       D[pos_list[i]]=i
    M=trans_matrice(pos_list,D,neighbours)
    M0=M.copy()
    P=np.zeros(n)
    P[i0]=1
    p_k=[]
    S=0
    for k in range(t1):
        a=M.dot(P)
        p0=-np.log(np.sum(a))-S
        p1=-np.log(np.sum(M0.dot(a)))-S
        m=M.max()
        M=np.dot(M,M)/m**2
        S=2*S+2*np.log(m)
        p_k.append(p0-np.log(1-np.exp(p0-p1)))
    p_k_2=[0]
    S=0
    for k in range(t0):
        P=M0.dot(P)
        m=max(P)
        P=P/m
        S+=np.log(m)
        p_k_2.append(-np.log(np.sum(P))-S)
    p_k_2=np.exp(-np.array(p_k_2))
    p_k_2=p_k_2[:-1]-p_k_2[1:]
    #p_k_2=p_k_2[:-1]-np.log(1-np.exp(p_k_2[:-1]-p_k_2[1:]))
    return(p_k_2,p_k)

t0=10**5
t1=0
for s in range(10**3):
  for d in range(2,3):
    for n in [2000,5000]:
      Ls,Ls2=np.zeros(t0),np.zeros(t0)
      Count=0 
      for m in range(10**2):
        L=np.array(list(exact_enum_pow(d,t0,t1,n)[0]))  
        Ls+=L
        Ls2+=L**2
        Count+=1
      np.save('Lattice/'+str(n)+'/'+str(np.random.randint(10**8)),[Ls,Ls2,Count])
