from fbm import FBM
import numpy as np
from collections import Counter

def taun(n,H):
    f=FBM(int(10*n**(1/H)),H,length=int(10*n**(1/H)))
    V=f.fbm()
    T=f.times()
    M,m=np.zeros(len(V)),np.zeros(len(V))
    for k in range(1,len(V)):
        M[k]=max(M[k-1],V[k])
        m[k]=min(m[k-1],V[k])
    N=M-m+1
    N=np.int64(N)
    print(n)
    return(T[np.where(N>=n+1)[0][0]]-T[np.where(N>=n)[0][0]])

H=0.4
for n in [20,40,80]:
    L=[int(taun(n,H)) for k in range(1000)]
    np.save('FBM04/'+str(n)+'/'+str(np.random.randint(10**4)),L)

