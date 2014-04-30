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
    distance : ['in_memory', 'ooc', 'by_row', 'pre_computed'], default='in_memory'
        the way that the distance should be calculated. In memory should be used
        for matrices whose product can fit in memory. Ooc uses HDF5 for disk
        backed matrix multiplication for very large matrices. By_row will 
        perform the matrix multiplication as need and pre_computed is to be
        used when the distance_matrix has already been calculated.
    """
    def __init__(self, term_doc_matrix, epsilon, minpts, distance='in_memory'):
        self.matrix = term_doc_matrix
        self.eps = epsilon
        self.minpts = minpts
        self.distance = distance
        self.cluster_num = 0
        self.labels = np.zeros(term_doc_matrix.shape[0])
        self.unvisited = range(term_doc_matrix.shape[0])

    def _get_distances(self, row=0):
        if self.distance == 'in_memory':
            distance_matrix = distances.compute_similarity(self.matrix)
        if self.distance == 'ooc':
            distance_matrix = distances.compute_ooc(self.matrix)
        if self.distance == 'by_row':
            distance_matrix = distances.compute_row(self.matrix)
        if self.distance == 'pre_computed':
            distance_matrix = self.matrix
        else:
            raise ValueError('Invalid value for distance calculation')
        return distance_matrix

    def scan(self):
        distance_matrix = self._get_distances()
        while self.unvisited:
            doc = self.unvisited[0]
            if self.distance == 'pairwise':
                row = self._get_distances(doc)
            else:
                row = distance_matrix[doc]
            neighbors = [index for index in xrange(len(row)) if row[index] >=
                         self.eps]
            self.unvisited.remove(doc)
            if len(neighbors) >= self.minpts:
                self.cluster_num += 1
                self.labels[doc] = self.cluster_num
                self._neighbor_scan(neighbors)

    def _neighbor_scan(self, neighbors):
        for neighbor in neighbors:
            if neighbor not in self.unvisited:
                continue
            self.unvisited.remove(neighbor)
            self.labels[neighbor] = self.cluster_num
            if self.distance == 'pairwise':
                row = self._get_distances(neighbor)
            else:
                row = distance_matrix[neighbor]
            new_neighbors = [index for index in range(len(row))
                             if row[index] >= self.eps]
            if len(new_neighbors) >= self.minpts:
                neighbors.append(new_neighbors)
