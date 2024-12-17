import sys
import os

from collections import OrderedDict

import spellchecker as sc
import truecase as tc


class spellChecker(object):

    def __init__(self):
        self.spell = sc
        self.spchecker = None

        self.target_str = ''
        self.check_sentence_list = []
        self.misspell_word_list = []
        self.changed_sentence = ''
        self.error_word_list = []
        self.res_sentence = ''

        self.output_dict = OrderedDict()

    def spellcheck_pipeline(self, input_str: str, input_language='en'):
        """
        스펠링 체크 파이프라인

        1. 사용자 입력 값 가져오기 (self.get_sentence_list)
        2. 스펠링 체크 (self.check_spell)
        3. 올바른 문장 추출 (self.get_correct_sentence)
        4. 올바르게 수정된 문장을 가지고 capitalization 진행 (self.capitalization)
        5. 프로세스 모든 결과 값이 저장 된 딕셔너리 생성 (self.get_output_dict)

        :param input_str: 입력값
        :param input_language: 스펠링 체크 라이브러리 부를 때 필요한 값.(default=en)
        :return:
        """
        self.spchecker = sc.SpellChecker(language=input_language)
        self.get_sentence_list(input_str)
        self.check_spell()
        self.get_correct_sentence()
        self.capitalization()
        self.get_output_dict()

    def get_sentence_list(self, input_str: str):
        """
        spellChecker input에 맞도록 수정하여 리스트 반환.

        현재는 두가지 타입을 기준으로 작성되어있으나,
        이후에 또 다른 타입에 관련하여 개발 예정

        list type의 경우 list 그대로를 읽어서 넘겨줌.
        -> check_spell 단계에서 리스트를 읽어서 체크하기 때문에 그대로 넘겨줘도 괜찮을듯?

        :param input_str: user input(str)
        :return: self.check_sentence_list
        """

        self.target_str = input_str

        if self.target_str == "" or self.target_str == []:
            print(f'enter sentence.')
        else:
            if type(self.target_str) == str:
                self.check_sentence_list = self.target_str.split(' ')
            elif type(self.target_str) == list:
                self.check_sentence_list = self.target_str
            else:
                print(f'check type of sentence: {type(self.target_str)}')

    def check_spell(self):
        """
        리스트로 반환 된 사용자 입력 값을 사용하여 스펠링 체크
        만약 수정이 필요한 단어가 포함된 경우 해당 단어를 misspell_word_list에 추가.
        :return: self.misspell_word_list
        """

        misspell_list = []
        if len(self.check_sentence_list) > 1:
            for words in self.check_sentence_list:
                if not words == []:
                    check_words = self.spchecker.unknown(words.split(' '))
                    misspell_list.extend(check_words)
                else:
                    pass
        else:
            misspell_list = self.spchecker.unknown(self.check_sentence_list)

        self.misspell_word_list = misspell_list

    def get_correct_sentence(self):
        """
        올바른 스펠링을 가진 단어를 찾고, input_sentence에서 틀린 부분을 치환.

        만약 올바른 스펠링 후보가 없다면,
        기존에 입력 받은 단어를 그대로 두고, error_word_list에 단어 append.
        :return: self.changed_sentence
        """
        error_word_list = []
        org_sentence_list = self.check_sentence_list

        for words in org_sentence_list:
            if words.lower() in self.misspell_word_list:
                correct_word = self.spchecker.correction(words)

                if correct_word is not None:
                    org_sentence_list = [sub.replace(words, self.spchecker.correction(words))
                                         for sub in org_sentence_list]
                else:
                    error_word_list.append(words)

            else:
                pass
        self.changed_sentence = ' '.join(org_sentence_list)
        self.error_word_list = error_word_list

        # print(f'error_word: {",".join(error_word_list)}')
        # print(f'org_sentence = {" ".join(self.check_sentence_list)}\nchange_sentence = {self.changed_sentence} ')

    def capitalization(self):
        """
        spell check 완료 된 문장 capitalization 진행.

        :return: self.res_sentence
        """
        self.res_sentence = tc.get_true_case(self.changed_sentence)

    def get_output_dict(self):
        """
        모든 프로세스를 진행한 결과 값 저장.
        :return: self.output_dict
        """
        self.output_dict['org_input'] = self.target_str
        self.output_dict['sentence_list'] = self.check_sentence_list
        self.output_dict['misspell_word_list'] = self.misspell_word_list
        self.output_dict['changed_sentence'] = self.changed_sentence
        self.output_dict['error_word_list'] = self.error_word_list
        self.output_dict['res_sentence'] = self.res_sentence

    # @staticmethod
    # def __set_output_format():
    #     output_dict = OrderedDict()
    #
    #     output_dict['org_input'] = ''
    #     output_dict['sentence_list'] = []
    #     output_dict['misspell_word_list'] = []
    #     output_dict['changed_sentence'] = ''
    #     output_dict['error_word_list'] = []
    #     output_dict['res_sentence'] = ''
    #
    #     return output_dict


if __name__ == '__main__':
    t = spellChecker()

    target_str = ["somteThing is HAppennuing here", "HeLlLo"]
    target_str = "somteThItng is HAppennuing hereeee. heldooo"

    t.spellcheck_pipeline(target_str)
    for k, v in t.output_dict.items():
        print(f'{k}: {v}')
