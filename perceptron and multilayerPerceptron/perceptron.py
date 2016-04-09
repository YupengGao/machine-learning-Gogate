import os,sys
import re
import math
from collections import Counter
import time
import numpy as np
from numpy import shape 
pathTrainHam = "/Users/pengpeng/Desktop/train/ham"
pathTrainSpam = "/Users/pengpeng/Desktop/train/spam"
pathTestSpam = "/Users/pengpeng/Desktop/test/spam"
pathTestHam = "/Users/pengpeng/Desktop/test/ham"


volcabularyMap = dict()
# spamVolcabularyMap = dict()
# hamVolcabularyMap = dict()
totalNumberDoc = 0
spamDocNumber = 0
hamDocNumber = 0
fileListSpam = [[]]
fileListHam = [[]]
fileListSpamTest = [[]]
fileListHamTest = [[]]
# numberWordsHam = 0
# numberWordsSpam = 0
# numberWordsHamDistinct = 0
# numberWordsSpamDistinct = 0
# numberWordsDistinct = 0
# put the words in ham in dictionary

def lengthBiggerThanOne(s):
	return len(s) > 1
	
	
	
for file in os.listdir(pathTrainHam):
	if file.endswith(".txt"):
		file_object = open(pathTrainHam+"/"+file)
		# totalNumberDoc += 1
		hamDocNumber += 1
		List = []
		for line in file_object:
			result = re.split(',|:| |-|/|\r|\.|\@|1|2|3|4|5|6|7|8|9|0|\'|\(|\)|\n|!', line)
			result = filter(None, result)
			result = filter(lengthBiggerThanOne,result)
			List = result + List

			for word in result:
				if word in volcabularyMap :
					volcabularyMap [word] += 1
				else:
					volcabularyMap [word] = 1
		fileListHam.append(List)
fileListHam = filter(None, fileListHam)

for file in os.listdir(pathTrainSpam):
	if file.endswith(".txt"):
		file_object = open(pathTrainSpam+"/"+file)
		# totalNumberDoc += 1
		spamDocNumber += 1
		List = []
		for line in file_object:
			result = re.split(',|:| |-|/|\r|\.|\@|1|2|3|4|5|6|7|8|9|0|\'|\(|\)|\n|!', line)
			result = filter(None, result)
			result = filter(lengthBiggerThanOne,result)
			List = result + List
			for word in result:
				if word in volcabularyMap:
					volcabularyMap[word] += 1
				else:
					volcabularyMap[word] = 1
		fileListSpam.append(List)
fileListSpam = filter(None, fileListSpam)

wordList = []
for key,value in volcabularyMap.items():
	wordList.append(key)


SpamTrainData = [([0] * 9165) for i in range(123)]
HamTrainData = [([0] * 9165) for i in range(340)]
SpamTestData = [([0] * 9165) for i in range(130)]
HamTestData = [([0] * 9165) for i in range(348)]
# get the volcabularylist
volcabularyList = []
for key,value in volcabularyMap.items():
	volcabularyList.append(key)
volcabularyList = filter(None,volcabularyList)

# get the spamTrainData matrix
count = 0
for line in fileListSpam:
	list = Counter(line)
	for word in list:
		# print list[word]
		SpamTrainData[count][volcabularyList.index(word)] = list[word]
	count += 1

# get the HamTrainData matrix
count = 0
for line in fileListHam:
	list = Counter(line)
	for word in list:
		HamTrainData[count][volcabularyList.index(word)] = list[word]
	count += 1



# np.savetxt('SpamTrainData.txt', SpamTrainData, fmt='%s	')
# np.savetxt('HamTrainData.txt', HamTrainData, fmt='%s	')

count = 0
for file in os.listdir(pathTestSpam):
	if file.endswith(".txt"):
		file_object = open(pathTestSpam+"/"+file)
		count += 1
		List = []
		for line in file_object:
			result = re.split(',|:| |-|/|\r|\.|\@|1|2|3|4|5|6|7|8|9|0|\'|\(|\)|\n|!', line)
			result = filter(None, result)
			result = filter(lengthBiggerThanOne,result)
			List = result + List
		fileListSpamTest.append(List)
fileListSpamTest = filter(None, fileListSpamTest)

count = 0
for file in os.listdir(pathTestHam):
	if file.endswith(".txt"):
		file_object = open(pathTestHam+"/"+file)
		count += 1
		List = []
		for line in file_object:
			result = re.split(',|:| |-|/|\r|\.|\@|1|2|3|4|5|6|7|8|9|0|\'|\(|\)|\n|!', line)
			result = filter(None, result)
			result = filter(lengthBiggerThanOne,result)
			List = result + List
		fileListHamTest.append(List)
fileListHamTest = filter(None, fileListHamTest)
# print len(fileListHamTest),len(fileListSpamTest)
# get the spamTrainData matrix
count = 0
for line in fileListSpamTest:
	list = Counter(line)
	for word in list:
		# print list[word]
		if word in volcabularyList:
			SpamTestData[count][volcabularyList.index(word)] = list[word]
	count += 1

# get the HamTrainData matrix
count = 0
for line in fileListHamTest:
	list = Counter(line)
	for word in list:
		if word in volcabularyList:
			HamTestData[count][volcabularyList.index(word)] = list[word]
	count += 1
# np.savetxt('SpamTestData.txt', SpamTestData, fmt='%s	')
# np.savetxt('HamTestData.txt', HamTestData, fmt='%s	')
TrainData = SpamTrainData + HamTrainData
TrainLable = 123*[0] + 340*[1]
TestData = SpamTestData + HamTestData
TestLabel = 130*[0] + 348*[1]


def perceptronTraining(data,label):
	dataMatrix = np.mat(data)
	labelMatrix = np.mat(label).transpose()
	m,n = shape(dataMatrix)
	alpha = 0.9
	weights = np.ones((n,1))
	# ?weights= np.matrix(np.random.rand(n,1))
	iteration = 30000
	# traverse all the training data
	for i in range(iteration):
		j = i
		if i >= 463:
			j = i%463
		h = dataMatrix[j,:] * weights
		if h >= 0:
			h = 1
		if h < 0:
			h = 0
		error = (labelMatrix[j,0] - h)
		if error != 0:
			weights = weights + alpha * dataMatrix[j,:].transpose() * error
	return weights

def test(weights,data,label):
	dataMatrix = np.mat(data)
	labelMatrix = np.mat(label).transpose()
	result = dataMatrix * weights
	m,n = np.shape(result)
	for i in range(m):
		if result[i,0] >= 0:
			result[i,0] = 1
		if result[i,0] < 0:
			result[i,0] = 0
	result = result - labelMatrix
	sum = 0
	for i in range(m):
		sum += math.pow(result[i,0],2)
	return sum * 1.0 / m


print "training start"
weight = perceptronTraining(TrainData,TrainLable)
accu = 1 - test(weight,TestData,TestLabel)
# np.savetxt("out.txt",weight)
print accu
