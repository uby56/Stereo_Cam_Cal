import os
import cv2
import numpy as np
import json
from stereovision.calibration import StereoCalibrator
from stereovision.calibration import StereoCalibration
from stereovision.exceptions import ChessboardNotFoundError

# Global variables preset
total_photos = 70

# Chessboard parameters
# Must use 6 Rows and 9 Column chessboard
rows = 8
columns = 6
square_size = 23

image_size = (640, 480)

if (os.path.isdir("calibration") == False):
    os.makedirs("calibration")

#This is the calibraation class from the StereoVision package
calibrator = StereoCalibrator(rows, columns, square_size, image_size)
photo_counter = 0
print('Start cycle')

#While loop for the calibration. It will go through each pair of image one by one
while photo_counter != total_photos:
    photo_counter += 1 
    print('Importing pair: ' + str(photo_counter))
    if(photo_counter<10):
        leftName = 'cal_image/left/left-000' + str(photo_counter) + '.png'
        rightName = 'cal_image/right/right-000' + str(photo_counter) + '.png'

    if(photo_counter>10):
        leftName = 'cal_image/left/left-00' + str(photo_counter) + '.png'
        rightName = 'cal_image/right/right-00' + str(photo_counter) + '.png'

    if os.path.isfile(leftName) and os.path.isfile(rightName):
        #reading the images in Color
        imgLeft = cv2.imread(leftName, 1)
        imgRight = cv2.imread(rightName, 1)

        #Ensuring both left and right images have the same dimensions
        (H, W, C) = imgLeft.shape

        imgRight = cv2.resize(imgRight, (W, H))

        # Calibrating the camera (getting the corners and drawing them)
        try:
            calibrator._get_corners(imgLeft)
            calibrator._get_corners(imgRight)
        except ChessboardNotFoundError as error:
            print(error)
            print("Pair No " + str(photo_counter) + " ignored")
        else:
            #add_corners function from the Class already helps us with cv2.imshow,
            #and hence we don't need to do it seperately 
            calibrator.add_corners((imgLeft, imgRight), True)
        
    else:
        print ("Pair not found")
        continue


print('Cycle Complete!')

print('Starting calibration... It can take several minutes!')
calibration = calibrator.calibrate_cameras()
calibration.export('calibration')
print('Calibration complete!')

# Lets rectify and show last pair after  calibration
calibration = StereoCalibration(input_folder='calibration')
rectified_pair = calibration.rectify((imgLeft, imgRight))

cv2.imshow('Left Calibrated!', rectified_pair[0])
cv2.imshow('Right Calibrated!', rectified_pair[1])
#why save as jpg here and not png?
cv2.imwrite("rectified_left.jpg", rectified_pair[0])
cv2.imwrite("rectified_right.jpg", rectified_pair[1])
cv2.waitKey(0)