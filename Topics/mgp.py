from numpy.random import multinomial
from numpy import log, exp
from numpy import argmax
import json

class MovieGroupProcess:
    def __init__(self, K=8, alpha=0.1, beta=0.1, n_iters=30):
        '''

        :param K: int.  Upper bound on the number of possible clusters.
        :param alpha: float between 0 and 1.  Alpha controls the probability that a student will join a table that is currently empty.
            When alpha is 0, no one will join an empty table.
        :param beta: float between 0 and 1.  Beta controls the student's affinity for other students with similar interests.
            A low beta means that students desire to sit with students of similar interests.
            A high beta means that students are more influenced by the popularity of a table.
        :param n_iters: int. Number of iterations or times that each student is reassigned to a new table.
            Should be a high enough value for the model to converge.
        '''

        self.K = K
        self.alpha = alpha
        self.beta = beta
        self.n_iters = n_iters

        self.number_docs = None
        self.vocab_size = None
        self.cluster_doc_cnt = [0 for i in range(K)]
        self.cluster_word_cnt = [0 for i in range(K)]
        self.cluster_word_dist = [{} for i in range(K)]

    @staticmethod
    def from_data(K, alpha, beta, D, vocab_size, cluster_doc_cnt, cluster_word_cnt, cluster_word_dist):
        ''' Reconstitute a MovieGroupProcess from previously fit data '''
        mgp = MovieGroupProcess(K, alpha, beta, n_iters=30)
        mgp.number_docs = D
        mgp.vocab_size = vocab_size
        mgp.cluster_doc_cnt = cluster_doc_cnt
        mgp.cluster_word_cnt = cluster_word_cnt
        mgp.cluster_word_dist = cluster_word_dist
        return mgp

    @staticmethod
    def _sample(p:list) -> int:
        '''
        Sample with probability vector p from a multinomial distribution
        return : index of randomly selected output
        Multinomial로 cluster number를 randomly 뽑아낸다.
        '''
        # print('_sample : Multinomial로 cluster number를 randomly 뽑아낸다.')
        return [i for i, entry in enumerate(multinomial(1, p)) if entry != 0][0]

    def fit(self, docs, vocab_size):
        '''
        Cluster the input documents
        :param docs: list of lists containing the unuque token set of each document
        :param vocab_size: total vocabulary size for each document
        :return: list of length : len(doc)
        '''
        alpha = self.alpha
        beta = self.beta
        K = self.K
        n_iters = self.n_iters
        V = vocab_size

        D = len(docs)
        self.number_docs = D
        self.vocab_size = vocab_size

        # unpack to easy var names
        m_z = self.cluster_doc_cnt # cluster_z로 분류되는 문서 수
        n_z = self.cluster_word_cnt # cluster_z에 해당하는 단어 수
        n_z_w = self.cluster_word_dist # cluster_z에 해당하는 단어의 빈도
        cluster_cnt = K
        d_z = [None for i in range(len(docs))] # 각 doc에 대한 위치에 cluster number가 저장될 것이다.

        # Initialize the clusters
        for i, doc in enumerate(docs):
            # Choose a random initial cluster for the doc
            z = self._sample([1.0 / K for _ in range(K)]) # z에 cluster number 할당
            d_z[i] = z # i번째 문서에 해당하는 z를 저장한다
            m_z[z] += 1
            n_z[z] += len(doc)

            # word가 n_z_w[z]에 있는지 체크하고 카운트 늘리는 과정
            for word in doc:
                if word not in n_z_w[z]:
                    n_z_w[z][word] = 0
                n_z_w[z][word] += 1

        for _iter in range(n_iters): # 한번씩 돌면
            total_transfers = 0 # ????

            for i, doc in enumerate(docs):
                # Remove the doc from it's current cluster to reassign
                z_old = d_z[i]
                m_z[z_old] -= 1 # cluster에서 문서 하나 빠졌으니 전체 수 -1
                n_z[z_old] -= len(doc)

                for word in doc:
                    n_z_w[z_old][word] -= 1
                    if n_z_w[z_old][word] == 0:
                        del n_z_w[z_old][word]

                # Draw sample from distribution to find new cluster
                p = self.score(doc)
                z_new = self._sample(p)

                # Transfer doc to the new cluster
                if z_new != z_old:
                    total_transfers += 1

                d_z[i] = z_new
                m_z[z_new] += 1
                n_z[z_new] += len(doc)

                for word in doc:
                    if word not in n_z_w[z_new]:
                        n_z_w[z_new][word] = 0
                    n_z_w[z_new][word] += 1

            cluster_cnt_new = sum([1 for v in m_z if v>0])
            print(f"In stage {_iter} : transferred {total_transfers} clusters with {cluster_cnt_new} clusters populated")
            if total_transfers == 0 and cluster_cnt_new == cluster_cnt and _iter>25:
                print('Converged. Break out.')
                break

            cluster_cnt = cluster_cnt_new
        self.cluster_word_dist = n_z_w

        return d_z

    def score(self, doc):
        '''
        Score a document.
        http://dbgroup.cs.tsinghua.edu.cn/wangjy/papers/KDD14-GSDMM.pdf

        :param doc: list[str]. The doc token stream.
        :return: list[float]. A length K probability vector
            where each component represents the probability of the document appearing in a particular cluster.
        '''
        alpha = self.alpha
        beta = self.beta
        K = self.K
        V = self.vocab_size
        D = self.number_docs
        m_z = self.cluster_doc_cnt
        n_z = self.cluster_word_cnt
        n_z_w = self.cluster_word_dist

        p = [0 for _ in range(K)]
        lD1 = log(D - 1 + K*alpha)
        doc_size = len(doc)
        for label in range(K):
            lN1 = log(m_z[label] + alpha)
            lN2 = 0
            lD2 = 0

            for word in doc:
                lN2 += log(n_z_w[label].get(word, 0) + beta)
            for j in range(1, doc_size+1):
                lD2 += log(n_z[label] + V*beta + j -1)

            p[label] = exp(lN1 - lD1 + lN2 - lD2)

        # normalize the probability vector
        pnorm = sum(p)
        pnorm = pnorm if pnorm > 0 else 1
        return [pp/pnorm for pp in p]

    def best_label(self, doc):
        '''
        Choose the highest probability label for the input document.
        :param doc: list[str]. The doc token stream
        :return:
        '''

        p = self.score(doc)
        return argmax(p), max(p)

    def word_score(self):
        word_dist = self.cluster_word_dist
        beta = self.beta
        V = self.vocab_size
        K = self.K
        phi = [{} for i in range(K)]

        for k in range(K):
            for word in word_dist[k]:
                phi[k][word] = (word_dist[k][word] + beta)/(sum(word_dist[k].values()) + V*beta)

        return phi











#
# def _sample(p:list) -> int:
#     '''
#     Sample with probability vector p from a multinomial distribution
#     return : index of randomly selected output
#     '''
#     print('p :', p)
#     result = 0
#     for i, entry in enumerate(multinomial(1, p)):
#         print('i :', i , '//', 'entry :', entry)
#         if entry != 0:
#             result = i
#         else:
#             continue
#     print(result)
#     return result
#
# K = 8
# _sample([1.0/K for _ in range(K)])
#
# nzw = [{} for i in range(K)]
#
#
#
#
# class test():
#     def __init__(self, a, b):
#         self.a = a
#         self.b = b
#
#     def aa(self, c):
#         a = self.a
#         b = self.b
#         self.b = b+c
#         print(b is self.b)
#
#         return (a,b,c)
#
#     def bb(self):
#         print(self.b, self.a)
#
#
# abc = test(a=1, b=3)
# print(abc.aa(5))
# abc.bb()
#
# nzw = [{'a':1, 'b':2}, {'c':1, 'd':3}, {'a':3, 'd':1}]
#
# doc = ['a', 'b']
# for label in range(3):
#     for word in doc:
#         print(f'label :{label}, word:{word}', log(nzw[label].get(word, 0)))