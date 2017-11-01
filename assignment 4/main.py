# Kerim Celik
# Jack Wines
from math import sqrt
from tabulate import tabulate
from random import shuffle
from nltk import word_tokenize
from functools import reduce

def dotProduct(vec1, vec2):
    return sum([x * y for x,y in zip(vec1, vec2)])

def magnitude(vec):
    return sqrt(sum([x ** 2 for x in vec]))

def normalize(vec):
    vecMagnitude = magnitude(vec)
    return [x / vecMagnitude for x in vec]

def calc_cosine_similarity(vec1, vec2):
    return abs(dotProduct(normalize(vec1), normalize(vec2))
)
def parseLine(line):
    l = line.split()
    return [l[0]] + [float(x) for x in l[1:]]


def makePairs(lines):
    lines = [parseLine(line) for line in lines]
    halfway = len(lines) // 2
    pairs = zip(lines[:halfway], lines[halfway:])
    return list(pairs)


def get50Pairs(fileName):
    pairs = None
    with open(fileName, 'r') as f:
        lines = list(f)
        return makePairs(lines)

def snd(t):
    (_, t2) = t
    return t2

def output_cosine_similarity(vecPairs):
    wordPairs = []
    scores = []
    for tup in vecPairs:
        wordPairs.append((tup[0][0], tup[1][0]))
        scores.append(calc_cosine_similarity(tup[0][1:], tup[1][1:]))
    table = list(zip(wordPairs, scores))
    table.sort(key = snd, reverse = True)
    print(tabulate(table, headers=["Word Pair", "Cosine Similarity"]))

def tokenize(sentence):
    return word_tokenize(sentence.replace(",", "").replace(".", " "))

def addToMultiset(multi, toAdd):
    if toAdd not in multi:
        multi[toAdd] = 1
    else:
        multi[toAdd] += 1
    return multi

def multisetGet(multi, val):
    if val not in multi:
        return 0;
    else:
        return multi[val]

def makeMultiSet(l):
    return reduce(addToMultiset, l, {})

def makeSentenceVector(sentenceMultiSet, allWords):
    return [multisetGet(sentenceMultiSet, word) for word in allWords]


def getInputVectorsFromSentences(fileName):
    with open(fileName, 'r') as f:
        cleanSentences = [sentence.replace("\n","").lower() for sentence in f]
        shuffle(cleanSentences)
        sentences = scleanSentences[:50]
        tokenizedSentences = [tokenize(sentence) for sentence in sentences]
        print(tokenizedSentences)
        sentenceMultiSets = [makeMultiSet(sentence) for sentence in tokenizedSentences]
        allWords = set(reduce(lambda x,y: x+y, tokenizedSentences))
        print(allWords)
        sentenceVectors = [[sentence] + makeSentenceVector(sentenceMultiset, allWords)
                for sentence, sentenceMultiset, tokenizedSentence in
                zip(sentences, sentenceMultiSets, tokenizedSentences)]
        return sentenceVectors








#output_cosine_similarity(get50Pairs('even50morePairs.txt'))
sentenceVectors = getInputVectorsFromSentences('Assignment_4_Input.txt')
vecPairs = zip(sentenceVectors[:25], sentenceVectors[25:])
output_cosine_similarity(vecPairs)

