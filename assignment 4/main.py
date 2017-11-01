# Kerim Celik
# Jack Wines
from math import sqrt
from tabulate import tabulate

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

def get50Pairs(fileName):
    pairs = None
    with open(fileName, 'r') as f:
        lines = list(f)
        lines = [parseLine(line) for line in lines]
        halfway = len(lines) // 2
        print(halfway)
        pairs = zip(lines[:halfway], lines[halfway:])
    return pairs

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



output_cosine_similarity(list(get50Pairs('even50morePairs.txt')))
# print(list(get50Pairs()))
