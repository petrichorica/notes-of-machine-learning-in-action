from numpy import *
import random


def loadDataSet():
    postingList = [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                   ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                   ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                   ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                   ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                   ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0, 1, 0, 1, 0, 1]
    return postingList, classVec


def createVocabList(dataSet):
    vocabList = set()
    for document in dataSet:
        vocabList = vocabList | set(document)
    return list(vocabList)


def words2vec(vocabList, words):
    vec = [0] * len(vocabList)
    for word in words:
        if word in vocabList:
            vec[vocabList.index(word)] = 1
        else:
            print("'%s' is not in the vocabulary." % word)
    return vec


def train(trainMatrix, classVec):
    """
    :param trainMatrix: the training data
    :param classVec: the labels of the training data
    :return (p0_vec, p1_vec, p_class1)
    p0_vec: p(w|c0); p1_vec: p(w|c1).
    w is a vector of words from the vocabulary list. w = <w0, w1, ..., wN>.
    p(w|c0) = p(<w0, w1, ..., wN>|c0) = p(w0|c0)p(w1|c0)...p(wN|c0).
    p(wi|c0) is the probability/frequency that when a sentence is in class 0, it contains wi.
    """
    doc_size = len(trainMatrix)
    num_of_words = len(trainMatrix[0])

    # The probability/frequency of documents of class 1
    p_class1 = sum(classVec) / doc_size

    # Laplace Smoothing, to avoid zero frequency
    p0_num = ones(num_of_words)  # The numerators
    p1_num = ones(num_of_words)
    p0_denom = p1_denom = 2  # The denominators

    for i in range(doc_size):
        if classVec[i] == 1:
            p1_num += trainMatrix[i]
            p1_denom += sum(trainMatrix[i])
        else:
            p0_num += trainMatrix[i]
            p0_denom += sum(trainMatrix[i])

    p1_vec = log(p1_num / p1_denom)  # take the logarithm to avoid underflow
    p0_vec = log(p0_num / p0_denom)

    return p0_vec, p1_vec, p_class1


def classify(vec, p0_vec, p1_vec, p_class1):
    """
    :param vec: the vector of words to be classified, vec = <w0, w1, ..., wN>
    :param p0_vec: p(w|c0)
    :param p1_vec: p(w|c1)
    :param p_class1: p(class=1)
    :return: 0 or 1
    """
    # p0 = (w|c0)p(c0) = p(w0|c0)p(w1|c0)...p(wN|c0)*p(c0)
    p0 = sum(vec * p0_vec) + log(p_class1)
    p1 = sum(vec * p1_vec) + log(1 - p_class1)
    if p0 > p1:
        return 0
    else:
        return 1


def textParser(text):
    import re
    tokens = re.split(r'\W*', text)
    return [token.lower() for token in tokens if len(token) > 2]


def spamTest():
    emails = []
    classVec = []

    ham_num = 74
    spam_num = 86

    for i in range(0, ham_num):
        with open(r'ham\%d.txt' % i) as f:
            word_list = f.read()
        emails.append(word_list)
        classVec.append(0)

    for i in range(0, spam_num):
        with open(r'spam\%d.txt' % i) as f:
            word_list = f.read()
        emails.append(word_list)
        classVec.append(1)

    vocabList = createVocabList(emails)

    trainingSet = list(range(ham_num+spam_num))
    testSet = []
    testSize = 30
    for i in range(testSize):
        index = random.randint(0, len(trainingSet) - 1)
        testSet.append(trainingSet[index])
        del trainingSet[index]

    trainMatrix = []
    trainClass = []
    for index in trainingSet:
        trainMatrix.append(words2vec(vocabList, emails[index]))
        trainClass.append(classVec[index])

    p0_vec, p1_vec, p_spam = train(array(trainMatrix), array(trainClass))
    error = 0
    for index in testSet:
        vec = words2vec(vocabList, emails[index])
        if classify(array(vec), p0_vec, p1_vec, p_spam) != classVec[index]:
            print(emails[index], "\n", "correct category:", classVec[index])
            error += 1
    return error / testSize


if __name__ == '__main__':
    errorRate = spamTest()
    print('The error rate is', errorRate)
