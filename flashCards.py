__author__ = 'lockout87'
from random import shuffle

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
        self.stackSize = 10
        for arg in args:
            self.cardList.extend(arg)

        self.stackRank = sum(card.rank for card in self.cardList)/len(self.cardList)
        self.stackCoefficient = self.stackSize / len(self.cardList)

        self.stack = self.shuffleStack()

        self.incorrectStack = []
        self.correctStack = []

    def shuffleStack(self):
        stack = []
        localCardList = self.cardList
        shuffle(localCardList)
        cardUse = {}
        while len(stack) < self.stackSize:
            addCard = self.getBest(localCardList)
            if addCard in cardUse:
                cardUse[addCard] += 1
            else:
                cardUse[addCard] = 1
            if cardUse[addCard] >= self.stackRank:
                localCardList.remove(addCard)
            stack.append(addCard)
        shuffle(stack)
        return stack

    def getBest(self, cardList):
        best = None
        bestCard = None
        for card in cardList:
            if best is None:
                best = abs(card.rank - self.stackRank)
                bestCard = card
                continue
            newBest = abs(card.rank - self.stackRank)
            if newBest < best:
                best = newBest
                bestCard = card
        return bestCard

    def pullCard(self):
        card = self.stack.pop()
        options = [card.swedish, card.english]
        shuffle(options)
        print options[0]
        return card

    def getAnswer(self):
        return raw_input("What is the translation: ")

    def answerCorrect(self, card, answer):
        retVal = False
        if answer.lower() in [card.swedish.lower(), card.english.lower()]:
            retVal = True

        return retVal

    def cycle(self):
        while len(self.stack) > 0:
            card = self.pullCard()
            answer = self.getAnswer()
            if self.answerCorrect(card, answer):
                if card not in self.correctStack and card not in self.incorrectStack:
                    card.rank -= 1
                    self.correctStack.append(card)
            else:
                if card in self.incorrectStack:
                    self.incorrectStack[self.incorrectStack.index(card)].rank += 1
                else:
                    card.rank += 1
                    self.incorrectStack.append(card)
                    if card in self.correctStack:
                        self.correctStack.remove(card)




def loadFile(filePath, fileType):
    fileList = []
    with open(filePath, "r") as file:
        for line in [line for line in file if line.strip()]:
            fileList.append(fileType(line))
    return fileList


def writeFile(filePath, cards):
    with open(filePath, "w") as file:
        for card in cards:
            file.write(card.swedish + "," + card.english + "," + str(card.rank) + "\n")

if __name__ == "__main__":
    words   = loadFile("newwords", Word)
    #phrases = loadFile("newPhrases", Phrase)
    cardStack = Stack(words)#, phrases)

    cardStack.cycle()
    print cardStack.incorrectStack
    print cardStack.correctStack

    writeFile("whatever", cardStack.cardList)
