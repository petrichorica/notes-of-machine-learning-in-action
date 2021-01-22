import knn
group, labels = knn.createDataSet()
print(knn.classify0([0.8,0.7], group, labels, 3))

m, labels = knn.file2matrix("datingTestSet.txt")
normMatrix = knn.normDataSet(m)