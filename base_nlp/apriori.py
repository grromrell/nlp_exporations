from __future__ import division
import scipy.sparse as sp
import numpy as np

class Apriori(object):
    """
    A class that implements the apriori frequent itemset search algorithm
    found in Agrawal and Srikant (1994). For more information read the
    original paper here: http://bit.ly/1gxxpIx

    Parameters
    ----------
    matrix: scipy.sparse matrix
        a term-document matrix with document as rows and words as columsn
    vocab: dictionary
        a vocabulary in a dictionary of form {'word': index}
    threshold: float
        minimum percentage of documents to be considered a frequency itemset
    """
    def __init__(self, matrix, vocab, threshold):
        self.matrix = matrix
        self.vocab = vocab
        self.threshold = threshold
        self.itemsets = {1: {}}

    def find(self):
        self.one_itemset()
        for k in xrange(2, self.matrix.shape[0]):
            candidates = self.candidate_gen(self.itemsets[k-1].keys(), k)
            k_itemset = self.k_itemsets(candidates, k)
            if k_itemset:
                self.itemsets[k] = k_itemset
            else:
                break

    def one_itemset(self):
        counts = np.bincount(self.matrix.indices).tolist()
        term_count = dict(zip(self.vocab.keys(), counts))
        for term in term_count.keys():
            if term_count[term]/self.matrix.shape[0] >= self.threshold:
                self.itemsets[1][(term,)] = term_count[term]

    def candidate_gen(self, itemset, k):
        candidates = []
        for i in xrange(len(itemset) - 1):
            for j in xrange(i+1, len(itemset)):
                potential = list(set(itemset[i] + itemset[j]))
                if len(potential) == k:
                    candidates.append(potential)

        for candidate in candidates:
            subsets = []
            for item in candidate:
                copy = candidate
                subsets.append(copy.remove(item))
            for subset in subsets:
                if subset not in itemset:
                    candidates.remove(candidate)
                    break
        return [tuple(candidate) for candidate in candidates]

    def k_itemsets(self, candidates, k):
        k_itemset = {}
        for candidate in candidates:
            indices = [self.vocab[term] for term in candidate]
            columns = [self.matrix[:,i] for i in indices]
            itemset_count = np.where(sp.hstack(columns).astype(np.bool).sum(1)
                                     == k, True, False).sum()
            if itemset_count/self.matrix.shape[0] >= self.threshold:
                k_itemset[candidate] = itemset_count
        return k_itemset
