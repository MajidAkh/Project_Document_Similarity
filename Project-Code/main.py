import sys
import random
import numpy as np
import itertools
import time
import matplotlib.pyplot as plt
import psutil 

#List of each doc from the file.
def get_outils():
    Docs = []

    #Parameters variables k = size of shingle contents = txt file
    k = int(sys.argv[2])
    t = float(sys.argv[3])
    with open(sys.argv[1], "r") as f:
        for line in f:
            Docs.append(line.strip().lower())   
        
        f.close()
    return Docs,k,t


#Here : Documents to Shingles



def createShingle(Liste,k):
    ids = 0
    m = []
    shingle_id = {}
    id_shingle = []


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
    return m, id_shingle




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
    
    
def gen_signature_matrix(m, n, id_shingle):
  perm = list(range(len(id_shingle)))
  S = []
  for i in range(n):
    S.append([])
    random.shuffle(perm)
    for doc in m:
      mh = min_hash(doc,perm)
      S[i].append(mh)
  return S

def min_hash_similarity(S,i1,i2):
  n = len(S)
  c = 0
  for i in range(n):
    if S[i][i1]==S[i][i2]: c += 1
  return float(c)/float(n)


def convert_list_to_string(list):
    
    list_to_string = '-'.join(str(s) for s in list)
    
    return list_to_string
      



def lsh(signature, b, r):
    S = np.array(signature)
    #bucket qui prends associes à chaque bande tous les doc ayant la band
    dict_of_bucket= {}
    #pair de tous les candidats potentiellement similaire
    candidat = {}
    # List des bandes
    sub_list = []
    
    for band in range(b):
        dict_of_bucket = {}
        
        for j  in range(len(S[0])):

            sub_list.append(list(S[band*r:band *r + r,j]))
            
            strband = convert_list_to_string(sub_list)
            
            sub_list = []
            #print(strband)
            if strband in dict_of_bucket:
                dict_of_bucket[strband].append(j)
            else:
                dict_of_bucket[strband] = [j]
        
        for doc_sim in dict_of_bucket:
            
        #print(doc_sim)
            
        
            
            if len(dict_of_bucket[doc_sim]) > 1:
              
           
                for pair in itertools.combinations(dict_of_bucket[doc_sim],2):
                    if pair in candidat:
                        candidat[pair] += 1
                    else:
                            
                            
                        candidat[pair] = 1
                        
                    
    
    #print(candidat)
    return candidat




#find candidate
def pair_similarity(candidat,t,m):
    
    count = 0
    for i in candidat.keys():
                if jaccard_similarity(m[i[0]], m[i[1]]) >= t:
                    valeur = jaccard_similarity(m[i[0]], m[i[1]])
                    print(i[0],i[1],valeur)
                    count = count + 1
                    #print('\n')
    return count
             
def main():
   
    time_final = 0
    time_line = []
    memoire_global = []
    faux_pos = []
    faux_positive = 0
   
    bands = [5,10,15,20,25,30,40,50]
    for b in bands:
        for i in range(8):
            n = 100
            r = int(n/b)
            starting_time = time.time() 
            docs,k,t = get_outils() 
            m, id_shingle = createShingle(docs,k)
            S = gen_signature_matrix(m, n, id_shingle)
            candidats = lsh(S,b,r)
            
            nbr_candidat = len(candidats)
            count = pair_similarity(candidats, t,m)
            
            
            time_final = time_final + time.time() - starting_time
            if i == 1:

                m = psutil.virtual_memory()
   
                memoire_global.append(m[3] / 10**6) 
            faux_positive = faux_positive + nbr_candidat - count
        
        time_line.append(time_final/8)
        time_final = 0
        
        faux_pos.append(faux_positive/8)
        faux_positive = 0
            



    fig = plt.figure()
    plt.title("time execution")
    plt.xlabel('bands')
    plt.ylabel('Time')
    ax = fig.add_subplot(111)
    ax.scatter(bands, time_line)
    plt.show()
    
    fig = plt.figure()
    plt.title("faux positif")
    plt.xlabel('bands')
    plt.ylabel('faux positif')
    ax = fig.add_subplot(111)
    ax.scatter(bands, faux_pos)
    plt.show()


    fig = plt.figure()
    plt.title("memory used")
    plt.xlabel('bands')
    plt.ylabel('memory used')
    ax = fig.add_subplot(111)
    ax.scatter(bands, memoire_global)
    plt.show()
   
if __name__ == '__main__':
	main()
    
    
    
    
