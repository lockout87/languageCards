__author__ = 'lockout87'

class LineLengthException(Exception):
    """
    Exception for lines that are not the correct size.
    :param line: line from file
    """
    def __init__(self, line):
        self.line = line

    def __str__(self):
        return "Line length not 3:", self.line


class Word(object):
    def __init__(self, line):
        splitLine = line.split(",")
        if len(splitLine) != 3:
            raise LineLengthException(line)

        self.swedish    = splitLine[0]
        self.english    = splitLine[1]
        self.rank       = int(splitLine[2])


class Phrase(object):
    def __init__(self, line):
        splitLine = line.split(",")
        if len(splitLine) != 3:
            raise LineLengthException(line)

        self.swedish  = splitLine[0]
        self.english  = splitLine[1]
        self.rank     = int(splitLine[2])


class Stack(object):
    def __init__(self, *args):
        self.cardList = []
        self.stackSize = 100
        for arg in args:
            self.cardList.extend(arg)

        self.stackRank = sum(card.rank for card in self.cardList)/len(self.cardList)
        self.stackCoefficient = self.stackSize / len(self.cardList)

        #self.stack = self.shuffleStack()

    def shuffleStack(self):
        stack = []
        higher  = []
        lower   = []
        for card in self.cardList:
            if card.rank >= self.stackRank:
                higher.append(card)
            else:
                lower.append(card)

        return stack


def loadFile(filePath, type):
    fileList = []
    with open(filePath, "r") as file:
        for line in [line for line in file if line.strip()]:
            fileList.append(type(line))
    return fileList


if __name__ == "__main__":
    words   = loadFile("newwords", Word)
    phrases = loadFile("newPhrases", Phrase)
    cardStack = Stack(words, phrases)

    print str(cardStack.stackCoefficient)
    print str(len(cardStack.cardList))

    print cardStack.stackRank

