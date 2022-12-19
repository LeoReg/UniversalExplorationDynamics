from collections import Counter,defaultdict
import numpy as np
import copy
        
def lattice_n(n,d,neighbours): #Make a walk of size n,of dimension d and having steps neighbours
    c0=0
    pos=set()
    pos.add(c0)
    m=1
    Moves=[]
    C=[]
    C.append(c0)
    while m<n:
      Moves_0=list(neighbours[np.random.randint(2*d,size=n-m)])
      c0=c0+np.cumsum(Moves_0,axis=0)
      C.extend(c0)  
      pos.update(c0)
      c0=c0[-1]
      m=len(pos)
      Moves.extend(Moves_0[:])
    D=Counter(C) #dictionnary recording the number of visits at each site
    M=len(Moves) #length of the random walk in order to visit the n sites
    E=n-1
    Pos=list(pos)
    for p in Pos:
          for vois in neighbours:
            if p+vois in pos:
              E-=1/2
    return(C,D,M,Moves,pos,int(E))

#A move of the MC MC 
def lattice_MC(n,d,C,D,M,Moves,pos,E,hist_ln_g,hist_E,ln_modif,neighbours): #when computing the energy, only the points at distance Neigh matter
      k=np.random.randint(M) #choose a position: between 1 and M-1, exchanges the moves i and i+1, k=M, we change completly the last move by drawing an other one
      if k<M-1: #in that case, only one position might change, the position of the site at step i+1. If the new position of the walk at step i+1 affects the number of different positions, one has to erase/produce new moves to keep the number of distinct visited sites to n
        c=C[k+1]
        c2=C[k+1]-Moves[k]+Moves[k+1]
        f=(c2 in pos)
        if (D[c]>1 and f) or (c2==c) : #First case: No change at all
            D[c]-=1
            D[c2]+=1
            Moves[k],Moves[k+1]=Moves[k+1],Moves[k]
            C[k+1]=c2  
            Mo,C0=[],[]
            K=0
            while D[C[-1]]>1: #changes so that the last visited site has been visited only once 
                D[C[-1]]-=1
                C0.append(C.pop())
                Mo.append(Moves.pop())
                K+=1
            if np.random.random()<(M/(M-K)): #erased moves: it corresponds to the probability to reach configuration 1 from 2 divided by the one from 2 to 1
                M-=K
            else:
                C0.reverse()
                C.extend(C0)
                Mo.reverse()
                Moves.extend(Mo)
                for c1 in C0[:-1]:
                    D[c1]+=1
                D[C0[-1]]=1
                D[c]+=1
                D[c2]-=1
                Moves[k],Moves[k+1]=Moves[k+1],Moves[k]
                C[k+1]=c
        elif D[c]==1 & (not f): #2nd case: you erase a site visited only once and replace it by a site you have never visited.
            pos.remove(c)
            links=0 #computation of the energy difference
            for m in neighbours:
                if c+m in pos:
                  links+=1
                if c2+m in pos:
                  links-=1
            pos.add(c2)
            delta_ln_g=hist_ln_g[-(E+links)]-hist_ln_g[-E]
            if np.random.random()<min(1,np.exp(-delta_ln_g)):
              E+=links
              D.pop(c)
              D[c2]=1
              Moves[k],Moves[k+1]=Moves[k+1],Moves[k]
              C[k+1]=c2
            else:
              pos.remove(c2)
              pos.add(c)
        elif D[c]==1 & f: #3rd case: you erase a site visited only once and replace it by a site you have already visited: you must add new moves.
            Moves[k],Moves[k+1]=Moves[k+1],Moves[k]
            links=0
            for m in neighbours:
              if c+m in pos:
                  links+=1
            Mo=[]
            C0=[C[-1]]
            pos.remove(c)
            pos.add(c2)
            D[C[-1]]-=1 
            D.pop(c)
            while C0[-1] in pos: 
                Mo.append(neighbours[np.random.randint(2*d)])
                C0.append(C0[-1]+Mo[-1])
            for m in neighbours:
                if C0[-1]+m in pos:
                  links-=1
            delta_ln_g=hist_ln_g[-(E+links)]-hist_ln_g[-E]
            if np.random.random()<min(1,(M/(M+len(Mo)))*np.exp(-delta_ln_g)):
              E+=links
              for c1 in C0[:-1]:
                D[c1]+=1
              D[C0[-1]]=1
              D[c2]+=1
              pos.update(C0)
              M+=len(Mo)
              Moves.extend(Mo)
              C[k+1]=c2
              C.extend(C0[1:])
            else:
              D[C0[0]]+=1
              pos.add(c)
              Moves[k],Moves[k+1]=Moves[k+1],Moves[k]
              D[c]=1 
        else: #fourth case: you discover a new site without changing the other visited sites. You have to remove moves until you have only seen n distincts sites
            links=0
            D[c]-=1
            D[c2]=1
            for m in neighbours:
                if C[-1]+m in pos:
                  links+=1
            pos.remove(C[-1])
            for m in neighbours:
                if c2+m in pos:
                  links-=1
            Moves[k],Moves[k+1]=Moves[k+1],Moves[k]
            C[k+1]=c2
            K=1
            C0=C[-1]
            D.pop(C0)
            c1=C0-Moves[-K]
            C0=[C0]
            while D[c1]>1: 
               K+=1
               D[c1]-=1
               C0.append(c1)
               c1=c1-Moves[-K] #You have to delete moves until you see the last site only once
            delta_ln_g=hist_ln_g[-(E+links)]-hist_ln_g[-E]
            if np.random.random()<min(1,(M/(M-K))*np.exp(-delta_ln_g)): #
                del Moves[-K:]
                del C[-K:]
                M-=K  
                pos.add(c2)
                E+=links
            else:
                Moves[k],Moves[k+1]=Moves[k+1],Moves[k]
                C[k+1]=c
                for c0 in C0[1:]:
                    D[c0]+=1
                D[C0[0]]=1
                D[c]+=1
                D.pop(c2)
                pos.update(C0)
                pos.add(c)
      else:  #Case in which you change the last move. What might happen: you fall on a sites you have already visited. Must add new moves.
        links=0
        for m in neighbours:
                if C[-1]+m in pos:
                  links+=1
        C0=[C[-1]]
        Mo=[neighbours[np.random.randint(2*d)]]
        C0[0]=C0[0]+Mo[0]-Moves[-1]
        pos.remove(C[-1])
        if C0[-1] in pos:
            Mo.append(Moves[-1])
            C0.append(C0[-1]+Mo[-1])
        while C0[-1] in pos:
                Mo.append(neighbours[np.random.randint(2*d)])
                C0.append(C0[-1]+Mo[-1])
        for m in neighbours:
                if C0[-1]+m in pos:
                  links-=1
        K=len(Mo)
        delta_ln_g=hist_ln_g[-(E+links)]-hist_ln_g[-E]
        if np.random.random()<min(1,M/(M+(K-1))*np.exp(-delta_ln_g)): 
                M+=K-1
                Moves.pop()
                Moves+=Mo
                D.pop(C[-1])
                C.pop()
                C.extend(C0)
                pos.update(C0)
                for c0 in C0[:-1]:
                  D[c0]+=1  
                D[C0[-1]]=1
                E+=links
        else:
            pos.add(C[-1])
      if np.isnan(hist_ln_g[-E]):
        hist_ln_g[-E]=ln_modif
      else:
        hist_ln_g[-E]+=ln_modif
      if np.isnan(hist_E[-E]):
        hist_E[-E]=1
      else:
        hist_E[-E]+=1
      return(M,E) 

