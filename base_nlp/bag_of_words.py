from __future__ import division
import scipy.sparse as sp
import numpy as np
import itertools
import string
import gensim
import array
import nltk
import csv
import os
import os.path
from nltk.corpus import stopwords
from collections import Counter, defaultdict

class Bow:

    def __init__(self, topdir = None, stem = False):
        """
        A class to support basic bag of words operations. Can tokenize,
        vectorize and weight you incoming text data and output term_document
        matrices. Optimized to use sparse vectors.

        Parameters
        ----------
        topdir : string
            the location of the directory containing the text documents to be
            analyzed
        """
        
        self.topdir = topdir
        self.stem = stem

        self.vocab = None
        self.word_matrix = None
        self.vocab_cnt = None

        self.id_list = []
        self.doc_cnt = 0

    def tokenizer(self):
        """
        Takes raw text data parses it into tokens in the form of individual
        words. 

        Parameters
        ----------
        stem : bool, default = False
            the option to stem the tokens, which will increase accuracy but
            decrease readability

        Returns
        -------
        tokens: generator
        """

        id_list = []

        for root, dirs, files in os.walk(self.topdir):
            for file in filter(lambda file: file.endswith('.txt'), files):
                id_list.append((file.split('.')[0]))
                text = open(os.path.join(root, file),'rU').read()
                split = text.translate(None, string.punctuation).split()
                tokens = [w.decode('unicode_escape').encode('ascii', 'ignore').lower()
                          for w in split if not w in stopwords.words('english')
                          or w.isdigit()]

                if self.stem == True:
                    stemmer = nltk.PorterStemmer()
                    tokens = [porter.stem(t) for t in tokens if len(porter.stem(t)) > 3]
                
                yield tokens
        
        self.id_list = id_list
        self.doc_cnt = len(id_list)
                
    def vectorizer(self):
        """
        Turns tokens into a word vector in the bag of words format. Also
        builds a vocabulary which contains all of the unique words from the
        tokens.
        
        Parameters
        ----------

        col_name : string
            name of the column where the text data resides
        
        id_name : string
            name of the column that uniquely identifies each document

        stem : bool, default = False
            the option to stem the tokens, which will increase accuracy but
            decrease readability
        """
        vocab = defaultdict(None)
        vocab.default_factory = vocab.__len__

        indices = array.array(str('i'))
        indptr = array.array(str('i'))
        indptr.append(0)

        for tokens in Bow.tokenizer(self):
            for token in tokens:
                indices.append(vocab[token])
            indptr.append(len(indices))

        vocab = dict(vocab)
        values = np.ones(len(indices))

        word_matrix = sp.csr_matrix((values, indices, indptr), shape = (len(indptr) - 1, len(vocab)))

        word_matrix.sum_duplicates()
        
        self.vocab = vocab
        self.word_matrix = word_matrix

    def trim_vocab(self, min_word_len=4, max_word_pct=1, min_word_cnt=0, max_vocab_size=100000):
        """
        Uses processing rules to trim vocabulary size.

        Parameters
        ----------

        min_word_len : integer, default = 4
            the minimum word lengcol_name : string
            name of the column where the text data resides

        max_word_pct : float, default = 1
            the maximum occurance rate of a word, default is set to allow
            all words

        min_word_cnt : int, default = 0
            the minimum number of occurances of a words, default is set to 
            allow all words

        max_vocab_size : int, default = 100000
            the maximum size of your vocab
        """
        word_matrix = self.word_matrix
        vocab = self.vocab
        counts = np.array(word_matrix.sum(0)).astype(int).flatten().tolist()
        term_count = dict(zip(vocab.keys(), counts))  

        for term in vocab.keys():
            if len(term) < min_word_len:
                del vocab[term]
                del term_count[term] 
            elif (term_count[term]/self.doc_cnt) > max_word_pct:
                del vocab[term]
                del term_count[term]
            elif (term_count[term]) < min_word_cnt:
                del vocab[term]
                del term_count[term]

        for term in sorted(term_count, key=term_count.get):
            if len(vocab) > max_vocab_size:
                del vocab[term]

        reindex = vocab.values()
        newterms = vocab.keys()
        newindex = np.arange(len(vocab))
        vocab = dict(zip(newterms, newindex))
        
        self.vocab_cnt = term_count
        self.vocab = vocab
        self.word_matrix = word_matrix[:, reindex]

    def tfidf(self):
        """
        Performs a tfidf transformation on word vectors, using augmented term
        frequency for increased accuracy.
        """
        word_matrix = self.word_matrix
        vocab = self.vocab
        counts = np.array(word_matrix.sum(0)).astype(int).flatten().tolist()
        term_count = dict(zip(vocab.keys(), counts))
        idf = array.array(str('f'))

        for term in vocab.keys():
            idf.append(np.log(len(vocab)/(1 + term_count[term])))

        idf = sp.csr_matrix(idf)
        tfidf = sp.lil_matrix(word_matrix.shape)

        for i in xrange(word_matrix.shape[0]):
            row = word_matrix[i]
            augmented_row = row.multiply(1/row.max())
            tfidf_row = row.multiply(idf)
            tfidf[i] = tfidf_row

        tfidf_matrix = tfidf.tocsr()

        self.word_matrix = tfidf_matrix

    def to_csv(self, fileloc, item='vocab'):
        """
        Writes in memory objects to a csv

        Parameters
        ----------

        fileloc : string
            location to save csv
        
        item : ['vocab', 'word_matrix'], default = 'vocab'
            which item to save

        Returns
        -------

        """
        if item == 'vocab':
            vocab = self.vocab

            with open(fileloc, 'wb') as csvfile:
                writer = csv.writer(csvfile, delimiter = ',')
                writer.writerow(['word_id', 'word', 'frequency'])
                id = 1

                for i in range(len(vocab)):
                    row = [id, vocab.keys()[i], vocab.values()[i]]
                    writer.writerow(row)
                    id += 1

        if item == 'word_matrix':
            word_matrix = word_matrix.todense()
            
            with open(fileloc, 'wb') as csvfile:
                writer = csv.writer(csvfile, delimiter = ',')
                word_ids = np.arange(len(word_matrix))
                writer.writerow(['Word ID &s' % i for i in word_ids])

                for row in word_matrix:
                    writer.writerow(list(row))

