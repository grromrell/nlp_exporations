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
    else:
        transpose = ((self.matrix).T).tocsc()
        distances = self.matrix * transpose
        self.distance_matrix = distances.toarray()

def scan(self, is_large=False):
    if not is_large:
        self.compute_distance_matrix()
    else:
        transpose = ((self.matrix).T).tocsc()
    unvisited = range((self.matrix).shape[0])
    while unvisited:
        doc = unvisited[0]
        if not is_large:
            row = self.distance_matrix[doc]
        else:
            row = ((self.matrix).getrow(doc) * transpose).toarray()[0]
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
                if not is_large:
                    subrow = self.distance_matrix[i]
                else:
                    subrow = ((self.matrix).getrow(i) * transpose).toarray()[0]
                sub_neighbors = [index for index in range(len(row))
                                 if row[index] >= self.eps]
                if len(sub_neighbors) >= self.minpts:
                    neighbors.append(sub_neighbors)
                else:
                    pass
            else:
                pass
