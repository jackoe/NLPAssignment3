# Kerim Celik
# Jack Wines

import nltk
from nltk import word_tokenize
from nltk.util import ngrams
from functools import reduce
from tabulate import tabulate
from nltk.tree import *
from nltk.draw import tree

# returns # items in from_l also in to_l
def overlap(from_l, to_l):
    to_s = set(to_l)
    count = 0
    for item in from_l:
        count += item in to_s
    return count

# concatnates two lists
def listConcat(x, y):
    x.extend(y)
    return x

[x ** 2 for x in range(4, 10)]
# takes words in, outputs CFG-style rules
def formatWordList(words):
    valsAsStrs =['"' + x + '"' for x in words]
    joined = " | ".join(valsAsStrs)
    return joined

# takes in words + tags, yields CFG
def makeBottomPly(tagPossb):
    return [key + ' -> ' + formatWordList(words) for key, words in tagPossb.items()]

# turns the first character lower case
def lowerCaseFirstChar(s):
    if s[0] == 'I' and s[1] == ' ':
        return s
    else:
        return s[0].lower() + s[1:]

# Turns the list of words into sentences
def cleanTokenizedSent(sent):
    return " ".join([wordToWord[wor] for wor in sent])

# Makes the first character upper case
def upperCaseFirstChar(sent):
    return sent[0].upper() + sent[1:]

lines = ["I hate this.",
    "Running is terrible.",
    "Everything is the worst.",
    "Sometimes I feel like I was born with a leak.",
    "Any goodness I started with just slowly spilled out of me.",
    "Now it is all gone.",
    "You did not know me.",
    "Then you fell in love with me.",
    "Now you know me.",
    "I need to go take a shower.",
    "I can not tell if I am crying.",
    "I just spent 7 hours playing with fonts."]

# for s in lines:
#     s.replace("didn't", "did not")

lines = [lowerCaseFirstChar(line.replace('.', '')) for line in lines]

tokenized_sens = [word_tokenize(sen) for sen in lines]

taggedSens = [nltk.pos_tag(word_tokenize(sen)) for sen in lines]

taggedWords = reduce(listConcat, taggedSens, [])

tagPossb = {}
for (word, tag) in taggedWords:
    if tag not in tagPossb:
        tagPossb[tag] = word,
    else:
        words = set(tagPossb[tag])
        words.add(word)
        tagPossb[tag] = tuple(words)

firstPlyRules = "\n".join(makeBottomPly(tagPossb))

higherLevelRules = """
S -> NP VP | RB S
VP -> RB VP | MD VP | VP PP | VBN PP | VBD VP | TO VP | VBP DT | VBP TO VP | VBZ JJ | VBZ DT JJS | VBZ DT VBN | VBP PRP | VBD IN NN | VB DT NN | VB VP | VB PP | VBP VBG | VBD NP | VBP PP
PP -> IN NP | IN PP | PP VP | VBG PP
NP -> NN | PRP | DT NP | NN PRP VBD IN | CD NNS | NNS
"""

rules = higherLevelRules + firstPlyRules
grammar = nltk.CFG.fromstring(rules)

# print('----------------------\n\n\n')
# v = 1
# for sent in tokenized_sens:
#     for tree in nltk.ChartParser(grammar).parse(sent):
#         print(v, sent)
#         tree.draw()
#     v += 1


wordToWord = {"7":"7",
    "this":"esto",
    "the":"el",
    "a":"un",
    "any":"cualquier",
    "all":"todo",
    "like":"como",
    "with":"con",
    "out":"fuera",
    "of":"de",
    "in":"en",
    "with":"con",
    "if":"si",
    "terrible":"terrible",
    "worst":"peor",
    "can":"puede",
    "everything":"todo",
    "leak":"fuga",
    "goodness":"bondad",
    "love":"amor",
    "shower":"ducha",
    "running":"corriendo",
    "hours":"horas",
    "fonts":"fuentes",
    "I":"yo",
    "me":"yo",
    "it":"ello",
    "you":"usted",
    "sometimes":"a veces",
    "just":"solo",
    "slowly":"lentamente",
    "now":"ahora",
    "then":"entonces",
    "not":"no",
    "to":"a",
    "know":"saber",
    "go":"ir",
    "take":"tomar",
    "tell":"decir",
    "was":"era",
    "started":"comenzo",
    "did":"hizo",
    "fell":"cayo",
    "spent":"gastado",
    "crying":"llorando",
    "playing":"jugando",
    "born":"nacido",
    "spilled":"derramado",
    "gone":"ido",
    "hate":"odio",
    "feel":"sentir",
    "know":"saber",
    "need":"necesidad",
    "am":"soy",
    "is":"es"}

googleTranslate = ["Odio esto.",
    "Correr es terrible.",
    "Todo es lo peor.",
    "A veces siento que naci con una fuga.",
    "Cualquier bondad que empece con sólo se derramo fuera de mi.",
    "Ahora todo se ha ido.",
    "No me conoces.",
    "Entonces te enamoraste de mi.",
    "Ahora me conoces.",
    "Necesito ir a banarme.",
    "No puedo decir si estoy llorando.",
    "Acabo de pasar 7 horas jugando con las fuentes."]

unModGoogleTranslate = googleTranslate
googleTranslate = [lowerCaseFirstChar(s.replace('.', '')) for s in googleTranslate]

espn = [cleanTokenizedSent(sent) for sent in tokenized_sens]

bleu = []
for i in range(len(espn)):
    scores = []
    for j in range(1, 5):
        sourceNgrams = list(ngrams(nltk.word_tokenize(espn[i]), j))
        standardNgrams = list(ngrams(nltk.word_tokenize(googleTranslate[i]), j))
        hits = overlap(sourceNgrams, standardNgrams)
        if hits != 0:
            scores.append(hits / len(sourceNgrams))
    if len(scores) != 0:
        bleu.append(sum(scores) / len(scores))
    else:
        bleu.append(0)

tabl = zip(range(1, 13), unModGoogleTranslate, bleu)


prettyTranslatedEspn = [upperCaseFirstChar(sen) for sen in espn]
print(tabulate(zip(range(1,13), prettyTranslatedEspn),
    headers = ('#','Translation')))

print('\n')
print(tabulate(tabl, headers=['#', 'Sentence', 'BLEU Score']))

#print(grammar.productions())
#print([(sen, grammar.check_coverage([y for (x, y) in word_tokenize(sen)])) for sen in lines])
