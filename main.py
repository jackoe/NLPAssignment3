# Kerim Celik
# Jack Wines

import nltk
from nltk import word_tokenize
from nltk.util import ngrams
from functools import reduce
from tabulate import tabulate
import nltk.tree
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

# list of sentences to parse
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

# scrub the input sentences to have no capital letters, remove periods
lines = [lowerCaseFirstChar(line.replace('.', '')) for line in lines]
# tokenize the sentences into lists of words
tokenized_sens = [word_tokenize(sen) for sen in lines]
# tag each word token with a part of speech using NLTK's POS tagger
taggedSens = [nltk.pos_tag(word_tokenize(sen)) for sen in lines]
# merges lists of tags into a single list
taggedWords = reduce(listConcat, taggedSens, [])

# creates the set of first ply rules by setting the left side of rules to a
# POS tag and the right side to include all words tagged with that part of speech
tagPossb = {}
for (word, tag) in taggedWords:
    if tag not in tagPossb:
        tagPossb[tag] = word,
    else:
        words = set(tagPossb[tag])
        words.add(word)
        tagPossb[tag] = tuple(words)
firstPlyRules = "\n".join(makeBottomPly(tagPossb))
# manually created grammar rules based on observed POS structure
higherLevelRules = """
S -> NP VP | RB S
VP -> RB VP | MD VP | VP PP | VBN PP | VBD VP | TO VP | VBP DT | VBP TO VP | VBZ JJ | VBZ DT JJS | VBZ DT VBN | VBP PRP | VBD IN NN | VB DT NN | VB VP | VB PP | VBP VBG | VBD NP | VBP PP
PP -> IN NP | IN PP | PP VP | VBG PP
NP -> NN | PRP | DT NP | NN PRP VBD IN | CD NNS | NNS
"""
# merges both sets of rules to create the full rule set, then
# passes it to the grammar
rules = higherLevelRules + firstPlyRules
grammar = nltk.CFG.fromstring(rules)

# allows visualization of the parse trees in separate windows
# not part of assignment, so commented out
# print('----------------------\n\n\n')
# v = 1
# for sent in tokenized_sens:
#     for tree in nltk.ChartParser(grammar).parse(sent):
#         print(v, sent)
#         tree.draw()
#     v += 1

# word to word transduction lexicon given by assignment, in dictionary form
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

# list of sentences translated through Google Translate (gold standard), also given
unModGoogleTranslate = ["Odio esto.",
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

# scrub the gold standard sentences the same way the input sentences were scrubbed
googleTranslate = [lowerCaseFirstChar(s.replace('.', '')) for s in unModGoogleTranslate]
# translate the english sentences to spanish by looking up the words in the
# lexicon, changing them to spanish, then connecting them into a sentence
espn = [cleanTokenizedSent(sent) for sent in tokenized_sens]

# calculate the BLEU score for each sentence as the average of the
# BLEU-1, BLEU-2, BLEU-3, and BLEU-4 scores
bleu = []
for i in range(len(espn)):
    scores = []
    for j in range(1, 5):
        sourceNgrams = list(ngrams(nltk.word_tokenize(espn[i]), j))
        standardNgrams = list(ngrams(nltk.word_tokenize(googleTranslate[i]), j))
        hits = overlap(sourceNgrams, standardNgrams)
        if hits != 0:
            scores.append(hits / len(sourceNgrams))
    # ignore any BLEU-n score if it is 0, and reduce the
    # denominator of the average accordingly
    if len(scores) != 0:
        bleu.append(sum(scores) / len(scores))
    else:
        bleu.append(0)

# create a table for printing out the BLEU scores nicely
prettyTranslatedEspn = [upperCaseFirstChar(sen) + '.' for sen in espn]
tabl = zip(range(1, 13), prettyTranslatedEspn, bleu)

# Pretty print our translations
print(tabulate(tabl, headers=['#', 'Our Translation', 'BLEU Score']))

#print(grammar.productions())
#print([(sen, grammar.check_coverage([y for (x, y) in word_tokenize(sen)])) for sen in lines])
