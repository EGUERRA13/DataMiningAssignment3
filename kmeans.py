import sys
import random
import math

kstring = sys.argv[1] 
k = int(kstring)
fileName = sys.argv[2]


def ReadData(fileName):

    f = open(fileName, 'r')
    lines = f.read().splitlines()
    f.close()

 
    items = []
 
    for i in range(0, len(lines)):
        line = lines[i].split('\t')
        itemFeatures = []

        for j in range(0, len(line)):
            v = int(line[j])

            itemFeatures.append(v)
 
        items.append(itemFeatures)
 
    return items

def FindMinMax(items):
    n = len(items[0])
    minima = [sys.maxsize for i in range(n)]
    maxima = [-sys.maxsize -1 for i in range(n)]
     
    for item in items:
        for f in range(len(item)):
            if (item[f] < minima[f]):
                minima[f] = item[f]
             
            if (item[f] > maxima[f]):
                maxima[f] = item[f]
 
    return minima,maxima

def InitializeMeans(items, k, cMin, cMax):
 
    f = len(items[0])
    means = [[0 for i in range(f)] for j in range(k)]
     
    for mean in means:
        for i in range(len(mean)):

            mean[i] = random.uniform(cMin[i]+1, cMax[i]-1)
 
    return means

def EuclideanDistance(x, y):
    S = 0; 
    for i in range(len(x)):
        S += math.pow(x[i]-y[i], 2)
 
    return math.sqrt(S)

def UpdateMean(n,mean,item):
    for i in range(len(mean)):
        m = mean[i]
        m = (m*(n-1)+item[i])/int(n)
        mean[i] = round(m, 3)
     
    return mean

def Classify(means,item):
 
    minimum = sys.maxsize
    index = -1
 
    for i in range(len(means)):
 
        dis = EuclideanDistance(item, means[i])
 
        if (dis < minimum):
            minimum = dis
            index = i
     
    return index

def CalculateMeans(k,items,maxIterations=100000):
 
    cMin, cMax = FindMinMax(items)
 
    means = InitializeMeans(items,k,cMin,cMax)
     
    clusterSizes= [0 for i in range(len(means))]
 
    belongsTo = [0 for i in range(len(items))]
 
    for e in range(maxIterations):
 
        noChange = True
        for i in range(len(items)):
 
            item = items[i];     
            index = Classify(means,item)
 
            clusterSizes[index] += 1
            cSize = clusterSizes[index]
            means[index] = UpdateMean(cSize,means[index],item)
 
            if(index != belongsTo[i]):
                noChange = False
 
            belongsTo[i] = index
 
        if (noChange):
            break
 
    return means

def MakeClusters(means,items):
    clusters = [[] for i in range(len(means))]; 
     
    for item in items:
 
        index = Classify(means,item)
 
        clusters[index].append(item)
 
    return clusters

items = ReadData(fileName)

minima,maxima = FindMinMax(items)
means = InitializeMeans(items,k,minima,maxima)
means = CalculateMeans(k,items,maxIterations=100000)
clusters = MakeClusters(means,items)

with open('output.txt', 'w') as f:
    i = 0
    for cluster in clusters:
        i = i + 1
        for point in cluster:
            f.write(str(point[0]) +  '\t' + str(point[1]) + '\t' + str(i) + '\n')

        

