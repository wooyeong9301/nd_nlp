import abc
from collections import OrderedDict


class TokenizeTemplate(abc.ABC):

    def __init__(self):
        self.word_tokens = []

        self.org_sentence = ''
        self.ner_tree = ''
        self.whitespace_tokens = []
        self.pos_tokens = []
        self.lemma_tokens = []
        self.noun_tokens = []
        self.sent_token = []
        self.remove_tokens = set()

        self.tokenize_dict = OrderedDict
        pass

    def set_output_default(self):
        """

        :return: OrderedDict
        """
        temp_dict = dict()
        temp_dict['org_sentence'] = ''
        temp_dict['ner_tree'] = ''
        temp_dict['pos_token'] = []
        temp_dict['noun_token'] = []
        temp_dict['whitespace_token'] = []
        temp_dict['lemma_token'] = []
        temp_dict['stopword_list'] = []
        temp_dict['sentence_token'] = []

        self.tokenize_dict = temp_dict

    @abc.abstractmethod
    def remove_stopword(self):
        """
        불용어 제거
        """
        pass

    @abc.abstractmethod
    def whitespace_tokenize(self):
        """
        Whitespace 토큰화 및 결과 저장을 위한 함수
        """
        pass

    @abc.abstractmethod
    def pos_tokenize(self):
        pass

    @abc.abstractmethod
    def noun_tokenize(self):
        pass

    @abc.abstractmethod
    def get_lemma(self):
        pass

    @abc.abstractmethod
    def get_ner(self):
        pass