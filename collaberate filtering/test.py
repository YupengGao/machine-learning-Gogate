#!/usr/bin/env python
# Implementation of collaborative filtering recommendation engine
 
# from TrainingData import dataset
 
# print "Lisa Rose rating on Lady in the water: {}\n".format(dataset['Lisa Rose']['The Night Listener'])
# print "Michael Phillips rating on Lady in the water: {}\n".format(dataset['Michael Phillips']['Lady in the Water'])
 
# print '**************Jack Matthews ratings**************'
# print dataset['Jack Matthews']

import numpy as np
from math import sqrt
TrainingPath = "/Users/pengpeng/Desktop/"
read_dictionary = np.load(TrainingPath+'trainingData.npy').item()
print(sqrt(sum([read_dictionary['15175'][it] for it in read_dictionary['15175']])))