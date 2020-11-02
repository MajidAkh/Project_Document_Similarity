import sys
import random
import numpy as np
import itertools


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
    size = len(signature[0])
    #bucket qui prends associes à chaque bande tous les doc ayant la band
    dict_of_bucket= {}
    #pair de tous les candidats potentiellement similaire
    candidat = {}
    # List des bandes
    sub_list = []
    
    for band in range(b):
        dict_of_bucket= {}
        
        for i  in range(size):
            sub_list = []
            for el in range(band*r,band*r+r):
                
             
        
                
                sub_list.append(signature[el][i])
            strband = convert_list_to_string(sub_list)
            if strband in dict_of_bucket:
                dict_of_bucket[strband].append(i)
            else:
                dict_of_bucket[strband] = [i]
        for doc_sim in dict_of_bucket:
            if len(dict_of_bucket[doc_sim]) > 1:
                for pair in itertools.combinations(dict_of_bucket[doc_sim],2):
                    if pair in candidat:
                        candidat[pair] += 1
                    else:
                        candidat[pair] = 0
                        
                    
    
    
    return candidat




#find candidate


def pair_similarity(candidat,t,m):

    for i in candidat.keys():
                if jaccard_similarity(m[i[0]], m[i[1]]) >= t:
                    valeur = jaccard_similarity(m[i[0]], m[i[1]])
                    print(i[0],i[1],valeur)
                    #print('\n')


        



def true_jacard_sim(m, treshold):
 
    true_result = dict()
    number_of_true_resulat = 0
    for i in range (0, len(m)):
        for j in range(i+1, len(m)):
            
            jacard_simi = jaccard_similarity(m[i],m[j])
            true_result[(i,j)] = jacard_simi
            if jacard_simi >= treshold:
                number_of_true_resulat += 1
    return true_result, number_of_true_resulat
 
def truthness(liste, true_result, signature,t):
    True_pos = 0
    True_neg = 0
    Fals_pos = 0
    Fals_neg = 0

    
    for i in range(0, len(liste)):
        for j in range(i+ 1, len(liste)):
            signature_similarity = min_hash_similarity(signature,i, j)
            if true_result[(i,j)] >= t:
                if signature_similarity >= t:
                    True_pos += 1
                else:
                    Fals_neg += 1
            else:
                
                if signature_similarity <= t:
                    Fals_pos += 1
                else:
                    True_neg += 1
    return True_pos, True_neg, Fals_pos, Fals_neg
    
    
    
    
     
        
    
                
def main():
    
    docs,k,t = get_outils()
    n = 100
    b=20
    r=5
    
    m, id_shingle = createShingle(docs,k)
    
    S = gen_signature_matrix(m, n, id_shingle)
    candidats = lsh(S,b,r)
    result = pair_similarity(candidats, t,m)
    true_res, number_of_true_res = true_jacard_sim(m, t)
    print(truthness(m, true_res, S, t))
    print(result)



if __name__ == '__main__':
	main()
    
    
    
    
