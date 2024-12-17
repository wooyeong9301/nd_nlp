import re

from sentence_splitter import SentenceSplitter as sent_splitter
from nltk.tokenize import sent_tokenize


class SentenceSplitter(object):

    def __init__(self):
        self.split_sentence_list = []

    def sentsplit_pipeline(self, input_str: str, input_language='english', input_lib_type='splitter'):
        """
        lib_type로 문장 분리 라이브러리를 구분지어 진행
        lib_type은 다음과 같은 값을 가짐
        - splitter (default): using sentence_splitter lib
        - nltk: using nltk sent_tokenize lib
        - regex(else): using regex

        :param input_str: 유저 입력 문장
        :param input_language: sentence_splitter, nltk lib에 필요한 매개변수 (default='english')
        :param input_lib_type: 문장분리 사용 라이브러리 선택 (default='splitter')
        :return:
        """

        # input_str = re.sub(r'\n|\s{4}|\t', '\n', input_str)
        # input_str = re.sub(r' +', ' ', input_str)
        # input_str = re.sub(r'\.{2,} ', '...\n', input_str)
        # input_str = re.sub(r'\.?\n', '.\n', input_str)
        # if '.' in input_str:
        #     input_str = input_str.replace('.', '.\n')

        if input_lib_type == 'splitter':
            self.split_sentence_using_lib(input_str, input_language=self.__load_language_code(input_language))
        elif input_lib_type == 'nltk':
            self.split_sentence_using_nltk(input_str, input_language)
        else:
            self.split_sentence(input_str)

    def split_sentence_using_lib(self, input_str: str, input_language: str):
        """
        sentence_splitter 라이브러리를 이용한 문장 분리
        import plit_text_into_sentences로도 사용이 가능하지만,
        현재처럼 import SentenceSplitter 사용을 권장.

        :param input_str: 유저 입력 문장
        :param input_language: sentence_splitter 라이브러리 사용 시 필요한 language value
        :return: self.split_sentence_list
        """

        splitter = sent_splitter(language=self.__load_language_code(input_language))
        split_sentence_list = splitter.split(input_str)

        self.split_sentence_list = split_sentence_list
        # print(f"using lib: {split_sentence_list}")

    def split_sentence_using_nltk(self, input_str: str, input_language: str):
        """
        nltk.sent_tokenize 라이브러리를 이용한 문장 분리

        :param input_str: 유저 입력 문장
        :param input_language: nltk 라이브러리 사용 시 필요한 language value
        :return: self.split_sentence_list
        """

        # input_str = input_str.replace("\n", " ")
        sent_input_str = sent_tokenize(input_str, input_language)
        self.split_sentence_list = sent_input_str
        # print(f"sent: {' / '.join(sent_input_str)}\n\n")

    def split_sentence(self, input_str: str):
        """
        라이브러리가 아닌 정규식을 이용한 문장 분리

        :param input_str: 유저 입력 문장
        :return: self.split_sentence_list
        """

        # reg_pattern3 = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s'
        # reg3 = re.compile(reg_pattern3)
        #
        # input_str = re.sub(reg3, "\n", input_str)
        # self.split_sentence_list = input_str.split('\n')
        # print(f"\n{''.join(input_str)}")

        reg_pattern1 = r'([A-Za-z가-힣]{3,}\.\s?[A-Za-z가-힣]{2,})|(\n)|(\.+\s+)'
        # reg_pattern1 = r'([A-Za-z가-힣]{3,}\.\s?[A-Za-z가-힣]{2,})|(\n)|(\.+)'
        url_pattern = r'(https?:\/\/)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)'

        reg1 = re.compile(reg_pattern1)

        match_list = re.findall(reg1, input_str)
        print(match_list)
        for i in match_list:
            if '.' in i[0]:
                target_word = i[0].split('.')[1]
                input_str = input_str.replace(target_word, f'\n{target_word}')
            else:
                pass

        self.split_sentence_list = input_str.split('\n')

    @staticmethod
    def __load_language_code(language: str) -> str:
        """
        nltk에서 제공하는 언어 값과 sentence_splitter에서 제공하는 언어 값이 다르기 때문에
        이를 맞춰 주기 위한 메소드.

        sentence_splitter에서는 총 24개 언어를 제공하고,
        nltk는 그에 비해 적은 언어를 제공하고 있기 때문에 해당 코드는 nltk를 기준으로 작성 됨.
        (더 많은 언어를 제공하는지에 대해서는 찾아볼 필요가 있음)

        지금은 if ~ else로 개발하였으나,
        이후에는 문서로 읽어서 처리할 수 있도록 바꾸어도 무방할듯 함.

        :param language: (default='english')
        :return: lang_code
        """
        if language == 'english':
            lang_code = 'en'
        elif language == 'czech':
            lang_code = 'cs'
        elif language == 'danish':
            lang_code = 'da'
        elif language == 'dutch':
            lang_code = 'nl'
        elif language == 'finnish':
            lang_code = 'fi'
        elif language == 'french':
            lang_code = 'fr'
        elif language == 'german':
            lang_code = 'de'
        elif language == 'greek':
            lang_code = 'el'
        elif language == 'italian':
            lang_code = 'it'
        elif language == 'norwegian':
            lang_code = 'no'
        elif language == 'polish':
            lang_code = 'pl'
        elif language == 'portuguese':
            lang_code = 'pt'
        elif language == 'russian':
            lang_code = 'ru'
        elif language == 'slovene':
            lang_code = 'sl'
        elif language == 'spanish':
            lang_code = 'es'
        elif language == 'swedish':
            lang_code = 'sv'
        elif language == 'turkish':
            lang_code = 'tr'
        else:
            lang_code = language

        return lang_code


if __name__ == '__main__':

    test_str = """RegExr was created by gskinner.com.Roll over matches or the expression for details.PCRE & JavaScript flavors of RegEx are supported.Validate your expression with Tests mode.Doctor can be spelled as 'Dr.' like Dr.Nam and 'Dr.' means doctor. Philosophy doctor can be spelled as 'Ph.D' like Ph.D Nam. 'Ph.D ghasdf"""

    t = SentenceSplitter()
    t.sentsplit_pipeline(test_str, input_lib_type='nltk')
    n = 1
    for i in t.split_sentence_list:
        print(n, ':', i)
        n += 1
