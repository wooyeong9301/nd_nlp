import os
import re
from bs4 import BeautifulSoup

#


def to_lines(lang):
    f1 = open(f'./system_messages/{lang}_source.txt', 'w')
    get_message = re.compile('(?<=\>)(.*?)(?=\<)')

    for i in range(1, 10):
        f2 = open(f'./system_messages/{lang}/{lang}_{i}.txt', 'r')

        kk = 1

        for line in f2.readlines():
            print(kk, get_message.findall(line))
            kk += 1
            if len(get_message.findall(line)) >= 1:
                text = str(get_message.findall(line)[0])
                text = text.replace('\\n', ' ')
                text = text +'\n'
                f1.write(text)
            #     text += '\n'
            #     f1.write(text)
            #     kk += 1
            else:
                continue

        f2.close()
    f1.close()

    return 'Text to lines Done.'


f1 = open('./system_messages/en_oneline.txt', 'w')
get_message = re.compile('(?<=\>)(.*?)(?=\<)')

for i in range(1, 10):
    f2 = open(f'./system_messages/en/en_{i}.txt', 'r')

    for line in f2.readlines():
        print(get_message.findall(line))
        if len(get_message.findall(line)) >= 1:
            text = str(get_message.findall(line)[0])
            text = text.replace('\\n', ' ')
            f1.write(text)
        else:
            continue

    f2.close()
f1.close()