import re
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk import pos_tag
#
# datapath = '/home/qwer/Desktop/ndsoft/ai/Data'
#
# def words(document):
#     """ Function to tokenize words """
#
#     return re.findall(r"'t|i'd|'ll|mr.|ms.|mrs.|ph.d|dr.|\w+", document.lower())
#
# test = "psychologist.so Dr.Aala Dr. cha (El-Khani) shares her work supporting -- and learning from -- refugee in 2011. country?How " \
#        "I'm going to."
#
# print(words("He doesn't investigated --the-- case with great care, for Ph.D Dr. Roylott's conduct had long been notorious, No, she was in her night-dress"))
# print(word_tokenize("He doesn't investigated --the-- case with great care, for Ph.D Dr. Roylott's conduct had long been notorious, No, she was in her night-dress"))
#
# test = "Edit the Expression & Text to see matches.Roll over matches or the expression for details.PCRE & JavaScript flavors of RegEx are supported.Validate your expression with Tests mode.Doctor can be spelled as 'Dr.' like Dr.Nam and 'Dr.' means doctor. Philosophy doctor can be spelled as 'Ph.D' like Ph.D Nam."
# # Hi.I know you. Dr.nam Ph.D nam
# # graph.Doctor said
# test_str = """RegExr was created by gskinner.com.Roll over matches or the expression for details.PCRE & JavaScript flavors of RegEx are supported.Validate your expression with Tests mode.Doctor can be spelled as 'Dr.' like Dr.Nam and 'Dr.' means doctor. Philosophy doctor can be spelled as 'Ph.D' like Ph.D Nam. 'Ph.D ghasdf"""
#
#
# print(test_str.replace('.', '.\n'))

input_text = "The U.S. DEA says hello.PCRE & JavaScript flavors of RegEx are supported. Double bubble disco queen Headed tothe guillotine.What?are?you?Skin as cool as Steve McQueen.. Let me be your killer king.!!It hurts until it stops.we will love until it's not.There’s a man on a hill, and I’m watching him with my telescope..Hello, Mrs.Smith.he got his Ph.D. https://translate.google.com/?sl=en&tl=ko&text=he%20got%20his%20PhD&op=translate"


print(sent_tokenize(input_text))

wtl = word_tokenize(input_text)
print(wtl)
print(pos_tag(wtl))

for a,b in pos_tag(wtl):
    if b == 'NNP':
        print(f'word : {a}, pos : {b}')
    else:
        continue



url_pattern = r"(https?:\/\/)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)"
acronym_pattern = r"([A-Z]\.?){2,}"
test = "가위 U.S. U.S.A. 보"
acr_list = re.findall(r"([A-Z\.?]{2,})", test)
print(acr_list)
# test = re.sub('##ACR##', '{}', test)
# print(test.format('바위'))


# input_text = re.sub(acronym_pattern, '##ACR##', input_text)
input_text = re.sub(url_pattern, "##URL##", input_text)
input_text = re.sub(r'\?+ ?', '#?#. ', input_text)
input_text = re.sub(r'!+ ?', '#!#. ', input_text)
print(input_text)


def get_dot_index(text):
    dot_index = []
    i = 0
    for i in range(1, len(text)-1):
        # if (text[i] == '!' or '?'):
        #

        if text[i] == '.':
            if i >= 2 and text[i-2:i] == 'Ph' and text[i+1] == 'D':
                continue
            elif i >= 2 and text[i-2:i] == 'Dr':
                continue
            elif text[i+1].isupper():
                dot_index.append(i)
            else:
                continue
    return dot_index


def insert_space(text):
    dot_index = get_dot_index(text)
    j = 1
    for idx in dot_index:
        text = text[:idx+j] + ' ' + text[idx+j:]
        j += 1

    return text


def sentence_split(text):
    # sentence_list = []
    text = insert_space(text)
    text = re.sub(r'Dr\.', '##DR##', text)
    text = re.sub(r'Ph\.D\.?', '##PH##', text)
    text = re.sub(r'#!#', '!', text)
    text = re.sub(r'#\?#', '?', text)
    sentence_list = str(text).split('. ')

    print('SL :', sentence_list)

    # for sentence in sentence_list:
    #     if '?' in sentence:
    #         temp = sentence.split('?')
    #         print('t? :', temp)

    restored = []
    for sentence in sentence_list:
        if (sentence[-1] != '?') and (sentence[-1] != '!'):
            sentence += '.'
        sentence = sentence.replace('##DR##', 'Dr.')
        sentence = re.sub(r'##PH##', 'Ph.D.', sentence)
        restored.append(sentence)

    return restored


i = 0
for _ in sentence_split(input_text):
    print(i, ":", _)
    i += 1


print(sent_tokenize(input_text))

