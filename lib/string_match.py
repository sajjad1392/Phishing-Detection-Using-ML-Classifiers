import re
from .brands import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import pandas as pd 
import numpy as np
from scipy.sparse import csr_matrix
import sparse_dot_topn.sparse_dot_topn as ct  #Cosine Similarity
import time

def ngrams(string, n=3):
    string = (re.sub(r'[,-./]|\sBD',r'', string)).upper()
    ngrams = zip(*[string[i:] for i in range(n)])
    return [''.join(ngram) for ngram in ngrams]
    
def ngrams2(string): 
    string = string.lower()
    chars_to_remove = ["~", "`", "!", "@", "#", "$", "%", "^", "*", "(", ")", "_", "|", "[", "]", "{", "}", "'", ";", ":", ">", "<", "="]
    rx = '[' + re.escape(''.join(chars_to_remove)) + ']'
    string = re.sub(rx, '', string) # remove the list of chars defined above
    string = string.replace('&', ' ')
    string = string.replace('.', ' ')
    string = string.replace(',', ' ').replace('-', ' ')
    string = re.sub(' +',' ',string).strip() # combine whitespace
    string = ' ' + string + ' ' # pad
    return string

def awesome_cossim_top(A, B, ntop, lower_bound=0):
    # force A and B as a CSR matrix.
    # If they have already been CSR, there is no overhead
    A = A.tocsr()
    B = B.tocsr()
    M, _ = A.shape
    _, N = B.shape
 
    idx_dtype = np.int32
 
    nnz_max = M*ntop
 
    indptr = np.zeros(M+1, dtype=idx_dtype)
    indices = np.zeros(nnz_max, dtype=idx_dtype)
    data = np.zeros(nnz_max, dtype=A.dtype)

    ct.sparse_dot_topn(
        M, N, np.asarray(A.indptr, dtype=idx_dtype),
        np.asarray(A.indices, dtype=idx_dtype),
        A.data,
        np.asarray(B.indptr, dtype=idx_dtype),
        np.asarray(B.indices, dtype=idx_dtype),
        B.data,
        ntop,
        lower_bound,
        indptr, indices, data)

    return csr_matrix((data,indices,indptr),shape=(M,N))

    
def get_matches_df(sparse_matrix, A, B, top=100):
    non_zeros = sparse_matrix.nonzero()
    
    sparserows = non_zeros[0]
    sparsecols = non_zeros[1]
    
    if top:
        nr_matches = top
    else:
        nr_matches = sparsecols.size
    
    left_side = np.empty([nr_matches], dtype=object)
    right_side = np.empty([nr_matches], dtype=object)
    similairity = np.zeros(nr_matches)
    
    for index in range(0, nr_matches):
        left_side[index] = A[sparserows[index]]
        right_side[index] = B[sparsecols[index]]
        similairity[index] = sparse_matrix.data[index]
    
    return pd.DataFrame({'left_side': left_side,
                          'right_side': right_side,
                           'similairity': similairity})
   
   
def tfidf_match(list1, list2):
    """For each item in list1, find the match in list2"""
    vectorizer = TfidfVectorizer(analyzer=ngrams, min_df=1, max_df=1.0)
    tfidf = vectorizer.fit_transform(list2)
    nbrs = NearestNeighbors(n_neighbors=1, n_jobs=-1).fit(tfidf)
    distances, indices = nbrs.kneighbors(vectorizer.transform(list1))
    
    matches = [(round(distances[i][0], 2), list1[i], list2[j[0]]) 
               for i, j in enumerate(indices)]
    """matches = pd.DataFrame(matches, 
                           columns=['score', 'original', 'matched'])"""
    return matches[0][0]*100
    

    
def tfidf_match5(list1, list2):
    """For each item in list1, find the match in list2"""
    vectorizer = TfidfVectorizer(analyzer=ngrams, min_df=1, max_df=1.0)
    tfidf = vectorizer.fit_transform(list2)
    nbrs = NearestNeighbors(n_neighbors=1, metric='cosine').fit(tfidf)
    distances, indices = nbrs.kneighbors(vectorizer.transform(list1))
    
    matches = [(round(distances[i][0], 2), list1[i], list2[j[0]]) 
               for i, j in enumerate(indices)]
    """matches = pd.DataFrame(matches, 
                           columns=['score', 'original', 'matched'])"""
    return matches[0][0]*100
    
    