# Kerim Celik
# Jack Wines
from math import sqrt
from tabulate import tabulate
from random import shuffle
from nltk import word_tokenize
from functools import reduce

# return the dot product of two specified vectors
def dotProduct(vec1, vec2):
    return sum([x * y for x,y in zip(vec1, vec2)])

# get the magnitude of the passed vector
def magnitude(vec):
    return sqrt(sum([x ** 2 for x in vec]))

# normalize the passed vector
def normalize(vec):
    vecMagnitude = magnitude(vec)
    return [x / vecMagnitude for x in vec]

# calculate cosine similarity between two specified vectors
def calc_cosine_similarity(vec1, vec2):
    return abs(dotProduct(normalize(vec1), normalize(vec2)))

# used to parse the vector bank, converts all values in a vector into floats
# from strings except the string representing the word
def parseLine(line):
    l = line.split()
    return [l[0]] + [float(x) for x in l[1:]]

# makes pairs of word vectors to compare with cosine similarity function
def makePairs(lines):
    lines = [parseLine(line) for line in lines]
    halfway = len(lines) // 2
    pairs = zip(lines[:halfway], lines[halfway:])
    return list(pairs)

# reads a file of vectors and returns a list of vector-pairs as tuples
def get50Pairs(fileName):
    with open(fileName, 'r') as f:
        lines = list(f)
        return makePairs(lines)

# gets the second item of the specified tuple
def snd(t):
    (_, t2) = t
    return t2

# given a list of vector pairs, calculate the cosine similarity between all
# pairs, then print out a table with those pairings and their scores
def output_cosine_similarity(vecPairs):
    wordPairs = []
    scores = []
    for tup in vecPairs:
        wordPairs.append((tup[0][0], tup[1][0]))
        scores.append(calc_cosine_similarity(tup[0][1:], tup[1][1:]))
    table = list(zip(wordPairs, scores))
    table.sort(key = snd, reverse = True)
    print(tabulate(table, headers=["Pairing", "Cosine Similarity"]))

# removes a specific string from within another passed string
def removeFromStr(theStr, toRemove):
    return theStr.replace(toRemove, '')

# tokenize the words of a sentence using nltk library
def tokenize(sentence):
    return word_tokenize(reduce(removeFromStr, ",.\"'!?", sentence))

# checks if an item is in a dictionary
# increment the associated counter if it is, add it to dict if not
def addToMultiset(multi, toAdd):
    if toAdd not in multi:
        multi[toAdd] = 1
    else:
        multi[toAdd] += 1
    return multi

# get the counter for a specific key in a dictionary
def multisetGet(multi, val):
    if val not in multi:
        return 0;
    else:
        return multi[val]

#
def makeMultiSet(l):
    return reduce(addToMultiset, l, {})

#
def makeSentenceVector(sentenceMultiSet, allWords):
    #print(sentenceMultiSet)
    return [multisetGet(sentenceMultiSet, word) for word in allWords]

#
def getInputVectorsFromSentences(fileName):
    with open(fileName, 'r') as f:
        sentences = [sentence.replace("\n", "") for sentence in f]
        shuffle(sentences)
        sentences = sentences[:50]
        cleanSentences = [sentence.lower() for sentence in sentences]
        tokenizedSentences = [tokenize(sentence) for sentence in cleanSentences]
        sentenceMultiSets = [makeMultiSet(sentence) for sentence in tokenizedSentences]
        allWords = set(reduce(lambda x,y: x+y, tokenizedSentences))
        # print(sentences)
        sentenceVectors = [[sentence] + makeSentenceVector(sentenceMultiset, allWords)
                for sentence, sentenceMultiset, tokenizedSentence in
                zip(sentences, sentenceMultiSets, tokenizedSentences)]
        return sentenceVectors



output_cosine_similarity(get50Pairs('even50morePairs.txt'))
sentenceVectors = getInputVectorsFromSentences('Assignment_4_Input.txt')
vecPairs = zip(sentenceVectors[:25], sentenceVectors[25:])
print('\n')
output_cosine_similarity(vecPairs)
