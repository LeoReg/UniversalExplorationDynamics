import numpy as np
from scipy import sparse
from scipy.sparse import linalg 
import os
from collections import defaultdict

def trans_matrice(L,D,neighbours):
    I,J,V=[],[],[]
    for i in range(len(L)):
        for l in neighbours[i]:
            j=D[l]
            if j>=0:
                I.append(i)
                J.append(j)
                V.append(1./len(neighbours[i]))
    I=np.array(I)
    J=np.array(J)
    V=np.array(V)
    return(sparse.csc_matrix((V,(J,I)),shape=(len(L),len(L))))


for K in range(1,11):
  for n in [100,500,1000]:
    L=[]
    for r in range(1000*(K-1)+1,1000*K+1):
      p_k=[]
      pos_list=[(0.,0.)]
      neighbours=[[(0.,1.),(1.,0.)]]
      filename = 'Documents/Data/Sier_comparison/data_n'+str(n)+'/sites'+str(r)+'.dat'
      Tm = np.loadtxt(filename)[:]
      for s in Tm:
        pos_list.append(tuple(s))
      filename = 'Documents/Data/Sier_comparison/data_n'+str(n)+'/voisins'+str(r)+'.dat'
      Tm = np.loadtxt(filename)[:]
      for neig in Tm:
        neighbours.append([])
        for k in range(4):
            neighbours[-1].append(tuple(neig[2*k:2*k+2]))
      filename = 'Documents/Data/Sier_comparison/data_n'+str(n)+'/end'+str(r)+'.dat'
      Tm = np.loadtxt(filename)[:]
      c1=tuple(Tm)
      i0=pos_list.index(c1)
      def moins_un():
        return(-1)
      dic=defaultdict(moins_un)
      for i in range(n):
        dic[pos_list[i]]=i
      M=trans_matrice(pos_list,dic,neighbours)
      P=np.zeros(n)
      P[i0]=1
      for t in range(10**4):
         P=M.dot(P)
      L.append(np.log(np.sum(P))-np.log(np.sum(M.dot(P))))
      #if r%100==0:
        #np.save('Sier_comparison/'+str(n)+'/Carac_times, '+str(K),L)
