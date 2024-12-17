# Standardizing Attribute Names 과정 필요.
# Save and load with sqlite3
from textacy.preprocessing.resources import RE_URL
from textacy.preprocessing.replace import urls as textacy_urls
from spacy import displacy
import textacy
import textacy.preprocessing as tprep
import re
import html
import spacy
import fasttext

fasttext.FastText.eprint = lambda x: None


def check_impurity(text, min_len=10):
    """Returns the share of suspicious characters in a text"""
    re_suspicious = re.compile(r'[&#<>{}\[\]\\]')
    if text == None or len(text) < min_len:
        return 0
    else:
        return len(re_suspicious.findall(text))/len(text)


def clean(text):
    """Remove moise with regular expressions"""
    text = html.unescape(text) # html escapes
    text = re.sub(r'<[^<>]*>', ' ', text) # tags
    text = re.sub(r'\[([^\[\]]*)\]\([^\(\)]*\)', r'\1', text) # markdown URLs
    text = re.sub(r'\[[^\[\]]*\]', ' ', text) # text or code in brackets
    # standalone seq of specials, matches &# but not #cool
    text = re.sub(r'(?:^|\s)[&#<>{}\[\]+|\\:-]{1,}(?:\s|$)', ' ', text)
    # standalone seq of hyphens like --- or ==
    text = re.sub(r'(?:^|\s)[\-=\+]{2,}(?:\s|$)', ' ', text)
    text = re.sub(r'\s+', ' ', text) # seq of white spaces
    return text.strip()


def normalize(text):
    text = tprep.normalize.hyphenated_words(text)
    text = tprep.normalize.quotation_marks(text)
    text = tprep.normalize.unicode(text)
    text = tprep.remove.accents(text)
    return text


def extract_lemmas(doc, **kwargs):
    return [t.lemma_ for t in textacy.extract.words(doc, **kwargs)]


def extract_noun_phrases(doc, pre_pos=['NOUN'], sep='_'):
    patterns = []
    for pos in pre_pos:
        patterns.append(f"POS:{pos} POS:NOUN:+")
    spans = textacy.extract.matches.token_matches(doc, patterns=patterns)
    return [sep.join([t.lemma_ for t in s]) for s in spans]


def extract_entities(doc, include_types=None, sep='_'):
    ents = textacy.extract.entities(doc, include_types=include_types,
                                    exclude_types=None, drop_determiners=True,
                                    min_freq=1)
    return [sep.join([t.lemma_ for t in e]) + ' :: ' + e.label_ for e in ents]


def extract_total(doc):
    return {'lemmas' : extract_lemmas(doc, exclude_pos=['PART', 'PUNCT', 'DET', 'PRON',
                                                        'SYM', 'SPACE'], filter_stops=False),
            'adjs_verbs' : extract_lemmas(doc, include_pos=['ADJ', 'VERB']),
            'nouns' : extract_lemmas(doc, include_pos=['NOUN', 'PROPN']),
            'noun_phrases' : extract_noun_phrases(doc, ['NOUN']),
            'adj_noun_phrases' : extract_noun_phrases(doc, ['ADJ']),
            'entities' : extract_entities(doc, ['PERSON', 'ORG', 'GPE', 'LOC'])}


def lang_detection(text, threshold=0.8, default='en'):
    lang_model = fasttext.load_model('lid.176.ftz')
    # if len(text) < 10: return default

    text = text.replace('\n', ' ')
    labels, probs = lang_model.predict(text)
    print(labels, probs)
    lang = labels[0].replace('__label__', '')
    prob = probs[0]

    if len(text) < 15 or prob >= threshold:
        return lang
    else : return default


token_map = {'U.S.': 'United_States', 'L.A.': 'Los_Angeles'}

def token_normalize(tokens):
    temp = []
    for t in tokens:
        if str(t) in token_map.keys():
            temp.append(token_map[str(t)])
        else:
            temp.append(None)
    return temp
    # return [token_map.get() for t in tokens]


text = """
James O'Neill, chairman of World Cargo Inc, lives in San Francisco
After viewing the [PINKIEPOOL Trailer](https://www.youtu.be/watch?v=ieHRoHUg)
it got me thinking about the best match ups.
<lb>Here's my take:<lb><lb>[](/sp)[](/ppseesyou) Deadpool<lb>[](/sp)[](/ajsly)
Captain America<lb>
The café “Saint-Raphaël” is loca-\nted on Côte dʼAzur.
2019-08-10 23:32: @pete/@louis - I don't have a well-designed
solution for today's problem. The code of module AC68 should be -1.
Have to think a bit... #goodnight ;-) 😩😬
"""
nlp = spacy.load('en_core_web_sm')
# text = ['estudiante', '안녕', 'hi', 'hola', 'school', 'buenos', 'My name is 우영.', 'tres']
# print(*[lang_detection(t) for t in (text)])
# print(*[t.pos_ for t in nlp("ASDFGWE")])

ww = token_normalize(nlp("L.A. is the city in the U.S."))
# print(token_map.keys())
print(ww)