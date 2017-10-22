import nltk
from nltk import word_tokenize
from functools import reduce

def listConcat(x, y):
    x.extend(y)
    return x

[x ** 2 for x in range(4, 10)]

def formatWordList(words):
    valsAsStrs =['"' + x + '"' for x in words]
    joined = " | ".join(valsAsStrs)
    return joined

def makeBottomPly(tagPossb):
    return [key + ' -> ' + formatWordList(words) for key, words in tagPossb.items()]

def lowerCaseFirstCharacter(s):
    if s[0] == 'I' and s[1] == ' ':
        return s
    else:
        return s[0].lower() + s[1:]

lines = ["I hate this.", 
    "Running is terrible.", 
    "Everything is the worst.", 
    "Sometimes I feel like I was born with a leak.", 
    "Any goodness I started with just slowly spilled out of me.", 
    "Now it is all gone.", 
    "You didn't know me.", 
    "Then you fell in love with me.", 
    "Now you know me.", 
    "I need to go take a shower.", 
    "I can not tell if I am crying.", 
    "I just spent 7 hours playing with fonts."]

lines = [lowerCaseFirstCharacter(line.replace('.', '')) for line in lines]

tokenized_sens = [word_tokenize(sen) for sen in lines]

taggedSens = [nltk.pos_tag(word_tokenize(sen)) for sen in lines]
#print(taggedSens)
taggedWords = reduce(listConcat, taggedSens, [])
#print(taggedWords)

for sent in taggedSens:
    print(sent)

tagPossb = {}
for (word, tag) in taggedWords:
    if tag not in tagPossb:
        tagPossb[tag] = word,
    else:
        words = set(tagPossb[tag])
        words.add(word)
        tagPossb[tag] = tuple(words)

# get rid of the period because it doesn't matter
# tagPossb.pop('.', None)

firstPlyRules = "\n".join(makeBottomPly(tagPossb))

#print(firstPlyRules)


higherLevelRules = """
S -> NP VP | RB S | S VP | VP | S PP
VP -> MD VB | MD VP | VBN PP | VBD VP | VP VB PP | TO VP | VBP PP | VBP DT | VBP S | VBZ JJ | VBZ DT JJS | VBZ DT VBN | VBP PRP | VBD IN NN | VB DT NN | VB VP | VBP VBG | RB VP | VBD NP | VBG PP
VBD -> VBD RB | RB VBD
PP -> IN NP | IN S | IN PP | IN NNS
NP -> NN | DT NN | DT NNS | PRP | DT JJ NN | VBG | DT NP | NN PRP VBD IN | CD NNS
MD -> MD RB
"""
rules = higherLevelRules + firstPlyRules

grammar = nltk.CFG.fromstring(rules)

print('----------------------\n\n\n')
for sent in tokenized_sens:
    print(sent)
    for tree in nltk.ChartParser(grammar).parse(sent):
        print(tree)



#print(grammar.productions())
#print([(sen, grammar.check_coverage([y for (x, y) in word_tokenize(sen)])) for sen in lines])
