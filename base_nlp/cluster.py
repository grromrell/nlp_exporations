import math
import numpy as np
import scipy.sparse
 
class DBSCAN(object):
 
def __init__(self, term_doc_matrix, epsilon, minpts):
    self.matrix = term_doc_matrix
    self.eps = epsilon
    self.minpts = minpts
    self.distance_matrix = None
    self.cluster_num = 0
    self.labels = np.zeros(term_doc_matrix.shape[0])

def compute_distance_matrix(self):
    if not scipy.sparse.issparse(self.matrix):
        raise ValueError('Input matrix is not a scipy sparse matrix')
    if ((self.matrix).shape[0] * (self.matrix).shape[1]) > 2500000000:
        distance_matrix = None
        for i in range(0, (self.matrix).shape[0], 50000):
            chunk = self.matrx[i:i+n]
            transpose = (chunk.T).tocsc()
            distance_chunk = chunk * transpose
            if not distance_matrix:
                distance_matrix = distance_chunk
            distance_matrix = scipy.sparse.vstack([distance_matrix, chunk])
    else:
        transpose = ((self.matrix).T).tocsc()
        distance_matrix = self.matrix * transpose
    self.distance_matrix = distance_matrix

def scan(self):
    self.compute_distance_matrix()
    unvisited = range((self.matrix).shape[0])
    while unvisited:
        doc = unvisited[0]
        row = self.distance_matrix[doc].toarray()
        neighbors = [index for index in range(len(row)) if row[index] >=
                     self.eps]
        if len(neighbors) < self.minpts:
            unvisited.remove(doc)
        else:
            self.cluster_num += 1
            self.labels[doc] = self.cluster_num
            unvisited.remove(doc)

            for i in neighbors:
                if i in unvisited:
                    unvisited.remove(i)
                self.labels[i] = self.cluster_num
                subrow = self.distance_matrix[i].toarray()
                sub_neighbors = [index for index in range(len(row))
                                 if row[index] >= self.eps]
                if len(sub_neighbors) >= self.minpts:
                    neighbors.append(sub_neighbors)
                else:
                    pass
            else:
                pass
