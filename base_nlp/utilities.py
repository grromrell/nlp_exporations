import array
import numpy as np
import scipy.sparse as sp

def sparse_amax(matrix):
    if sp.isspmatrix_csc(matrix):
        pass
    elif sp.isspmatrix(matrix):
        matrix = matrix.tocsc()
    else:
        raise ValueError("Input matrix must be a scipy.sparse matrix")
    results = array.array(str('i'))
    for i in xrange(matrix.shape[1]):
        indices = matrix.indptr[i:i+2]
        if indices[0] != indices[1]:
            results.append(np.max(matrix.data[indices[0]:indices[1]]))
        else:
            results.append(0)
    return np.array(results)
