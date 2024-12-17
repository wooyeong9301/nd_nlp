import re
from collections import Counter


def words(document):
    """ Function to tokenize words """
    return re.findall(r'\w+', document.lower())


test_text = '''
d'Alba dandelions dandelion's dandelion-alive dr.cha as~pos~as, cat, hat, hello halo
'''
print(words(test_text))


all_words = Counter(words(test_text))


def prob(word, N=sum(all_words.values())):
    return all_words[word] / N


def edits_one(word):
    """ Create all edits that are one edit away from 'word' """
    alphabets = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word)+1)]
    deletes = [left + right[1:] for left, right in splits if right]
    inserts = [left + c + right for left, right in splits for c in alphabets]
    replaces = [left + c + right[1:] for left, right in splits for c in alphabets]
    transposes = [left + right[1] + right[0] + right[2:] for left, right in splits if len(right)>1]

    return set(deletes+inserts+replaces+transposes)


def edits_two(word):
    """ Create all edits that are two edits away from 'word' """
    return (e2 for e1 in edits_one(word) for e2 in edits_one(e1))


def known(words):
    """ The subset of 'words' that appear in the 'all_words' """
    return set(word for word in words if word in all_words)


def candidates(word):
    """ Generate possible spelling corrections for word """
    return known([word]) or known(edits_one(word)) or known(edits_two(word)) or [word]


def best(word):
    """ Most probable spelling correction for word """
    return max(candidates(word), key=prob)


def spell_check(word):
    new_word = best(word)
    if new_word != word:
        return 'Did you mean {}?'.format(new_word)
    else:
        return 'Nothing to correct.'

print(spell_check('I want to go home'))