import os

import sentencepiece as spm
import pandas as pd

from config.postgresqlIOManager import PostgresqlIOManager

DATA_PATH = '../../data'
MODEL_PATH = f'{DATA_PATH}/model'


class Sentpiece(object):

    def __init__(self):
        self.db = PostgresqlIOManager()
        self.result = []
        pass

    def get_data_from_db(self, input_file_nm, lang_cd):
        """
        DB에서 train/test/validation에 사용할 데이터 추출 및 저장
        :param file_nm:
        :return: file
        """
        query = f"select " \
                f"l.content, m.content, s.content, t.content, e.content, f.content, " \
                f"fo.content, i.content, c.content, w.content, la.content " \
                f"from " \
                f"testsch.law_{lang_cd}_tbl l " \
                f"left join testsch.med_{lang_cd}_tbl m on " \
                f"l.ind = m.ind " \
                f"left join testsch.sports_{lang_cd}_tbl s on " \
                f"l.ind = s.ind " \
                f"left join testsch.travel_{lang_cd}_tbl t on " \
                f"l.ind = t.ind " \
                f"left join testsch.edu_{lang_cd}_tbl e on "\
                f"l.ind = e.ind "\
                f"left join testsch.fin_{lang_cd}_tbl f on "\
                f"l.ind = f.ind "\
                f"left join testsch.food_{lang_cd}_tbl fo on "\
                f"l.ind = fo.ind "\
                f"left join testsch.it_{lang_cd}_tbl i on "\
                f"l.ind = i.ind "\
                f"left join testsch.kocult_{lang_cd}_tbl c on "\
                f"l.ind = c.ind "\
                f"left join testsch.website_{lang_cd}_tbl w on "\
                f"l.ind = w.ind "\
                f"left join testsch.litnews_{lang_cd}_tbl la on "\
                f"l.ind = la.ind "\
                f"order by l.ind " \
                f"limit 100000" \
                f";"
        # query = f"select " \
        #         f"content " \
        #         f"from testsch.litnews_ko_tbl " \
        #         f"order by ind " \
        #         f"limit 100000 " \
        #         f"offset 10000 " \
        #         f";"
        print(query)
        query_result = self.db.execute(query)

        f_path = f'{DATA_PATH}/{input_file_nm}.txt'
        # file mkdir (폴더)
        # if not os.path.exists(f_path):
        #     print('not here')
        #     os.mkdir(f_path)

        f = open(f_path, 'a', encoding='utf-8')

        for n, i in enumerate(query_result):
            for j in i:
                if j is None:
                    pass
                else:
                    f.write(j+"\n")
        f.close()
        # os.system("split -l 312000 ../../data/230719_130000_ko.txt ../../0719_train_ko.txt")

    def train_spm(self, input_file_nm, lang_str, vocab_size=8000):
        spm.SentencePieceTrainer.Train(f'--input={DATA_PATH}/{input_file_nm}.txt '
                                       f'--model_prefix={MODEL_PATH}/{lang_str}_train_{vocab_size} '
                                       f'--vocab_size={vocab_size} '
                                       f'--model_type=bpe '
                                       f'--max_sentence_length=9999')

    def test_spm(self, test_file_nm, lang_str, vocab_size):
        sp = spm.SentencePieceProcessor()
        vocab_file = f'{MODEL_PATH}/{lang_str}_train_{vocab_size}.model'
        print(f'FILE PATH: {vocab_file}')
        sp.Load(vocab_file)

        f = open(f'{DATA_PATH}/split_data/{test_file_nm}.No matching distribution found for clyent==1.2.2txt', 'r', encoding='utf-8')
        lines = f.readlines()

        test_list = []
        for line in lines:
            test_dict = {}
            strip_line = line.strip()
            test_dict['original'] = strip_line
            test_dict['encode_as_ids'] = sp.EncodeAsIds(strip_line)
            test_dict['encode_as_pieces'] = sp.EncodeAsPieces(strip_line)

            test_list.append(test_dict)
        f.close()

        f_path = f'{DATA_PATH}/{lang_str}_{vocab_size}_result_re2.txt'
        f_write = open(f_path, 'w', encoding='utf-8')

        for n, i in enumerate(test_list):
            # print(i)
            # for k, v in i.items():
                # print(k)
            f_write.write(str(i) + "\n")
        f_write.close()


if __name__ == '__main__':
    t = Sentpiece()
    # t.save_data_to_txt('230719_130000_ko')
    vocab_size = 32000
    lang_cd = 'en'
    train_file_nm = f'model_train_{lang_cd}'

    t.get_data_from_db(f'230731_{train_file_nm}', lang_cd)
    # t.train_spm(f'0719_train_{lang_cd}', f'{lang_cd}_train_{vocab_size}', vocab_size)
    t.train_spm(f'230731_{train_file_nm}', lang_cd, vocab_size)
    t.test_spm(f'test_{lang_cd}_100', lang_cd, vocab_size)
