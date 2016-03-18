import os,sys
import re
import math
from collections import Counter
import time
pathTrainHam = "/Users/pengpeng/Desktop/train/ham"
pathTrainSpam = "/Users/pengpeng/Desktop/train/spam"
pathTestSpam = "/Users/pengpeng/Desktop/test/spam"
pathTestHam = "/Users/pengpeng/Desktop/test/ham"
# dirs = os.listdir(path)

# for file in dirs:
# file_object = open(path)
# 	if file.endWith(".txt"):


# try:
	# all_the_text = file_object.read().split('\n')
	# for line in all_the_text:
def lengthBiggerThanOne(s):
	return len(s) > 1
# the class is Ham the Y is 1
def update(key,lam,rate,wmap,updateMap):
	sum2 = 0
	for line in fileListHam:
		sum1 = 0
		list = Counter(line)
		for word in list:
			sum1 += list[word] * wmap[word] * 1.0
		condPro = 1 / (1 + math.exp(sum1))
		if key in list:
			sum2 += list[key] * (1 - condPro)
	for line in fileListSpam:
		sum1 = 0
		list = Counter(line)
		for word in list:
			sum1 += list[word] * wmap[word] * 1.0
		condPro = 1 / (1 + math.exp(sum1))
		if key in list:
			sum2 += list[key] * (0 - condPro)	
	result = sum2 * rate - rate * lam * wmap[key] + wmap[key]
	updateMap[key] = result



volcabularyMap = dict()
# spamVolcabularyMap = dict()
# hamVolcabularyMap = dict()
totalNumberDoc = 0
spamDocNumber = 0
hamDocNumber = 0
fileListSpam = [[]]
fileListHam = [[]]
# numberWordsHam = 0
# numberWordsSpam = 0
# numberWordsHamDistinct = 0
# numberWordsSpamDistinct = 0
# numberWordsDistinct = 0
# put the words in ham in dictionary
for file in os.listdir(pathTrainHam):
	if file.endswith(".txt"):
		file_object = open(pathTrainHam+"/"+file)
		# totalNumberDoc += 1
		# hamDocNumber += 1
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
		# spamDocNumber += 1
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


# the W0 = 0
weightMap = dict()
for key,value in volcabularyMap.items():
	weightMap[key] = 0.0
# print weightMap
lamda = 1
learnRate = 1 


# number of iteration
iteration = 10
for i in range(1,iteration):
	print i
	start = time.time()
	weightUpdateMap = dict()
	for key,value in weightMap.items():
		update(key,lamda,learnRate,weightMap,weightUpdateMap)
	weightMap = weightUpdateMap
	end = time.time()
	print(end - start)

