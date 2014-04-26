import numpy as np
import scipy.sparse
import compute_distance, compute_large 
class DBSCAN(object):
 
    def __init__(self, term_doc_matrix, epsilon, minpts, is_large=False):
        self.matrix = term_doc_matrix
        self.eps = epsilon
        self.minpts = minpts
        self.is_large = is_large
        self.cluster_num = 0
        self.labels = np.zeros(term_doc_matrix.shape[0])

    def scan(self):
        if self.is_large:
            distance_matrix = compute_large(self.matrix)
        else:
            distance_matrix = compute_distance(self.matrix)
        unvisited = range((self.matrix).shape[0])
        while unvisited:
            doc = unvisited[0]
            row = distance_matrix[doc]
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
                    subrow = self.distance_matrix[i]
                    sub_neighbors = [index for index in range(len(row))
                                     if row[index] >= self.eps]
                    if len(sub_neighbors) >= self.minpts:
                        neighbors.append(sub_neighbors)
