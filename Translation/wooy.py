import torch
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from nltk.translate.bleu_score import corpus_bleu
import sentencepiece
import pickle

# def translation(source, target, text):
#     """
#
#     :type text: str
#     """
#     print(f'Source language : {source.upper()}, Target language : {target.upper()}')
#     # print('List of available models :', torch.hub.list('pytorch/fairseq'))
#
#     model = torch.hub.load('pytorch/fairseq', 'transformer.wmt19.en-ru',
#                            checkpoint_file='model1.pt:model2.pt:model3.pt:model4.pt',
#                            tokenizer='moses', bpe='fastbpe')
#     # torch.save(model, '/home/qwer/.cache/torch/hub/pytorch_fairseq_main/ttttttt')
#     #
#     # model = torch.load('/home/qwer/.cache/torch/hub/pytorch_fairseq_main/ttttttt')
#
#     # en2fr.eval()
#     return model.translate(str(text))
#
#
# print(translation('en', 'ru', text='hello'))


# 번역된 내용 저장 russian

en_source = list(line.replace('\n', '') for line in open(f'../Data/system_messages/en_source.txt').readlines())


def save_translated(source):
    model = torch.hub.load('pytorch/fairseq', 'transformer.wmt19.en-ru',
                           checkpoint_file='model1.pt:model2.pt:model3.pt:model4.pt',
                           tokenizer='moses', bpe='fastbpe')

    target = model.translate(source)

    with open(f'../Data/system_messages/ru_translated.txt', 'w') as fw:
        for _ in target:
            line = _+'\n'
            fw.write(line)

    translated = list()
    not_translated = list()

    f1 = open('../Data/system_messages/ru_translated.txt', 'w')
    f2 = open('../Data/system_messages/ru_not_translated.txt', 'w')
    for a, b in zip(target, source):
        line = a + '\n'
        if a == b:
            not_translated.append(a)
            f1.write('\n')
            f2.write(line)
        else:
            translated.append(a)
            f1.write(line)

    f1.close()
    f2.close()
    print('Saved the result of translation.')

    return translated, not_translated


# txt 파일의 문장을 토큰리스트로 바꾸어 저장
# def to_tokens(lang):
#     source = open(f'../Data/system_messages/{lang}_source.txt')
#     ref = list(map(lambda x: x.split(), list(line.replace('\n', '') for line in source.readlines())))
#     source.close()
#
#     return ref

# save_translated(en_source)

temp1 = []
temp2 = []
temp = open(f'../Data/system_messages/ru_reference.txt')
reference = list(map(lambda x: x.split(), list(line.replace('\n', '') for line in temp.readlines())))
temp.close()
temp = open(f'../Data/system_messages/ru_translated.txt')
candidate = list(map(lambda x: x.split(), list(line.replace('\n', '') for line in temp.readlines())))
temp.close()

#
# scores = []
# for cand, ref in zip(candidate, reference):
#
#
# # print(len(scores), scores)
#
# whole_score = corpus_bleu(reference, target, smoothing_function=SmoothingFunction().method1)
# print(whole_score)


print(sentence_bleu([['Традиционные', 'hello']], ['Традиционный', 'hello'], weights=(1, 0, 0, 0),
                    smoothing_function=SmoothingFunction().method4, auto_reweigh=True))
print('test1 :', sentence_bleu(['word'], ['word']))
print('test2 :', sentence_bleu([['word']], ['word']))
print('test3 :', sentence_bleu(['word'], ['word'], weights=(1, 0, 0, 0)))
print('test4 :', sentence_bleu([['word']], ['word'], weights=(1, 0, 0, 0)))
print('test5 :', sentence_bleu(['This is a new world.'.lower().split()], ['a', 'new', 'this', 'is', 'world.'], weights=(1, 0, 0, 0)))
print('test6 :', sentence_bleu([['안녕하세요', '반갑습니다', '오늘은', '월요일입니다']], ['안녕하세요', '오늘은', '월요일입니다'], weights=(0.5, 0.5, 0, 0)))
print('test7 :', sentence_bleu([['안녕하세요', '오늘은', '월요일입니다']], ['안녕하세요', '반갑습니다', '오늘은', '월요일입니다'], weights=(1, 0, 0, 0)))
print('test8 :', sentence_bleu([['안녕하세요']], ['안녕하세요'], weights=(1, )))
print('test9 :', sentence_bleu([['안녕하세요', '아니요', '네']], ['안녕하세요']))
print('test10 :', sentence_bleu([list(_.lower() for _ in ['Hello'])], ['hello'], weights=(1, 0, 0, 0)))

# enru = torch.hub.load('pytorch/fairseq', 'transformer.wmt19.en-ru',
#                       checkpoint_file='model1.pt:model2.pt:model3.pt:model4.pt',
#                       tokenizer='moses', bpe='fastbpe')


# print('not translated :', failed)
# print('Translated :', result)


# BLEU 스코어
# tokenization
# reference = to_tokens('en')
# with open('../Data/system_messages/en_tokens.pickle', 'wb') as fw:
#     pickle.dump(reference, fw)

