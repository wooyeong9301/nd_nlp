import re
from collections import OrderedDict

#####################

from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords as sw
from nltk import pos_tag, ne_chunk
from nltk.tokenize import sent_tokenize, word_tokenize, WhitespaceTokenizer
from nltk.stem import WordNetLemmatizer as lemma

from Tokenize.tempData.tokenizeTemplate import TokenizeTemplate


class EnParser(TokenizeTemplate):

    def __init__(self):
        TokenizeTemplate.__init__(self)

        self.lemma = lemma()
        self.stopword = sw.words('english')

        self.noun_list = self.__load_noun_pos_list()
        self.verb_list = self.__load_verb_pos_list()

    def preprocessing_pipeline(self, input_str: str):
        self.org_sentence = input_str
        self.sentence_tokenize()
        self.whitespace_tokenize()
        self.pos_tokenize()
        self.get_ner()
        self.remove_stopword()
        self.get_lemma()
        self.noun_tokenize()
        self.output_formatter()

    def remove_stopword(self) -> list:
        temp_result = []

        for i in self.pos_tokens:
            word = i[0]
            pos = i[1]

            if word not in self.stopword and word != pos:
                temp_result.append(i)
            else:
                self.remove_tokens.add(word)

        self.pos_tokens = temp_result
        return temp_result

    def whitespace_tokenize(self):
        """

        :return:
        """
        wt = WhitespaceTokenizer()
        self.whitespace_tokens = wt.tokenize(self.org_sentence)

    def pos_tokenize(self):
        """

        :return:
        """
        token_list = word_tokenize(self.org_sentence)
        self.word_tokens = token_list
        self.pos_tokens = pos_tag(token_list)

    def noun_tokenize(self):
        """

        :return:
        """
        noun_token_list = []
        for word, pos in self.pos_tokens:

            if pos in self.noun_list:
                noun_token_list.append(word)
            else:
                pass
        self.noun_tokens = noun_token_list
        return noun_token_list

    def get_lemma(self) -> list:
        """
        tokenize result를 가지고 원형 뽑아내기???????
        :return:
        """
        lemma_list = []
        for word, pos in self.pos_tokens:
            lemma_pos = self.set_lemma_pos_tag(pos)
            if lemma_pos != '':
                lemma_list.append(self.lemma.lemmatize(word, pos=lemma_pos))
            else:
                lemma_list.append(self.lemma.lemmatize(word))

        self.lemma_tokens = lemma_list
        return lemma_list

    def get_ner(self):
        ner_sentence = ne_chunk(self.pos_tokens)
        self.ner_tree = ner_sentence

    def output_formatter(self):
        temp_dict = dict()
        temp_dict['org_sentence'] = self.org_sentence
        temp_dict['ner_tree'] = self.ner_tree
        temp_dict['whitespace_token'] = self.whitespace_tokens
        temp_dict['pos_token'] = list(map('/'.join, self.pos_tokens))
        temp_dict['noun_token'] = self.noun_tokens
        temp_dict['lemma_token'] = self.lemma_tokens
        temp_dict['stopword_list'] = list(self.remove_tokens)
        temp_dict['sentence_token'] = self.sent_token

        self.tokenize_dict = temp_dict

    def sentence_tokenize(self):
        self.org_sentence = self.org_sentence.replace("\n", ". ")

        self.sent_token = sent_tokenize(self.org_sentence)
        print(">>", self.sent_token)

    @staticmethod
    def __load_noun_pos_list():
        """

        :return:
        """

        pos_list = ['NN', 'NNS', 'NNP', 'NNPS']
        return pos_list

    @staticmethod
    def __load_verb_pos_list():
        """

        :return:
        """
        pos_list = ['VB', 'VBG', 'VBN', 'VBD', 'VBP', 'VBZ']
        return pos_list

    @staticmethod
    def set_lemma_pos_tag(input_pos_tag: str) -> str:
        """

        :param input_pos_tag:
        :return:
        """
        if input_pos_tag.startswith('N'):
            lemma_pos = 'n'
        elif input_pos_tag.startswith('V'):
            lemma_pos = 'v'
        elif input_pos_tag.startswith('J'):
            lemma_pos = 'a'
        elif input_pos_tag.startswith('R'):
            lemma_pos = 'r'
        else:
            lemma_pos = ''

        return lemma_pos


if __name__ == '__main__':
    c = EnParser()

    test_str = """dddddddd.Where
say "hi." to me. '안녕.'이라고 말하지마
Ph.D. dfdfdfdf. we're here"""

    test_str = "The U.S. DEA says hello.PCRE & JavaScript flavors of RegEx are supported. Double bubble disco queen Headed tothe guillotine.What?are?you?Skin as cool as Steve McQueen.. Let me be your killer king.!!It hurts until it stops.we will love until it's not. There's a man on a hill, and I'm watching him with my telescope.. Hello, Mrs.Smith.he got his Ph.D. in Italy."
    test_str = "But they answered: Frighten? Why should any one be frightened by a hat?"

    c.preprocessing_pipeline(test_str)
    temp_dict = c.tokenize_dict

    for k, v in temp_dict.items():
        print(f'{k}: {v}')
