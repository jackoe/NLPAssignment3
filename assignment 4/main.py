# Kerim Celik
# Jack Wines

def dotProduc(vec1, vec2):
    return sum([x * y for x,y in zip(vec1, vec2)])

def magnitude(vec):
    return sqrt(sum([x ** 2 for x in vec]))

def normalize(vec):
    vecMagnitude = getMagnitude(vec)
    return [x / vecMagnitude for x in vec]

def parseLine(line):
    l = line.split()
    return [l[0]] + [float(x) for x in l[1:]]

def get50Pairs():
    pairs = None
    with open('50pairs.txt', 'r') as f:
        lines = list(f)
        lines = [parseLine(line) for line in lines]
        halfway = len(lines) // 2
        print(halfway)
        pairs = zip(lines[:halfway], lines[halfway:])
    return pairs


print(list(get50Pairs()))
