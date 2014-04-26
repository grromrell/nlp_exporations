import math
import numpy
import scipy.sparse

def compute_distance(matrix):
    if scipy.sparse.issparse(matrix):
        distance_matrix = (matrix * matrix.T).toarray()
    else:
        distance_matrix = matrix * matrix.T
    return distance_matrix

def compute_large(matrix):
    if not scipy.sparse.issparse(matrix):
        raise ValueError('Input matrix is not a scipy.sparse matrix')
    try:
        import tables
    except:
        raise ValueError('Large distance calculation depends on pytables')
    f = tables.open('product.h5', 'w')
    filters = tables.Filters(complevel=3, complib='blosc')
    distance_matrix = f.create_carray(f.root, 'distance_matrix', 
                                      tables.Atom.from_dtypes(matrix.dtype),
                                      shape=(matrix.shape[0], matrix.shape[0]),
                                      filters = filters)
    buff_size = (2**20)*32
    bl = math.sqrt(buff_size / out.dtype.itemsize)
    bl = 2**int(math.log(bl, 2))
    for i in range(0, matrix.shape[0], bl):
        for j in range(0, matrix.shape[1], bl):
            for k in range(0, matrix.shape[0], bl):
                subset1 = matrix[i:min(i+bl, l), k:min(k+bl, m)]
                subset2 = (matrix.T)[k:min(k+bl, m), j:min(j+bl, n)]
                distance_matrix[i:i+bl, j:j+bl] += matrix * matrix.T

    return distance_matrix


