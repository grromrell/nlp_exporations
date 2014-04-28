from __future__ import division
import scipy.sparse as sp
import numpy as np
import string
import array
import nltk
import csv
import os
import re
from stop_words import stop_list
from collections import Counter, defaultdict

class Bow:

    def __init__(self, topdir=None, tokenizer='word_size', stem=False, 
                 stop_words=True, min_word_len=4, max_word_pct=1, min_word_cnt=0, 
                 max_vocab_size=100000):
        """
        A class to support basic bag of words operations. Can tokenize,
        vectorize and weight you incoming text data and output term_document
        matrices. Optimized to use sparse vectors.

        Parameters
        ----------
        topdir : string
            the location of the directory containing the text documents to be
            analyzed

        tokenizer : ['word_size', 'white_space', 'punctuation'], default = word_size
            the method of tokenization, word_size will split on any word three
            characters or longer, white_space will split on white_space and 
            punctuation will split on punctuation. Can also pass a regex
            statement that be used to parse the text.

        stem : bool, default = False
            the option to stem the tokens, which will increase accuracy but
            decrease readability

        stop_words : bool or iterable, default=True
            strips out english stopwords when true, if false then stop words
            will not be removed. If an iterable then the iterable will be used
            to filter stopwords

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
        self.topdir = topdir
        self.tokenizer = tokenizer
        self.stem = stem
        self.min_word_len = min_word_len
        self.max_word_pct = max_word_pct
        self.min_word_cnt = min_word_cnt
        self.max_vocab_size = max_vocab_size

        self.vocab = None
        self.word_matrix = None
        self.vocab_cnt = None

        self.id_list = []
        self.doc_cnt = 0

        self.stop_words = None
        if stop_words:
            if hasattr(stop_words, '__iter__'):
                self.stop_words = stop_words
            else:
                self.stop_words = stop_list

    def _word_tokenize(self, text):
        """
        Accepts document text and splits into words

        Parameters
        ----------
        text : string

        Returns
        -------
        list of tokens
        """
        if self.tokenizer == 'word_size':
            compiler = re.compile(r'\b\w\w\w+\b')
        elif self.tokenizer == 'punctuation':
            compiler = re.compile(r'\w+|[^\w\s]+')
        elif self.tokenizer == 'white_space':
            return text.translate(None, string.punctuation).split()
        else:
            compiler = re.compile(self.tokenizer)

        if compiler:
            return compiler.findall(text)

    def tokenizer(self):
        """
        Accepts the directory where text documents are stored and splits them
        into words

        Returns
        -------
        tokens: generator
        """
        id_list = []

        for root, dirs, files in os.walk(self.topdir):
            for file in filter(lambda file: file.endswith('.txt'), files):
                id_list.append((file.split('.')[0]))
                with open(os.path.join(root, file), 'rb') as text_file:
                    text = text_file.read()
                words = self._word_tokenize(text)
                tokens = [w.encode('utf-8', 'ignore').decode('utf-8').lower()
                          for w in words if w not in self.stop_words]
                if self.stem:
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
        values = np.ones(len(indices), dtype=np.int)

        word_matrix = sp.csr_matrix((values, indices, indptr), shape = (len(indptr) - 1, len(vocab)))

        word_matrix.sum_duplicates()
        
        self.vocab = vocab
        self.word_matrix = word_matrix

    def trim_vocab(self):
        """
        Uses processing rules to trim vocabulary size.       
        """
        word_matrix = self.word_matrix
        vocab = self.vocab
        counts = np.bincount(word_matrix.indices).tolist()
        term_count = dict(zip(vocab.keys(), counts))  

        for term in vocab.keys():
            if len(term) < self.min_word_len:
                del vocab[term]
                del term_count[term] 
            elif (term_count[term]/self.doc_cnt) > self.max_word_pct:
                del vocab[term]
                del term_count[term]
            elif (term_count[term]) < self.min_word_cnt:
                del vocab[term]
                del term_count[term]

        for term in sorted(term_count, key=term_count.get):
            if len(vocab) > self.max_vocab_size:
                del vocab[term]

        reindex = vocab.values()
        newterms = vocab.keys()
        newindex = np.arange(len(vocab))
        vocab = dict(zip(newterms, newindex))
        
        self.vocab_cnt = term_count
        self.vocab = vocab
        self.word_matrix = word_matrix[:, reindex]

    def tfidf(self, augmented_df=False):
        """
        Performs a tfidf transformation on word vectors, using augmented term
        frequency for increased accuracy.

        Parameters
        ---------
        augemented_df : bool, default = False
            If true use augmented document frequency, which scales document
            by their most common word. If false, perform normal tfidf
        """
        counts = np.bincount(self.word_matrix.indices)
        idf = np.log(self.doc_cnt/(counts + 1))
        if augmented_df:
            maxes = np.array(np.amax(self.word_matrix.todense(), axis=1), dtype=np.float)
            aug_maxes = (1/(1+maxes))
            self.word_matrix = sp.csr_matrix(self.word_matrix.multiply(aug_maxes))
        diag_matrix = sp.spdiags(idf, 0, len(counts), len(counts))
        tfidf_matrix = self.word_matrix * diag_matrix
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

def corpus_gensim(word_matrix, stream=False):
    """
    Transforms sparse word_matrix (typically from Bow Class) into the two
    gensim compatible corpus versions, one for streaming and one for static
    use. These two corpi can be used to access most of the gensim functionality

    Parameters
    ----------
    word_matrix : scipy.sparse.csr_matrix
        a word_matrix containing a sparse corpus with rows as documents and
        words as columns

    stream : bool, default=False
        whether to return the corpus in stream mode or not

    Returns
    -------
    stream_corpus : gensim.stream_corpus
        a gensim corpus for streaming data

    corpus : gensim.corpus
        a gensim corpus for static use
    """
    try:
        import gensim
    except:
        raise ValueError("Gensim compatability requires gensim to be installed")
    if stream:
        corpus = gensim.matutils.Sparse2Corpus(word_matrix.T)
    else:
        corpus = gensim.matutils.Scipy2Corpus(word_matrix.T)
    return corpus

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
    try:
        import gensim
    except:
        raise ValueError("Gensim compatability requires gensim to be installed")
    bow = gensim.matutils.scipy2sparse(vector.T)
    return bow
