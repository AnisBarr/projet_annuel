import cv2
import numpy as np
import copy
import math
import tensorflow as tf
import os


cap_region_x_begin=0.5  # start point/total width
cap_region_y_end=0.8  # start point/total width
threshold = 60  #  BINARY threshold
blurValue = 41  # GaussianBlur parameter
bgSubThreshold = 100
learningRate = 0


bgModel = cv2.createBackgroundSubtractorMOG2(0, bgSubThreshold)

def removeBG(frame,bgModel):

    return frame

list_all=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"," "]
list_all=[elt.lower() for elt in list_all]

camera = cv2.VideoCapture(0)
count = 0
isBgCaptured = 0

# for elt in list_all:
#     os.mkdir("../resources/my_data_set/"+elt+"_normal_orig")
#     os.mkdir("../resources/my_data_set/"+elt+"_resize_orig")

tmp_count = 0
current_lettre = None

while camera.isOpened():
    
    ret, frame = camera.read()
    frame = cv2.flip(frame, 1)  # flip the frame horizontally
    cv2.rectangle(frame, (int(cap_region_x_begin * frame.shape[1]), 0),
                (frame.shape[1], int(cap_region_y_end * frame.shape[0])), (255, 0, 0), 2)
    
    cv2.imshow('original', frame)
     
    count+=1

    img = None

    if isBgCaptured == 1  :  # this part wont run until background captured
         
        img = frame
        img = img[0:int(cap_region_y_end * frame.shape[0]),
                    int(cap_region_x_begin * frame.shape[1]):frame.shape[1]]  # clip the ROI

        img = removeBG(img,bgModel)
        resized = cv2.resize(img, (64,64))
        
        cv2.imshow('original_rezized', resized)
        
        k = cv2.waitKey(1)
        for elt in list_all:

            if k == ord(elt):
                if current_lettre == elt :
                    tmp_count +=1 
                else :
                    tmp_count = 0

                current_lettre = elt
                if elt == " ":
                    elt = "space"

                
                
                

                img_flip = cv2.flip(img, 1)
                resized_flip = cv2.flip(resized, 1)
                
                cv2.imshow('original_rezized', resized)

                print(tmp_count)
                cv2.imwrite("../resources/my_data_set/"+elt+"_normal_orig/"+str(count)+".jpg",img)
                cv2.imwrite("../resources/my_data_set/"+elt+"_normal_orig/"+str(count)+"_flip.jpg",img_flip)

                cv2.imwrite("../resources/my_data_set/"+elt+"_resize_orig/"+str(count)+".jpg",resized)
                cv2.imwrite("../resources/my_data_set/"+elt+"_resize_orig/"+str(count)+"flip.jpg",resized_flip)
            
        if k == ord("1"):
            break

   
    k = cv2.waitKey(1)

      
    if k == ord("2"):
        isBgCaptured = 1
        
   
