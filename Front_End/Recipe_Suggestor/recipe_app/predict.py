# import the necessary packages


import numpy as np
import argparse
import imutils
import cv2
import os
import sys
import pandas as pd
import pickle

from keras.src.saving import load_model
from keras.src.utils import img_to_array
from sklearn import preprocessing
from difflib import get_close_matches
from sklearn.neighbors import KNeighborsClassifier
# initialising

def predictor(image_path):
	dir_labels=()
	dir_predict=()
	num_class=0
	args=dict()
	args["dataset"]="Data/training_set"
	args["model"]="Data/trained_model"
	args["image"]="media/"+image_path
	#findings the labels
	for file in os.listdir(args["dataset"]) :
		temp_tuple=(file,'null')
		dir_labels=dir_labels+temp_tuple
		dir_labels=dir_labels[:-1]
		num_class=num_class+1

	print("[INFO] Labels are ",dir_labels)

	# load the image
	print("[INFO] Loading Image...")
	try :
		image = cv2.imread(args["image"])
		orig = image.copy()
	except AttributeError :
		#print("[INFO] Error in the test image... ")
		#print('[INFO] Exiting...')
		sys.exit()

	# pre-process the image for classification
	image = cv2.resize(image, (28, 28))
	image = image.astype("float") / 255.0
	image = img_to_array(image)
	image = np.expand_dims(image, axis=0)

	# load the trained convolutional neural network
	#print("[INFO] Loading Network...")
	model_base=args["model"]+'.h5'
	model = load_model(model_base)

	# classify the input image
	dir_predict = model.predict(image)[0]
	#print(dir_labels)
	#print(dir_predict)
	for i in range(num_class) :
		var = 0
		for j in range(num_class) :
			if(dir_predict[i]>=dir_predict[j]) :
				var=var+1
		if(var==num_class) :
			label=dir_labels[i]
			proba=dir_predict[i]
		elif(var==num_class-1) :
			label2=dir_labels[i]
			proba2=dir_predict[i]

	#print("label")
	#print(label)
	#print('[INFO] Exiting...')
	return label
#print("yes",predictor("test_set/baa.jpg"))
