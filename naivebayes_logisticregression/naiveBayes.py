import os,sys
import re
import math
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

# volcabularyMap = dict()
spamVolcabularyMap = dict()
hamVolcabularyMap = dict()
totalNumberDoc = 0
spamDocNumber = 0
hamDocNumber = 0
numberWordsHam = 0
numberWordsSpam = 0
numberWordsHamDistinct = 0
numberWordsSpamDistinct = 0
numberWordsDistinct = 0
# put the words in ham in dictionary
for file in os.listdir(pathTrainHam):
	if file.endswith(".txt"):
		file_object = open(pathTrainHam+"/"+file)
		totalNumberDoc += 1
		hamDocNumber += 1
		for line in file_object:
			result = re.split(',|:| |-|/|\r|\.|\@|1|2|3|4|5|6|7|8|9|0|\'|\(|\)|\n|!', line)
			result = filter(None, result)
			result = filter(lengthBiggerThanOne,result)
			
			for word in result:
				word = word.lower()
				if word in hamVolcabularyMap :
					hamVolcabularyMap [word] += 1
				else:
					hamVolcabularyMap [word] = 1
numberWordsHamDistinct = len(hamVolcabularyMap )
numberWordsHam = sum(hamVolcabularyMap.values())

# put the words in spam in dictionary
for file in os.listdir(pathTrainSpam):
	if file.endswith(".txt"):
		file_object = open(pathTrainSpam+"/"+file)
		totalNumberDoc += 1
		spamDocNumber += 1
		for line in file_object:
			result = re.split(',|:| |-|/|\r|\.|\@|1|2|3|4|5|6|7|8|9|0|\'|\(|\)|\n|!', line)
			result = filter(None, result)
			result = filter(lengthBiggerThanOne,result)
			
			for word in result:
				word = word.lower()
				if word in spamVolcabularyMap:
					spamVolcabularyMap[word] += 1
				else:
					spamVolcabularyMap[word] = 1
# print spamDocNumber,totalNumberDoc,hamDocNumber
ProSpam = spamDocNumber*1.0/totalNumberDoc
ProHam = hamDocNumber*1.0/totalNumberDoc
numberWordsSpamDistinct = len(spamVolcabularyMap)
numberWordsSpam = sum(spamVolcabularyMap.values())
numberWordsDistinct = numberWordsSpamDistinct + numberWordsHamDistinct

hamDocNumbertest = 0
spamDocNumbertest = 0
missClassify = 0
for file in os.listdir(pathTestSpam):
	if file.endswith(".txt"):
		file_object = open(pathTestSpam+"/"+file)
		spamDocNumbertest += 1
		# hamDocNumber += 1
		List = []
		probSpam = []
		probHam = []

		for line in file_object:
			result = re.split(',|:| |-|/|\r|\.|\@|1|2|3|4|5|6|7|8|9|0|\'|\(|\)|\n|!', line)
			result = filter(None, result)
			result = filter(lengthBiggerThanOne,result)
			List = List + result
		# get the conditional probability for each term for spam class
		for word in List:
			word = word.lower()
			if word in spamVolcabularyMap:
				p = (spamVolcabularyMap[word] + 1) *1.0/ (numberWordsSpam + numberWordsDistinct)
			else:
				p = (0 + 1) *1.0/ (numberWordsSpam + numberWordsDistinct)
			probSpam.append(p)
		for word in List:
			word = word.lower()
			if word in hamVolcabularyMap:
				p1 = (hamVolcabularyMap[word] + 1) *1.0/ (numberWordsHam + numberWordsDistinct)
			else:
				p1 = (1) *1.0/ (numberWordsHam + numberWordsDistinct)
			probHam.append(p1)
		# print ProSpam
		proFinalSpam = math.log10(ProSpam)
		proFinalHam = math.log10(ProHam)
		for num in probSpam:
			proFinalSpam += math.log10(num)
		for num in probHam:
			proFinalHam += math.log10(num)
		if(proFinalSpam < proFinalHam):
			missClassify += 1

for file in os.listdir(pathTestHam):
	if file.endswith(".txt"):
		file_object = open(pathTestHam+"/"+file)
		hamDocNumbertest += 1
		# hamDocNumber += 1
		List = []
		probSpam = []
		probHam = []

		for line in file_object:
			result = re.split(',|:| |-|/|\r|\.|\@|1|2|3|4|5|6|7|8|9|0|\'|\(|\)|\n|!', line)
			result = filter(None, result)
			result = filter(lengthBiggerThanOne,result)
			List = List + result
		# get the conditional probability for each term for spam class
		for word in List:
			word = word.lower()
			if word in spamVolcabularyMap:
				p = (spamVolcabularyMap[word] + 1) *1.0/ (numberWordsSpam + numberWordsDistinct)
			else:
				p = (0 + 1) *1.0/ (numberWordsSpam + numberWordsDistinct)
			probSpam.append(p)
		# get the conditional probability for each term for ham class
		for word in List:
			word = word.lower()
			if word in hamVolcabularyMap:
				p1 = (hamVolcabularyMap[word] + 1) *1.0/ (numberWordsHam + numberWordsDistinct)
			else:
				p1 = (1) *1.0/ (numberWordsHam + numberWordsDistinct)
			probHam.append(p1)
		# print ProSpam
		proFinalSpam = math.log10(ProSpam)
		proFinalHam = math.log10(ProHam)
		for num in probSpam:
			proFinalSpam += math.log10(num)
		for num in probHam:
			proFinalHam += math.log10(num)
		if(proFinalSpam > proFinalHam):
			missClassify += 1

accuracy = 1 - missClassify*1.0/(hamDocNumbertest+spamDocNumbertest)
print accuracy
		# print proFinalSpam,proFinalHam
# print numberWordsHam,numberWordsHamDistinct,numberWordsSpam,numberWordsSpamDistinct
# for key, value in volcabularyMap.iteritems():
# 	print key,value
# print SpamNumber,hamNumber,totalNumberDoc
# finally:
# 	file_object.close( )