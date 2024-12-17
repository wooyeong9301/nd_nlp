import nltk
import re
import gensim
import pickle
import pyLDAvis
import pyLDAvis.gensim_models
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from nltk.stem import *
from gensim.models import CoherenceModel
from tqdm import tqdm



ddd = '/home/qwer/Desktop/ndsoft/ai/nd_nlp/Topics/nltk_data'
nltk.downloader.Downloader.default_download_dir(ddd)
# for _ in ['punkt', 'wordnet', 'stopwords', 'omw-1.4']:
#     if os.path.isdir(ddd.join(_)):
#         print('Already exists')
#         continue
#     else:
#         print('Download {}'.format(_))
#         nltk.download(_, download_dir=ddd)
# nltk.download('punkt', download_dir=ddd) # Stemming
# nltk.download('wordnet', download_dir=ddd) # Lemmatization
# nltk.download('stopwords', download_dir=ddd) # Stopword removal
# nltk.download('omw-1.4', download_dir=ddd)

nltk.data.path.append(ddd)
stopwords = set(nltk.corpus.stopwords.words('english'))
try:
    df_fetch20 = pd.read_pickle('fetch_20.pkl')
    print('Get pickled data')
    # df = pd.DataFrame(fetch_20.data, columns=['text'])

except:
    from sklearn.datasets import fetch_20newsgroups
    fetch_20 = fetch_20newsgroups(subset='train')
    df_fetch20 = pd.DataFrame(fetch_20.data, columns=['text'])
    df_fetch20.to_pickle('fetch_20.pkl')
    print('Get data from sklearn.datasets')


# Remove urls
def remove_url(text):
    text = re.sub(r'http(s)?:\S*', '', text)
    return text

# Remove mentions and hashtags
def remove_m_and_tags(text):
    text = re.sub(r'@\S*', '', text)
    test = re.sub(r'#\S*', '', text)
    return text

df_fetch20.text = df_fetch20.text.apply(remove_url)
df_fetch20.text = df_fetch20.text.apply(remove_m_and_tags)

# Preprocessing
def text_preprocessing(df, n):
    corpus = []
    lemma = WordNetLemmatizer()

    for news in df['text']:
        words = [w for w in nltk.tokenize.word_tokenize(news) if w not in stopwords]
        words = [lemma.lemmatize(w) for w in words if len(w)>=n]
        corpus.append(words)
    return corpus

corpus = text_preprocessing(df_fetch20, 3)

# Transform to gensim dictionary
dic = gensim.corpora.Dictionary(corpus)
bow_corpus = list(dic.doc2bow(d) for d in corpus)
pickle.dump(bow_corpus, open('corpus.pkl', 'wb'))
dic.save('dictionary.gensim')
# print('bow_corpus :', bow_corpus[0])
# print('dic :', dic)

# Model
lda_model = gensim.models.LdaMulticore(bow_corpus, num_topics=4, id2word=dic,
                                       passes=10)
print('workers :', lda_model.workers)
lda_model.save('model230713.gensim')

# Print words occuring in each of the topics
for idx,  topic in lda_model.print_topics(num_words=10):
    print('Topic : {} // Words : {}'.format(idx, topic))

# Evaluation
# cm = CoherenceModel(model=lda_model, corpus=bow_corpus, texts=corpus, coherence='c_v')
# coherence_lda = cm.get_coherence()
# print(coherence_lda)

topics = []
score = []

for i in tqdm(range(2, 15, 1)):
    lda_model = gensim.models.LdaMulticore(corpus=bow_corpus, num_topics=i, id2word=dic,
                                           passes=10, iterations=5, random_state=42)
    cm = CoherenceModel(model=lda_model, corpus=bow_corpus, texts=corpus, coherence='c_v')
    topics.append(i)
    score.append(cm.get_coherence())
# 최적의 점수를 갖는 토픽 수를 추출해보자

plt.plot(topics, score)
plt.xlabel('# of Topics')
plt.ylabel('Coherence score')
plt.savefig('scores.jpg')

# lda_model2 = gensim.models.LdaMulticore(bow_corpus, num_topics=2, id2word=dic, passes=8)
# lda_model2.save('model230713_2.gensim')
#
# for idx,  topic in lda_model2.print_topics(num_words=10):
#     print('Topic : {} // Words : {}'.format(idx, topic))
#
# # Load the dictionary, corpus and model files saved earlier
# dictionary = gensim.corpora.Dictionary.load('dictionary.gensim')
# corpus = pickle.load(open('corpus.pkl', 'rb'))
# lda = gensim.models.ldamodel.LdaModel.load('model230713_2.gensim')
# # pyLDAvis.enable_notebook()
# vis = pyLDAvis.gensim_models.prepare(lda, bow_corpus, dic)
# pyLDAvis.save_html(vis, 'vis.html')
# # pyLDAvis.show(vis)
