from pymongo import MongoClient
from pprint import pprint
import json
import pandas as pd
import numpy as np
import re
import string
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from nltk import pos_tag

import numpy as np
import pandas as pd
pd.options.display.max_rows = 999

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD

from gensim import corpora, models, similarities, matutils

from matplotlib import pyplot as plt

import pickle

from scipy.spatial.distance import euclidean
from sklearn.metrics.pairwise import cosine_similarity

wnl = WordNetLemmatizer()
tokenizer = RegexpTokenizer('\s+', gaps=True)

with open('full_hiphop.pickle', 'rb') as file:
    full_hiphop = pickle.load(file)

with open('full_other.pickle', 'rb') as file:
    full_other = pickle.load(file)

with open('count_vec.pickle', 'rb') as file:
    count_vec = pickle.load(file)

with open('hiphop_vec.pickle', 'rb') as file:
    hiphop_vec = pickle.load(file)

with open('other_vec.pickle', 'rb') as file:
    other_vec = pickle.load(file)

with open('first_lda.pickle', 'rb') as file:
    lda = pickle.load(file)

with open('kmeans.pickle', 'rb') as file:
    km = pickle.load(file)

with open('hiphop_lda.pickle', 'rb') as file:
    lda_hiphop = pickle.load(file)

with open('other_lda.pickle', 'rb') as file:
    lda_other = pickle.load(file)

def undo_list(lyr):
    '''Takes strings in a list or nested lists and return one continuous string'''
    if type(lyr) == str:
        return lyr
    else:
        line = ''
        for li in lyr:
            line += ' ' + undo_list(li)
        return line

def nouns_adj(text):
    '''Given a string of text, tokenize the text and pull out only the nouns and adjectives.'''
    is_noun_adj = lambda pos: pos[:2] == 'NN' or pos[:2] == 'JJ'
    tokenized = tokenizer.tokenize(text)
    nouns_adj = [word for (word, pos) in pos_tag(tokenized) if is_noun_adj(pos)]
    return ' '.join(nouns_adj)

def clean_text(text):
    '''Cleans input text'''
    text = re.sub('\w*\d\w*', ' ', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text.lower())
    text = re.sub(r'[^\x00-\x7F]+','', text)
    text = re.sub(' +', ' ',text)
    text = re.sub(r'chorus|verse|intro|bridge|outro','', text)
    text = nouns_adj(text)
    tokenizer = RegexpTokenizer('\s+', gaps=True)
    toke_text = tokenizer.tokenize(text)
    lem = [wnl.lemmatize(word) for word in toke_text]
    text = undo_list(lem).strip()
    return text

def first_lda(text):
    '''Applies first round LDA on input text'''
    newwords_df = count_vec.transform([text])

    newwords_df = newwords_df.transpose()
    new_corpus = matutils.Sparse2Corpus(newwords_df)

    newdoctopmat = lda.__getitem__(new_corpus, eps=0)
    new_csr = matutils.corpus2csc(newdoctopmat)
    new_doc_top = new_csr.T.toarray()
    return new_doc_top

def hiphop_or_other(array):
    '''Assigns input text to either hiphop or other subset of data'''
    return km.predict(array)[0]

def similar_hiphop(text):
    '''Applies second round hiphop LDA to input text and returns most similar artist'''
    newwords_df = hiphop_vec.transform([text])

    newwords_df = newwords_df.transpose()
    new_corpus = matutils.Sparse2Corpus(newwords_df)

    newdoctopmat = lda_hiphop.__getitem__(new_corpus, eps=0)
    new_csr = matutils.corpus2csc(newdoctopmat)
    new_doc_top = new_csr.T.toarray()

    min_dist = np.Inf
    closest_ind = -1
    for index, row in full_hiphop.iterrows():
        dist = euclidean(new_doc_top[0], row[3:])
        if dist < min_dist:
            min_dist = dist
            closest_ind = index
    return full_hiphop.iloc[closest_ind].Artist

def similar_other(text):
    '''Applies second round other LDA to input text and returns most similar artist'''
    newwords_df = other_vec.transform([text])

    newwords_df = newwords_df.transpose()
    new_corpus = matutils.Sparse2Corpus(newwords_df)

    newdoctopmat = lda_other.__getitem__(new_corpus, eps=0)
    new_csr = matutils.corpus2csc(newdoctopmat)
    new_doc_top = new_csr.T.toarray()

    min_dist = np.Inf
    closest_ind = -1
    for index, row in full_other.iterrows():
        dist = euclidean(new_doc_top[0], row[3:])
        if dist < min_dist:
            min_dist = dist
            closest_ind = index
    return full_other.iloc[closest_ind].Artist

def find_similar_artist(text):
    cleaned = clean_text(text)
    ar = first_lda(cleaned)
    if hiphop_or_other(ar) == 1:
        return similar_hiphop(cleaned)
    else:
        return similar_other(cleaned)
