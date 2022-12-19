import numpy as np
import copy

# In[26]:


def replace(a,n1,n2): # replace value 1 by value 2 if exists
    b=np.copy(a)
    for i,j in enumerate(b):
        if j==n1:
            b[i]=n2
    return b

def replace_all(dic,n1,n2): # change all values in dic. Replace all n1 by n2
    pairs=list(dic.items())
    for key,item in pairs:
        if key==n1:
            dic.pop(key)
            dic.update({n2:replace(item,n1,n2)})
        else:
            dic.update({key:replace(item,n1,n2)})

def merge_nodes(i,j,dic1,dic2): # merge two nodes
    a=dic2.pop(j)
    dic1.update({i:np.concatenate((dic1.get(i),a))})
    dic1.update(dic2)
    for k,l in dic1.items():
        dic1.update({k:replace(l,j,i)})

def connect_nodes(i,j,dic):
    dic.update({i:np.concatenate((dic.get(i),[j]))})
    dic.update({j:np.concatenate((dic.get(j),[i]))})



def relabel(dic): # relabel vertices so that they range from 0 to n-1
    n=len(dic)
    changes=[]
    for i,k in zip(dic.keys(),range(n)):
        if i!=k:
            changes.append([i,k])
            #dic.update({k:replace(l,j,i)})
    for c in changes:
        c=np.array(c)
        replace_all(dic,c[0],c[1])
def adjacency_from_neighbor(dic): #make adjacency matrix from neighbor list
    adja=np.zeros((len(dic),len(dic)))
    for key,item in dic.items():
        for l in item:
            adja[key,l]=1
    return adja


# # Sierpinsky gasket

# In[27]:


def sierpinsky_make_neighbor(dic):
    n=len(dic)
    dic1={k+n:l+n for k,l in dic.items()}
    dic2={k+2*n:l+2*n for k,l in dic.items()}
    tochange=[]
    tochange1=[]
    tochange2=[]
    for v,v1,v2 in zip(dic.items(),dic1.items(),dic2.items()):
        if len(v[1])==2:
            tochange.append(v[0])
        if len(v1[1])==2:
            tochange1.append(v1[0])
        if len(v2[1])==2:
            tochange2.append(v2[0])
    merge_nodes(tochange[0],tochange1[0],dic,dic1)
    merge_nodes(tochange[1],tochange2[1],dic,dic2)
    merge_nodes(tochange1[2],tochange2[2],dic,dic)
    relabel(dic)

def gen_sierpinsky(n):
    dic={0: np.array([1, 2]),1: np.array([0, 2]),2: np.array([0, 1])}
    for k in range(n-1):
        sierpinsky_make_neighbor(dic)
    return dic

dic_sirpinsky11=gen_sierpinsky(11)

with open('Sierpinsky10.txt','w') as file:
    for value in dic_sirpinsky10.values():
        file.write(" ".join([str(item) for item in value]))
        file.write("\n")

def unmatched_sierpinsky_make_neighbor(dic):
    n=len(dic)
    dic1={k+n:l+n for k,l in dic.items()}
    dic2={k+2*n:l+2*n for k,l in dic.items()}
    tochange=[]
    tochange1=[]
    tochange2=[]
    for v,v1,v2 in zip(dic.items(),dic1.items(),dic2.items()):
        if len(v[1])==2:
            tochange.append(v[0])
        if len(v1[1])==2:
            tochange1.append(v1[0])
        if len(v2[1])==2:
            tochange2.append(v2[0])
    dic.update(dic1)
    dic.update(dic2)
    connect_nodes(tochange[0],tochange1[0],dic)
    connect_nodes(tochange[1],tochange2[1],dic)
    connect_nodes(tochange1[2],tochange2[2],dic)

def gen_unmatched_sierpinsky(n):
    dic={0: np.array([1, 2]),1: np.array([0, 2]),2: np.array([0, 1])}
    for k in range(n-1):
        unmatched_sierpinsky_make_neighbor(dic)
    return dic


# In[412]:

dic_unmatched_sirpinsky11=gen_unmatched_sierpinsky(11)

with open('Unmatched_Sierpinsky10.txt','w') as file:
    for value in dic_unmatched_sirpinsky10.values():
        file.write(" ".join([str(item) for item in value]))
        file.write("\n")

