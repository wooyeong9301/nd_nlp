import numpy as np
import pandas as pd
import sys
import gensim
import spacy
import re
import os
import nltk


from mgp import MovieGroupProcess
from gensim.models.coherencemodel import CoherenceModel
from gensim import corpora, models
from gensim.utils import simple_preprocess
from gensim.models.ldamulticore import LdaMulticore
from gensim.models import Phrases
from gensim.models.phrases import Phraser
from nltk.stem import *




# Prepare data
def get_data(route):
    data = pd.read_csv(route, encoding='utf-8')
    print('Data :', data.head())

    return data

data = get_data('/home/qwer/Desktop/ndsoft/ai/nd_nlp/Data/tripadvisor_hotel_reviews.csv')

# Check length
data['length'] = data.Review.apply(lambda row:len(row.split()))
print('Mean length :', data['length'].mean())

# Preprocessing
data['review_pre'] = data.Review.values.tolist()

# Remove characters
data['review_pre'] = [re.sub('\s+', ' ', sent) for sent in data['review_pre']]
data['review_pre'] = [re.sub("\'", '', sent) for sent in data['review_pre']]

def sent_to_words(sentences):
    for sent in sentences:
        yield gensim.utils.simple_preprocess(str(sent), deacc=True)


targets = ['punkt', 'wordnet', 'stopwords', 'omw-1.4', 'averaged_perceptron_tagger']
dpath = '/home/qwer/Desktop/ndsoft/ai/nd_nlp/Topics/nltk_data'
for target in targets:
    nltk.download(target, download_dir=dpath)
    print(f'{target} downloaded.')





# Bigram을 먼저 만든 후, 그 Bigram을 바탕으로 Trigram 생성
def make_ngrams(texts):
    i = 1
    bigram = gensim.models.Phrases(texts, min_count=1, threshold=10)
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    trigram = gensim.models.Phrases(bigram[texts], threshold=10)
    trigram_mod = gensim.models.phrases.Phraser(trigram)

    bigram_text = [bigram_mod[doc] for doc in texts]
    for doc in bigram_text:
        print(bigram_mod[doc])
        print(f'{i} :', trigram_mod[bigram_mod[doc]])
        i += 1

    trigram_text = [trigram_mod[bigram_mod[doc]] for doc in bigram_text]

    return trigram_text

def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) if word not in gensim.parsing.
             preprocessing.STOPWORDS.union(
        {'also', 'meanwhile', 'however', 'time', 'hour', 'soon', 'day', 'book', 'there', 'hotel', 'room', 'leave',
         'arrive', 'place', 'stay', 'staff', 'location', 'service', 'come', 'check', 'ask', 'lot', 'thing', 'soooo',
         'add', 'rarely', 'use', 'look', 'minute', 'bring', 'need', 'world', 'think', 'value', 'include'})]
            for doc in texts]


def lemmatization(texts, allowed=['NOUN', 'ADJ', 'VERB', 'ADV']):
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent))
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed])
    return texts_out


def top_words(cluster_word_dist, top_cluster, values):
    for cluster in top_cluster:
        sort_dicts = sorted(mgp.cluster_word_dist[cluster].items(), key=lambda k:k[1], reverse=True)[:values]
        print(f'Cluster {cluster} : {sort_dicts}')



review_tokens = list(sent_to_words(data['review_pre']))
review_tokens = make_ngrams(review_tokens)
review_lemma = lemmatization(review_tokens)
review_lemma_stop = remove_stopwords(review_lemma)

# GSDMM for the topic modeling
# 최적의 parameter를 찾는 알고리즘 필
mgp = MovieGroupProcess(K=8, alpha=0.1, beta=0.5, n_iters=30)
vocab = set(x for review in review_lemma_stop for x in review)
n_terms = len(vocab)
model = mgp.fit(review_lemma_stop, n_terms)

doc_count = np.array(mgp.cluster_doc_cnt)
print('Number of docs per topic :', doc_count)

# topics sorted by the number of document they are allocated to
top_index = doc_count.argsort()[-10:][::-1]
print('Most important clusters :', top_index)

# Show the top 5 words in term frequency for each cluster
top_words(mgp.cluster_word_dist, top_index, 10)

topic_dict = {}
topic_names = ['Topic 1', 'Topic 2', 'Topic 3', 'Topic 4', 'Topic 5', 'Topic 6', 'Topic 7', 'Topic 8', ]
for i, topic_num in enumerate(top_index):
    topic_dict[topic_num] = topic_names[i]

print(topic_dict)

def topic_df(model=mgp, data=data, topic=topic_dict, lemma_text=review_lemma_stop, threshold=0.3):
    result = pd.DataFrame(columns=['Text', 'Topic', 'Rating', 'Lemma'])

    for i, text in enumerate(data.Review):
        result.at[i, 'Text'] = text
        result.at[i, 'Rating'] = data.Rating[i]
        result.at[i, 'Lemma'] = lemma_text[i]
        prob = model.best_label(review_lemma_stop[i])

        if prob[1] >= threshold:
            result.at[i, 'Topic'] = topic_dict[prob[0]]
        else:
            result.at[i, 'Topic'] = 'Other'
    print(result.head())

    return result


result = topic_df()

phi = mgp.word_score()
print(phi[0])

