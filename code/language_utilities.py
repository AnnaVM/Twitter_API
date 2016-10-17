'''
You need to have the Stanford NER  Tagger downloaded

remove_numbers: from text
remove_en_em: from text, split words that have short and long dashes and backslach

handle_single_tweet
'''
import os
import re

import nltk
from nltk.tokenize import word_tokenize

from collections import defaultdict

def remove_numbers(text):
    numbers = re.compile(r'\b\w*[0-9]')
    return re.sub(numbers, '', text)

def remove_en_em(tokens):
    set_separator = set(["-", "/"])
    clean_tokens = []
    for i, token in enumerate(tokens):
        intersection = set(list(token)) & set_separator
        if len(intersection)>0:
            for sep in set_separator:
                token = ' '.join(token.split(sep))
            clean_tokens += token.split()
        else:
            clean_tokens.append(token)
    return clean_tokens

def handle_single_tweet(text, remove_set, st_instance, lem_stem_instance, method='lemmatize'):
    '''
    parameters:
    ----------
    text: as STR,
         from tweet text with no hashtags and no links
    remove_set: as set
         all the words (stopwords and punctuations that we want to remove)
         from string import punctuation
         from nltk import stopwords
         remove_set = set(punctuation).union(set(stopwords.words('english')))
    st_instance: as instance of StanfordNERTagger('english.all.3class.distsim.crf.ser.gz')
    lem_stem_instance: depending on the method, an instance of WordNet Lemmatizer
          or Porter Stemmer
          wn_lemmatizer = WordNetLemmatizer()
          porter_stemmer = PorterStemmer()
    method: lemmatize, stem

    returns
    -------
    processed_tokens as LST of STR, a list of the tokens that have not been
        removed and that have been stemmed/lemmatized
    dict_by_type: as DICT
        key = nltk.tag type (adv, adj, verbs with abbrev like JJS, RBS,...)
        value = [tokens]

    what we want to remove
    ---------------
        - stopwords
        - very short words (<= 2 characters)
        - punctuation marks (from punctuation)
        - proper nouns ('O' take)
    '''
    text = remove_numbers(text)

    #get list of tokens
    tokens = word_tokenize(text)

    #handle short dash, long dash, back /
    tokens = remove_en_em(tokens)

    #tag the tokens (nltk and stanford)
    pos_list = nltk.pos_tag(tokens)
    st_tag_list = st_instance.tag(tokens)

    tokens_indicative = []
    tags = []
    for i, token in enumerate(tokens):
        if (token not in remove_set) and\
           (st_tag_list[i][1] == 'O') and\
            len(token)>2:
            tokens_indicative.append(token)
            tags.append(pos_list[i])

    dict_by_type = defaultdict(list)
    processed_tokens = []
    if method == 'lemmatize':
        for i,token in enumerate(tokens_indicative):
            word = lem_stem_instance.lemmatize(token.lower())
            processed_tokens.append(word)
            dict_by_type[tags[i][1]].append(word)
    elif method == 'stem':
        for i,token in enumerate(tokens_indicative):
            word = lem_stem_instance.stem(token.lower())
            processed_tokens.append(word)
            dict_by_type[tags[i][1]].append(word)

    return processed_tokens, dict_by_type
