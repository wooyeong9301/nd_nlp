import fugashi as fu
import pandas as pd
from nltk.translate.bleu_score import sentence_bleu,SmoothingFunction


org = open('data/source.txt').read().splitlines()
result = open('data/result.txt').read().splitlines()
google = open('data/google.txt').read().splitlines()


numsens = len(org)

print("The number of sentences of your file...")
print("org.txt", "result.txt", "google.txt")
print((len(org), len(result), len(google)))


tagger = fu.Tagger()

b_result = []
b_google = []

for i in range(numsens):
    
    orgword = [word.surface for word in tagger(org[i])]
    rword = [word.surface for word in tagger(result[i])]
    gword = [word.surface for word in tagger(google[i])]
    
    b_result.append(round(sentence_bleu([orgword], rword, smoothing_function=SmoothingFunction().method4,), 2))
    b_google.append(round(sentence_bleu([orgword], gword, smoothing_function=SmoothingFunction().method4,), 2))


df = pd.DataFrame(list(zip(b_result, b_google)), columns=["BLEU_result", "BLEU_GOOGLE"])
df.to_csv('data/bleu.csv', sep=',')
