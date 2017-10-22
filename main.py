import nltk
from functools import reduce

def listConcat(x, y):
    x.extend(y)
    return x



lines = ["I hate this.", 
    "Running is terrible.", 
    "Everything is the worst.", 
    "Sometimes I feel like I was born with a leak.", 
    "Any goodness I started with just slowly spilled out of me.", 
    "Now it is all gone.", 
    "You didn’t know me .", 
    "Then you fell in love with me.", 
    "Now you know me.", 
    "I need to go take a shower.", 
    "I can not tell if I am crying.", 
    "I just spent 7 hours playing with fonts."]

taggedSens = [nltk.pos_tag(sen.split()) for sen in lines]
print(taggedSens)
taggedWords = reduce(listConcat, taggedSens, [])
print(taggedWords)

tagPossb = {}
for (word, tag) in taggedWords:
    if tag not in tagPossb:
        tagPossb[tag] = word
    else:
        words = list(tagPossb[tag])
        words.append(word)
        tagPossb[tag] = tuple(words)

print(tagPossb)

