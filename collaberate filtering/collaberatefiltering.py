import numpy as np
from math import sqrt
Path = "/Users/pengpeng/Desktop/"



#Returns the Pearson correlation coefficient for p1 and p2 
# p1--active user p2-- user
def sim_pearson(prefs,p1,p2):
	#Get the list of mutually rated items
	si = {}
	for item in prefs[p1]:
		if item in prefs[p2]: 
			si[item] = 1

	#if they are no rating in common, return 0
	if len(si) == 0:
		return 0

	#sum calculations
	n = len(si)
	vote_p1_mean = sum(prefs[p1][it] for it in prefs[p1]) / len(prefs[p1])
	vote_p2_mean = sum(prefs[p2][it] for it in prefs[p2]) / len(prefs[p2])
	# vote_p1_mean = sum([prefs[p1][it] for it in si]) / n
	# vote_p2_mean = sum([prefs[p2][it] for it in si]) / n
	pSum = sum([(prefs[p1][it] - vote_p1_mean) * (prefs[p2][it] - vote_p2_mean) for it in si])
	# fenzi = pSum - n * vote_p1_mean * vote_p2_mean
	sum1Sq = sum([pow(prefs[p1][it] - vote_p1_mean,2) for it in si])
	sum2Sq = sum([pow(prefs[p2][it] - vote_p2_mean,2) for it in si])
	fenmu = sqrt((sum1Sq) * (sum2Sq))
	if fenmu == 0:
		return 0
	r = pSum / fenmu
	return r
	# sum of all preferences
	# sum1 = sum([prefs[p1][it] for it in si])
	# sum2 = sum([prefs[p2][it] for it in si])
	# # sum1 = sum(prefs[p1][it] for it in prefs[p1]) / len(prefs[p1])
	# # sum2 = sum(prefs[p2][it] for it in prefs[p2]) / len(prefs[p2])
	# #Sum of the squares
	# sum1Sq = sum([pow(prefs[p1][it],2) for it in si])
	# sum2Sq = sum([pow(prefs[p2][it],2) for it in si])

	# #Sum of the products
	# pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])

	# #Calculate r (Pearson score)
	# num = pSum - (sum1 * sum2/n)
	# den = sqrt((sum1Sq - pow(sum1,2)/n) * (sum2Sq - pow(sum2,2)/n))
	# if den == 0:
	# 	return 0

	# r = num/den

	# return r
	
	


# a--active user j--item
def get_prediction(prefs,a,j):
	if a in prefs:		
		length = len(prefs[a])
		vote_a_mean = sum([prefs[a][it] for it in prefs[a]]) / length
		sumWeight = 0
		temp = 0
		for user in prefs:
			if user == a:
				continue
			vote_user_mean = sum([prefs[user][it] for it in prefs[user]]) / len(prefs[user])
			weight = sim_pearson(trainingData,a,user)
			sumWeight += weight
			if j in prefs[user]:
				temp += weight * (prefs[user][j] - vote_user_mean)
			# else:
				
			# 	temp += weight * (0 - vote_user_mean)

		k = 1/(sumWeight)
		prediction = k * temp + vote_a_mean
		return prediction
	else:
		return 0

# Load
trainingData = np.load(Path + 'trainingData.npy').item()
sumOfSquare = 0
count = 0
for line in open(Path+ "TestingRatings.txt"):
	(user,movieid,rating) = line.split(",")
	count += 1
	pre_rating = get_prediction(trainingData,(user),(movieid))
	sumOfSquare += pow(pre_rating - float(rating), 2)
	print pre_rating
	# print movieid, user
	
MSE = sqrt(sumOfSquare / count)

