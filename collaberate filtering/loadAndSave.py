# This function is to read the original "data movieId, userId, Rating"
# change it into two level dictionary and save it to disk
# input completePath "/Users/pengpeng/Desktop/TrainingRatings.txt"
# output trainingData.npy 
def loadDataset(completePath=""):
	""" To load the dataSet"
		Parameter: The folder where the data files are stored
		Return: the dictionary with the data
	"""
	#Recover the titles of the books
	# books = {}
	# for line in open(path+"BX-Books.csv"):
	# 	line = line.replace('"', "")
	# 	(id,title) = line.split(";") [0:2]
	# 	books[id] = title
	
	#Load the data
	prefs = {}
	count = 0
	for line in open(completePath):
		# line = line.replace('"', "")
		# line = line.replace("\\","")
		(user,movieid,rating) = line.split(",")
		try:
			if float(rating) > 0.0:
				prefs.setdefault(user,{})
				prefs[user][movieid] = float(rating)
		except ValueError:
			count+=1
			print "value error found! " + user + movieid + rating
		except KeyError:
			count +=1
			print "key error found! " + user + " " + movieid
	return prefs

	
Path = "/Users/pengpeng/Desktop/"
TrainingData = loadDataset(Path)
import numpy as np
np.save(TrainingPath + 'trainingData', TrainingData)


# file = open(TrainingPath+"TrainingData.py","w")
# text = "dataset={"
# for user in TrainingData:
#     movieData = TrainingData[user]
#     text +=  user +  ": {"
#     for movie in movieData:
#         rating = movieData[movie]
#         text +=  movie + ":" + str(rating)  + ","
#     text += "}," + "\n"
# f = open(TrainingPath+"mydata.py", "w")
# f.write(text)
# f.close()