def single_tokenizer(text, stem = False):
    """
    Tokenizes a single text object
    
    Parameters
    ----------

    text : string
        text to be tokenized

    stem : bool, default = False
        whether to use stemming to increase accuracy, reduces readability

    Returns
    -------

    tokens : list
        list of strings containing tokens
    """
    wordtokens = text.split('\n').split('.').split('')
    tokens = [w.decode('unicode_escape').encode('ascii', 'ignore').lower() for w in wordtokens if not w in stopwords.words('english') or w.isdigit()]

    if stem == True:
        stemmer = nltk.PorterStemmer()
        tokens = [porter.stem(t) for t in tokens if len(porter.stem(t)) > 3]
                    
    yield tokens

def doc2bow(tokens, vocab):
    """
    Transforms tokens into bag of word representation from a given vocabulary,
    a port of the gensim function of the same name

    Parameters
    ----------
    
    tokens: list
        a list of tokens from a body of text

    vocab : dict
        a dictionary of format {word : index}

    Returns
    -------

    word_vector : scipy.sparse.csr_matrix
        a sparse vector bag of word representation of the given tokens

    """
    indices = array.array(str('i'))
    indptr = array.array(str('i'))
    indptr.append(0)
    
    for token in tokens:
        indices.append(vocab[token])
    
    indptr.append(len(indices))
    values = np.ones(len(indices))
    word_vector = sp.csr_matrix((values, indices, indptr), shape = (len(indptr) - 1, len(vocab)))
    
    word_vector.sum_duplicates()
    return word_vector

def corpus_gensim(word_matrix):
    """
    Transforms sparse word_matrix (typically from Bow Class) into the two
    gensim compatible corpus versions, one for streaming and one for static
    use. These two corpi can be used to use most of the gensim functionality

    Parameters
    ----------
    word_matrix : scipy.sparse.csr_matrix
        a word_matrix containing a sparse corpus with rows as documents and
        words as columns

    Returns
    -------
    
    stream_corpus : gensim.stream_corpus
        a gensim corpus for streaming data

    corpus : gensim.corpus
        a gensim corpus for static use
    """
    stream_corpus = gensim.matutils.Sparse2Corpus(word_matrix.T)
    corpus = gensim.matutils.Scipy2Corpus(word_matrix.T)
    return stream_corpus, corpus

def vector_gensim(vector):
    """
    Transforms an individual vector into a gensim sparse representation,
    when used in conjunction with doc2bow can be used to make lsi queries
    in gensim

    Parameters
    ----------

    vector : scipy.sparse.csr_matrix
        an individual word_vector in scipy sparse format

    Returns
    -------
    bow : gensim.sparse
        a word vector in the correct gensim format
    """
    bow = gensim.matutils.scipy2sparse(vector.T)
    return bow
