import cv2
import numpy as np
import copy
import math



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


while camera.isOpened():
    ret, frame = camera.read()
    # threshold = cv2.getTrackbarPos('trh1', 'trackbar')
    # frame = cv2.bilateralFilter(frame, 5, 64, 64)  # smoothing filter
    frame = cv2.flip(frame, 1)  # flip the frame horizontally
    cv2.rectangle(frame, (frame.shape[0]-124, 0) ,(frame.shape[1], 255), (0, 0, 0), 2)
    cv2.imshow('original', removeBG(frame))

    #  Main operation
    if isBgCaptured == 1:  # this part wont run until background captured
        img = frame
        img = img[0:int(frame.shape[0]-124),
                    int(255):frame.shape[1]]  # clip the ROI
        cv2.imshow('orrri', img)
        # convert the image into binary image
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (blurValue, blurValue), 0)
        ret, thresh = cv2.threshold(blur, threshold, 255, cv2.THRESH_BINARY)
        print(gray.shape)
        cv2.imshow('ori', gray)

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

