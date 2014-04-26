import math
import numpy
import scipy.sparse

def compute_similarity(matrix):
    """
    compute cosine similarity for matrices that fit in memory

    Parameters
    ----------
    matrix: scipy.sparse or numpy.array
        term document matrix

    Returns
    -------
    distance_matrix: numpy.array
        cosine similarity matrix
    """
    if scipy.sparse.issparse(matrix):
        distance_matrix = (matrix * matrix.T).toarray()
    else:
        distance_matrix = matrix * matrix.T
    return distance_matrix

def compute_large(matrix):
    """
    compute cosine similarity out of core for large matrices. A large part of
    this method was writen by Francesc Alted. Source: Copyright (c) 2013,
    Francesc Alted BSD
    """
    if not scipy.sparse.issparse(matrix):
        raise ValueError('Input matrix is not a scipy.sparse matrix')
    try:
        import tables
    except:
        raise ValueError('Large distance calculation depends on pytables')
    f = tables.open_file('distance_matrix.h5', 'w')
    filters = tables.Filters(complevel=3, complib='blosc')
    distance_matrix = f.create_carray(f.root, 'distance_matrix', 
                                      tables.Atom.from_dtype(matrix.dtype),
                                      shape=(matrix.shape[0], matrix.shape[0]),
                                      filters = filters)

    l, m, n = matrix.shape[0], matrix.shape[1], matrix.shape[0]
    buff_size = (2**20)*32
    bl = math.sqrt(buff_size / distance_matrix.dtype.itemsize)
    bl = 2**int(math.log(bl, 2))
    for i in range(0, l, bl):
        for j in range(0, n, bl):
            for k in range(0, m, bl):
                subset1 = matrix[i:min(i+bl, l), k:min(k+bl, m)]
                subset2 = (matrix.T)[k:min(k+bl, m), j:min(j+bl, n)]
                distance_matrix[i:i+bl, j:j+bl] += subset1 * subset2

    return distance_matrix


