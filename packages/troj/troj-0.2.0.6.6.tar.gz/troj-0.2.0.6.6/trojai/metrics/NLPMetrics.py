import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk import download
import gensim.downloader as api
from nltk.tokenize import word_tokenize
download('punkt')

download('stopwords')  # Download stopwords list.
stop_words = stopwords.words('english')



def count_stopwords(s, normalize=True):
    '''
    Counts the number of stopwords in a sentence.
    :param s:
    :param normalize:
    :return:
    '''
    word_tokens = word_tokenize(s)

    stopwords_s = [w for w in word_tokens if w in stop_words]
    if normalize:
       return len(stopwords_s) / len(word_tokens)
    else:
        return len(stopwords_s)

def count_non_stopwords(s, normalize=True):
    '''
    Counts the number of non-stop words in a sentence.
    :param s:
    :param normalize:
    :return:
    '''
    word_tokens = word_tokenize(s)
    n_stop = [w for w in word_tokens if w not in stop_words]
    if normalize:
       return len(n_stop) / len(word_tokens)
    else:
        return len(n_stop)

def get_swapped(inp1, inp2, remove_stop=False):
    '''
    Gets swapped words from two sentences.
    :param inp1:
    :param inp2:
    :param remove_stop:
    :return:
    '''
    proc_inp1 = word_tokenize(inp1)
    proc_inp2 = word_tokenize(inp2)
    if remove_stop:
        proc_inp1 = [w for w in proc_inp1 if w not in stop_words]
        proc_inp2 = [w for w in proc_inp2 if w not in stop_words]
    if len(proc_inp1) != len(proc_inp2):
        return []
    elif len(proc_inp1) == len(proc_inp2):
        swapped_words = []
        for idx in range(len(proc_inp1)):
            if proc_inp1[idx] != proc_inp2[idx]:
                swapped_words.append((proc_inp1[idx], proc_inp2[idx]))
        return swapped_words

def percent_swapped(inp1, inp2, remove_stop=False):
    '''
    Returns percent of words swapped.
    :param inp1:
    :param inp2:
    :param remove_stop:
    :return:
    '''
    swapped = get_swapped(inp1, inp2, remove_stop)
    proc_inp1 = word_tokenize(inp1)
    if remove_stop:
        proc_inp1 = [w for w in proc_inp1 if w not in stop_words]
    if swapped != None:
        perc_swapped = len(swapped)/len(proc_inp1)
    else:
        perc_swapped = 0
    return perc_swapped, swapped



def word_based_character_count(s):
    '''
    counts characters in a sentence which belong to words.
    :param s:
    :return:
    '''
    words = s.split()
    letter_count_per_word = {w: len(w) for w in words}
    count = sum(list(letter_count_per_word.values()))
    return count

def levenshteinDistance(s1, s2):
    '''
    Computes levenshtein distance between two strings.
    :param s1:
    :param s2:
    :return:
    '''
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

def swapped_lev_dist(swapped_list):
    '''
    Gets Levenshtein distance between swapped words.
    :param swapped_list:
    :return:
    '''
    if len(swapped_list)==0:
        return []
    else:
        dists=[]
        for swapped_words in swapped_list:
            dist = levenshteinDistance(swapped_words[0], swapped_words[1])
            dists.append(dist)
        return dists


def get_w2v_oov_words(spcy_doc):
    '''
    Checks for words in the input that are not in the word2vec vocabulary.
    :param spcy_doc:
    :return:
    '''
    oov_words = []
    for token in spcy_doc:
        if token.is_oov:
            oov_words.append(token.text)
    return oov_words


def tagger(spc_doc):
    '''
    Gets POS tags
    :param spc_doc:
    :return:
    '''
    comps = []
    for token in spc_doc:
        pos = (token.text, token.pos_)
        comps.append(pos)
    return comps

class WordMoverDistance:
    '''
    Computes word mover distance between two samples
    '''
    def __init__(self, embedder_name):
        ''' load Gensim embedder'''
        self.embedder = api.load(embedder_name)

    def distance(self, inp1, inp2):
        proc_inp1 = word_tokenize(inp1)
        proc_inp2 = word_tokenize(inp2)
        dist = self.embedder.wmdistance(proc_inp1, proc_inp2)
        return dist


if __name__=='__main__':
    sentence_obama = 'Obama speaks to the media in Illinois'
    print(word_tokenize(sentence_obama))
    sentence_president = 'The president greets the press in Chicago'
    wmd = WordMoverDistance('word2vec-google-news-300')
    d = wmd.distance(sentence_obama, sentence_president)
    print(d)