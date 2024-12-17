import pandas as pd
import spacy
from konlpy.tag import Mecab
from nltk.translate.bleu_score import SmoothingFunction, sentence_bleu
import argparse


# 인자값을 받을 수 있는 인스턴스 생성
parser = argparse.ArgumentParser(description='Please input an excel file including one result sentence and original sentence.')

# 입력받을 인자값 설정 (default 값 설정가능)
parser.add_argument('--file', '-f', type=str)

# args 에 위의 내용 저장
args = parser.parse_args()

# 입력받은 인자값 출력
print("The file you input here.")
print(args.file)

# 데이터 로드, 컬럼명 지정
df = pd.read_excel(args.file, header=0)
df.columns = ['ko_original', 'result']

# bleu_score, Smoothing Function
cc = SmoothingFunction()

# Sentence splitter
mecab = Mecab()


reference = [mecab.morphs(df['ko_original'][0])]
target_text = mecab.morphs(df['result'][0])
score = sentence_bleu(reference, target_text, weights=[1,0,0,0], smoothing_function=cc.method2, auto_reweigh=True)

print("original sentence : ", reference)
print("result sentence : ", target_text)
print("BLEU score : ", score)
