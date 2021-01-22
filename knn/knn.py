from numpy import *

DATE = {"largeDoses":3, "smallDoses":2, "didntLike":1}

def createDataSet():
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels

def classify0(inX, dataSet, labels, k):
    # inX is the coordinates of the point (vector) to be classified
    # k is the number of the nearest neighbors
    dataSetSize = dataSet.shape[0]
    tmp = tile(inX, (dataSetSize, 1))
    diffMat = tmp - dataSet
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)  # sum of the second level of the array
    distances = sqDistances**0.5
    sortedDistIndices = distances.argsort()  # the indices that would sort an array
    classCount = {}
    for i in range(k):
        voteILabel = labels[sortedDistIndices[i]]
        classCount[voteILabel] = classCount.get(voteILabel, 0)+1
    sortedClassCount = sorted(classCount.items(),
                              key=lambda kv: kv[1], reverse=True)
    return sortedClassCount[0][0]

def file2matrix(filename):
    with open(filename) as f:
        lines = f.readlines()
        size = len(lines)
    returnMatrix = zeros((size, 3))
    label = zeros(size)
    for i in range(size):
        line = lines[i].strip().split()
        returnMatrix[i, :] = line[:3]
        label[i] = DATE[line[3]]
    return returnMatrix, label

def normDataSet(dataSet):
    max = dataSet.max(0)
    min = dataSet.min(0)
    diff = max - min
    normMatrix = zeros(dataSet.shape)
    normMatrix = dataSet - tile(min, (dataSet.shape[0], 1))
    normMatrix = normMatrix / tile(diff, (dataSet.shape[0], 1))
    return normMatrix