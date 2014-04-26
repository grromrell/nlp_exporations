import numpy as np
import scipy.sparse
import distances

class DBSCAN(object):
    """
    Clusters documents together based on a term document matrix. Calling the
    scan methdo will store the results of the clustering in the .labels
    attribute. For more information see: http://bit.ly/1rtAMVx
    
    Parameters
    ---------
    term_doc_matrix : scipy.sparse or numpy array
        matrix that contains your term document matrix, typically output from
        bag_of_words.
    epsilon : float
        the threshold for which documents are considered similar. 1 will only
        match a document to itself, 0 will match all documents.
    minpts : integer
        minimum number of points considered to be similar before a cluster
        is defined.
    is_large : bool, default = False
        if the expected outcome of the term_document matrix is larger than
        can fit in memory set this value to true to allow for out of core
        multiplication. This method requires pytables for HDF5 usage.
    """
    def __init__(self, term_doc_matrix, epsilon, minpts, is_large=False):
        self.matrix = term_doc_matrix
        self.eps = epsilon
        self.minpts = minpts
        self.is_large = is_large
        self.cluster_num = 0
        self.labels = np.zeros(term_doc_matrix.shape[0])

    def scan(self):
        if self.is_large:
            distance_matrix = distances.compute_large(self.matrix)
        else:
            distance_matrix = distances.compute_similarity(self.matrix)
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
