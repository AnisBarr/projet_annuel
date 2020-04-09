import cv2
import numpy as np
import copy
import math
import tensorflow as tf


cap_region_x_begin=0.5  # start point/total width
cap_region_y_end=0.8  # start point/total width
threshold = 60  #  BINARY threshold
blurValue = 41  # GaussianBlur parameter
bgSubThreshold = 100
learningRate = 0


isBgCaptured = 0   

bgModel = cv2.createBackgroundSubtractorMOG2(0, bgSubThreshold)

def removeBG(frame):
    fgmask = bgModel.apply(frame,learningRate=learningRate)
    kernel = np.ones((3, 3), np.uint8)
    fgmask = cv2.erode(fgmask, kernel, iterations=1)
    res = cv2.bitwise_and(frame, frame, mask=fgmask)
    return res



# Camera
camera = cv2.VideoCapture(0)
# camera.set(640,640)
# cv2.namedWindow('trackbar')
# cv2.createTrackbar('trh1', 'trackbar', threshold, 100)
model = tf.keras.models.load_model("/home/anis/hdd/stockage/projet_annuel/logs/mo_layer_512*10_aug_false_act_relu_do_0.2_l2_0.0_op_adam_lr_0.001_mome_0.01/my_model.h5")

while camera.isOpened():
    ret, frame = camera.read()
    # threshold = cv2.getTrackbarPos('trh1', 'trackbar')
    # frame = cv2.bilateralFilter(frame, 5, 64, 64)  # smoothing filter
    frame = cv2.flip(frame, 1)  # flip the frame horizontally
    cv2.rectangle(frame, (int(cap_region_x_begin * frame.shape[1]), 0),
                 (frame.shape[1], int(cap_region_y_end * frame.shape[0])), (255, 0, 0), 2)
    
    cv2.imshow('original', frame)

    #  Main operation
    if isBgCaptured == 1:  # this part wont run until background captured
        img = frame
        img = img[0:int(cap_region_y_end * frame.shape[0]),
                    int(cap_region_x_begin * frame.shape[1]):frame.shape[1]]  # clip the ROI
        # cv2.imshow('orrri', img)
        # convert the image into binary image
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (64,64))
        cv2.imshow('original_rezized', resized)
        reshaped = np.reshape(resized,(-1,64,64,1))
        data = np.asarray(reshaped, dtype = "float32")/255
        arry = model.predict(data)
        print(np.argmax(arry))
        # print((arry))
        # blur = cv2.GaussianBlur(gray, (blurValue, blurValue), 0)
        # ret, thresh = cv2.threshold(blur, threshold, 255, cv2.THRESH_BINARY)
        # print(gray.shape)
        # cv2.imshow('ori', gray)
        
        # cv2.imshow('output', drawing)
        


    # Keyboard OP 
    k = cv2.waitKey(10)
    if k == 27:  # press ESC to exit
        camera.release()
        cv2.destroyAllWindows()
        break
    elif k == ord('b'):  # press 'b' to capture the background
        isBgCaptured = 1
        
        
        print( '!!!Background Captured!!!')
    elif k == ord('r'):  # press 'r' to reset the background
        bgModel = None
        triggerSwitch = False
        isBgCaptured = 0
        print ('!!!Reset BackGround!!!')
    elif k == ord('q'):
        break

