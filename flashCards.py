__author__ = 'lockout87'
from random import shuffle, seed
from datetime import datetime

seed(datetime.now())


class LineLengthException(Exception):
    """
    Exception for lines that are not the correct size.
    :param line: line from file
    """
    def __init__(self, line):
        self.line = line

    def __str__(self):
        return "Line length not 3:", self.line

class BoundedNumber(object):
    """
    A number that has a upper and lower bound.
    """
    class OutOfBounds(Exception):
        """

        """
    def __init__(self, minimum, maximum, initValue):
        self.min = minimum
        self.max = maximum
        self._value = initValue

    def set(self, value):
        if self.min <= value <= self.max:
            self._value = value
        else:
            if value > self.max:
                self._value = self.max
            else:
                self._value = self.min

    def get(self):
        return int(self._value)

    def increment(self):
        if self._value + 1 <= self.max:
            self._value += 1

    def decrement(self):
        if self._value - 1 >= self.min:
            self._value -= 1


class Word(object):
    def __init__(self, line):
        splitLine = line.split(",")
        if len(splitLine) != 3:
            raise LineLengthException(line)

        self.swedish    = splitLine[0]
        self.english    = splitLine[1]
        self.rank       = BoundedNumber(1, 20, int(splitLine[2]))


class Phrase(object):
    def __init__(self, line):
        splitLine = line.split(",")
        if len(splitLine) != 3:
            raise LineLengthException(line)

        self.swedish  = splitLine[0]
        self.english  = splitLine[1]
        self.rank     = BoundedNumber(1, 20, int(splitLine[2]))


class Stack(object):
    def __init__(self, *args):
        self.cardList = []
        self.stackSize = 10
        for arg in args:
            self.cardList.extend(arg)

        self.stackRank = sum(card.rank.get() for card in self.cardList)/len(self.cardList)
        self.stackCoefficient = self.stackSize / len(self.cardList)

        self.stack = self.shuffleStack()

        self.incorrectStack = []
        self.correctStack = []

    def shuffleStack(self):
        stack = []
        for card in self.cardList:
            stack.extend([card] * card.rank.get())
        shuffle(stack)
        stack = stack[:self.stackSize]
        return stack

    def getBest(self, cardList):
        best = None
        bestCard = None
        for card in cardList:
            if best is None:
                best = abs(card.rank.get() - self.stackRank)
                bestCard = card
                continue
            newBest = abs(card.rank.get() - self.stackRank)
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
                print "Correct!", card.swedish, "is", card.english
                if card not in self.correctStack and card not in self.incorrectStack:
                    card.rank.decrement()
                    self.correctStack.append(card)
            else:
                print "Incorrect!", card.swedish, "is", card.english
                if card in self.incorrectStack:
                    self.incorrectStack[self.incorrectStack.index(card)].rank.increment()
                else:
                    card.rank.decrement()
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
            file.write(card.swedish + "," + card.english + "," + str(card.rank.get()) + "\n")

if __name__ == "__main__":
    words   = loadFile("newWords", Word)
    phrases = loadFile("newPhrases", Phrase)
    cardStack = Stack(words, phrases)
    cardStack.cycle()

    writeFile("newWords", cardStack.cardList)