import sys
n=int(sys.argv[1])
d=2
neighbours=np.array([0 for i in range(2*d)])
for k in range(0,d):
      neighbours[2*k]=n**k
      neighbours[2*k+1]=-n**k
ln_modif=1
C,D,M,Moves,pos,E=lattice_n(n,d,neighbours)
hist_E= [np.nan]*(d*n-n-d*int(n**((d-1)/d))+2)
hist_ln_g=[np.nan]*(d*n-n-d*int(n**((d-1)/d))+2)
hist_E[-E]=1
hist_ln_g[-E]=ln_modif


for jrun in np.arange(21):
    flag_histo=1
    i=1
    Emax=-E
    imin=-E
    while ((flag_histo) or (i<500*n)) and i<10**9:
        M,E=lattice_MC(n,d,C,D,M,Moves,pos,E,hist_ln_g,hist_E,ln_modif,neighbours)
        if i==1:
            imin=-E
        i+=1
        Emax=max(-E,Emax)
        if (i%n == 0):
           thres=0.8*i/(Emax+1)
           imin=np.nanargmin(hist_E)
           if (hist_E[imin]>thres and i>500*n):
               flag_histo=0
    ln_modif/=2.
    hist_E=np.array([np.nan]*(d*n-n-d*int(n**((d-1)/d))+2))
    hist_ln_g=hist_ln_g-np.nanmin(hist_ln_g)
    for i in range(len(hist_ln_g)):
        if not np.isnan(hist_ln_g[i]):
            hist_E[i]=0
    np.save('ln_density/'+str(n)+'/Complete',hist_ln_g)
