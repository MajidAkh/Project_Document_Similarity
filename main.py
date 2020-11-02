import sys
import numpy as np
import string
import random




#List of each doc from the file.
Docs = []

#Parameters variables k = size of shingle contents = txt file
k = int(sys.argv[2])
with open(sys.argv[1], "r") as f:
    for line in f:
        Docs.append(line.strip().lower())   
        
f.close()


#Here : Documents to Shingles
m = []
shingle_id = {}
id_shingle = []


def createShingle(Liste):
    ids = 0

    #Implementation of a dict the key is the doc id and value is the text.
    
    #loop all the docs
    for d in Liste:
        #removing whitespace
        d_new = ''.join(c for c in d if c.isalnum())
        char_shing = [d_new[i:i+k] for i in range(len(d_new)-k+1)]
        sid = set()
        for sh in char_shing:
            if sh not in shingle_id:
                shingle_id[sh] = ids
                id_shingle.append(sh)
                ids = ids + 1
            sid.add(shingle_id[sh])
        m.append(sid)   
    print(shingle_id)


createShingle(Docs)

# Jaccard_similarity

def jaccard_similarity(doc1, doc2):
    if len(doc1) == 0 or len(doc2) == 0:
        return 0.0
    else:
        inter = doc1.intersection(doc2)
        union = doc1.union(doc2)
        return float(len(inter))/float(len(union))
    
    
def min_hash(doc, perm):
    for d in perm:
        if d in doc: return d
n = 100

mh_0 = []
mh_1 = []

perm = list(range(len(id_shingle)))

for _ in range(n):
    random.shuffle(perm)
    mh_0.append(min_hash(m[0], perm))
    mh_1.append(min_hash(m[1], perm))
    
    
c = 0
for i in range(len(mh_0)):
    if mh_0[i]==mh_1[i]:
        c +=1
        
print(float(c)/float(n))


def lsh(signature, b, r):
    
    lsh ={}
    for counter, value in enumerate(signature):
        for position, signa in enumerate(value):
            if (position + r <=len(value)) and (position % r) == 0:
                
                basket = ""
                basket = str(pos) + ','
            
            



    
    
    
    
    
