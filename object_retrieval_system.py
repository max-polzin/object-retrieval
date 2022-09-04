'''
SYSC 5906:
Object Retrieval System - V1.0
---
This system peforms a object retrieval task inside a known semantically mapped indoor space.

The main components of the system are:
1.   Guessing the most likely room(s) that a object will be located in
2.   Path planning to the likely room(s)
3.   Searching of the space untill the desired object is detected
'''
########
# SETUP:
########
#Directories with model weights and datasets
NN1_OD_DIRECTORY = '/weights/object_detector/'   #Object detector
NN2_RD_DIRECTORY = '/weights/room_classifier/' #Room detector/guessor
TEST_DATASET = '/gdrive/My Drive/Colab Notebooks/SYSC 5906/datasets/mit_indoors/processed/data_labelsOnly/'
PICKLE_DIRECTORY = '/models/trained_data/data_labelsOnly/'

#Import libraries and scripts
import tensorflow as tf
import pandas as pd
import pickle
import sklearn as sk
import matplotlib.pyplot as plt
import numpy as np
import tensorflow_datasets as tfds
import keras.api._v2.keras as keras
from keras.models import load_model
from sklearn.model_selection import train_test_split

from room_detection.room_detection import roomGuesser, roomDetector
from object_detection.object_detection import objectDetector
from object_detection.vision_system import cameraSetup
from path_planner.path_planner import path_planner

#Import dataset
pickledData = open(PICKLE_DIRECTORY+"listOfAllObj_v3.pkl","rb")
dataSet = pickle.load(pickledData)
pickledData.close()

#Import list of unqiue objects from training dataset
pickledObjs = open(PICKLE_DIRECTORY+"uniqueObjs_v3.pkl","rb")
uniqueObjs = pickle.load(pickledObjs)
uniqueObjs = dataSet.columns[0:-1]
pickledObjs.close()

#Load custom models
model_OD = tf.keras.models.load_model(NN1_OD_DIRECTORY)
model_RD = tf.keras.models.load_model(NN2_RD_DIRECTORY)

#Summarize models
model_OD.summary()
model_RD.summary()

####################################
# OFFLINE VERSION
# This version of the system loads a 
# pre-recorded map and video file.
####################################
########
# ROOM GUESSING:
########
#Get a desired object from the user
targetObj = input('Enter the desired object: ')

#Search for singular objects in the current input and return top results
result, n = roomGuesser(targetObj, uniqueObjs, model_RD)

#Check if result is valid
if n == 0:
    print(result[0])
    #Get a new desired object from the user
    targetObj = input('Enter a valid desired object: ')

########
# INTIAL PATH PLAN:
########
# get current pose
# plan path from current pose

########
# ACCESS PRE-RECORDED DATA (VIDEO+POSES):
########
OFFLINE = True
frames, path = cameraSetup(OFFLINE)

########
# MAIN LOOP:
########
targetObjStatus = False
haveFrames = True
while(not(targetObjStatus)):
    #Check if target was found in the last analysed frame
    if targetObjStatus:
        break

    for currentFrame in frames:
        ########
        # OBJECT DETECTION:
        ########
        #Detect objects in current frame
        detectedObjects = objectDetector(currentFrame, model_OD)

        ########
        # TARGET CHECK:
        ########
        if targetObj in detectedObjects:
            targetObjStatus = True
            print(f'The {targetObj} has been found!' )
        else:
            print('Still searching for target object')

        ########
        # ROOM DETECTION:
        ########
        #Label rooms based on currently detected objects
        detectedRooms = roomDetector(detectedObjects,model_RD)

        ########
        # PATH PLANNING:
        ########
        # confirm current room matches map (detectedRooms + currentPose + labeledMapFile)
        # update local path
        # if path end has been reached, throw err msg

        #Load in pre-recorded map
        currentMap = grab_map()

        #Load in pre-recorded localized rooms
        rooms = grab_rooms()

        #Get current pose for the frame


        path_planner(currentMap, targetObjStatus, detectedRooms, rooms, current_pose)