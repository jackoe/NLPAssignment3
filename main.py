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
    "You did not know me.",
    "Then you fell in love with me.",
    "Now you know me.",
    "I need to go take a shower.",
    "I can not tell if I am crying.",
    "I just spent 7 hours playing with fonts."]

# for s in lines:
#     s.replace("didn't", "did not")

lines = [lowerCaseFirstCharacter(line.replace('.', '')) for line in lines]

tokenized_sens = [word_tokenize(sen) for sen in lines]

taggedSens = [nltk.pos_tag(word_tokenize(sen)) for sen in lines]
#print(taggedSens)
taggedWords = reduce(listConcat, taggedSens, [])
#print(taggedWords)

#for sent in taggedSens:
    #print(sent)

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

#print('----------------------\n\n\n')
#for sent in tokenized_sens:
    #print(sent)
    #for tree in nltk.ChartParser(grammar).parse(sent):
        #print(tree)


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
    "A veces siento que nací con una fuga.",
    "Cualquier bondad que empecé con sólo se derramó fuera de mí.",
    "Ahora todo se ha ido.",
    "No me conoces.",
    "Entonces te enamoraste de mi.",
    "Ahora me conoces.",
    "Necesito ir a bańarme.",
    "No puedo decir si estoy llorando.",
    "Acabo de pasar 7 horas jugando con las fuentes."]


espn = [" ".join([wordToWord[wor] for wor in sent]) for sent in tokenized_sens]
espn = [s[0].upper() + s[1:] + '.' for s in espn]
print(espn)
#print(grammar.productions())
#print([(sen, grammar.check_coverage([y for (x, y) in word_tokenize(sen)])) for sen in lines])
