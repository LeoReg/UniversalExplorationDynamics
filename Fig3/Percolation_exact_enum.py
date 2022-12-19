import numpy as np
from collections import defaultdict
from scipy import sparse


def trans_matrice(L,D,vois):
    I,J,V=[],[],[]
    for i in range(len(L)):
        for l in vois[L[i]]:
            j=D[l]
            if j>=0:
                I.append(i)
                J.append(j)
                V.append(1./len(vois[L[i]]))
    I=np.array(I)
    J=np.array(J)
    V=np.array(V)
    return(sparse.csc_matrix((V,(J,I)),shape=(len(L),len(L))))
import sys

n=int(sys.argv[1])
K=int(sys.argv[2])

vois=defaultdict(list)
filename = 'percLeo1000/cl_sel1000/perc_voisins_L_1000_'+str(K)+'.dat'
Tm = np.loadtxt(filename)[:]
print(Tm)
for k in range(len(Tm)):
    Tm[k]=[int(Tm[k][i]) for i in range(2)]
for i in range(len(Tm)):
  vois[Tm[i][0]].append(Tm[i][1])




t=100000
L=np.zeros(t)
Err=np.zeros(t)

for r in range(1,10**4+1):
    p_k=[]
    pos_list=[]
    filename = 'percLeo1000/perc/data_n'+str(n)+'_'+str(K)+'/sites'+str(r)+'.dat'
    Tm = np.loadtxt(filename)[:]
    for a in Tm:
        pos_list.append(a)
    filename = 'percLeo1000/perc/data_n'+str(n)+'_'+str(K)+'/end'+str(r)+'.dat'
    c1 = np.loadtxt(filename)
    i0=pos_list.index(c1)
    def moins_un():
       return(-1)
    dic=defaultdict(moins_un)
    for i in range(n):
       dic[pos_list[i]]=i
    M=trans_matrice(pos_list,dic,vois)
    P=np.zeros(n)
    P[i0]=1
    p_k=[1]
    S=0
    for k in range(t):
        P=M.dot(P)
        p_k.append(np.sum(P))
    p_k=np.array(p_k)
    p_k=p_k[:-1]-p_k[1:]
    L+=p_k
    Err+=p_k**2
    if r%10**2==0:
      np.save('percolation/'+str(n)+'/Probabilities_n'+str(n)+', '+str(K),[L,Err])

