import numpy as np 
import cv2
from stereovision.calibration import StereoCalibration
from cam_setting import Start_Cameras
 
# Check for left and right camera IDs
# These values can change depending on the system
CamL_id = 0 # Camera ID for left camera
CamR_id = 1 # Camera ID for right camera

L_cam = Start_Cameras(CamL_id)
R_cam = Start_Cameras(CamR_id)

L_cam.start()
R_cam.start()

calibration = StereoCalibration(input_folder='calibration')
 
# Reading the mapping values for stereo image rectification
# cv_file = cv2.FileStorage("data/stereo_rectify_maps.xml", cv2.FILE_STORAGE_READ)
# Left_Stereo_Map_x = cv_file.getNode("Left_Stereo_Map_x").mat()
# Left_Stereo_Map_y = cv_file.getNode("Left_Stereo_Map_y").mat()
# Right_Stereo_Map_x = cv_file.getNode("Right_Stereo_Map_x").mat()
# Right_Stereo_Map_y = cv_file.getNode("Right_Stereo_Map_y").mat()
# cv_file.release()
 
def nothing(x):
    pass

 
# Creating an object of StereoBM algorithm
stereo = cv2.StereoBM_create()
 
while True:
 
  # Capturing and storing left and right camera images
  retL, imgL= L_cam.read()
  retR, imgR= R_cam.read()
   
  # Proceed only if the frames have been captured
  if retL and retR:
    imgR_gray = cv2.cvtColor(imgR,cv2.COLOR_BGR2GRAY)
    imgL_gray = cv2.cvtColor(imgL,cv2.COLOR_BGR2GRAY)

    rectified_pair = calibration.rectify((imgR_gray, imgL_gray))
 
    # Updating the parameters based on the trackbar positions
    numDisparities = 16
    blockSize = 9
    preFilterType = 1
    preFilterSize = 9
    preFilterCap = 1
    textureThreshold = 1
    uniquenessRatio = 1
    speckleRange = 1
    speckleWindowSize = 2
    disp12MaxDiff = 5
    minDisparity = 2
     
    # Setting the updated parameters before computing disparity map
    stereo.setNumDisparities(numDisparities)
    stereo.setBlockSize(blockSize)
    stereo.setPreFilterType(preFilterType)
    stereo.setPreFilterSize(preFilterSize)
    stereo.setPreFilterCap(preFilterCap)
    stereo.setTextureThreshold(textureThreshold)
    stereo.setUniquenessRatio(uniquenessRatio)
    stereo.setSpeckleRange(speckleRange)
    stereo.setSpeckleWindowSize(speckleWindowSize)
    stereo.setDisp12MaxDiff(disp12MaxDiff)
    stereo.setMinDisparity(minDisparity)

    c, r = rectified_pair[0].shape
    dmLeft = rectified_pair[0]
    dmRight = rectified_pair[1]

    # Calculating disparity using the StereoBM algorithm
    disparity = stereo.compute(dmLeft, dmRight)
    # NOTE: Code returns a 16bit signed single channel image,
    # CV_16S containing a disparity map scaled by 16. Hence it 
    # is essential to convert it to CV_32F and scale it down 16 times.
 
    # Converting to float32 
    disparity = disparity.astype(np.float32)
 
    # Scaling down the disparity values and normalizing them 
    disparity = (disparity/16.0 - minDisparity)/numDisparities
 
    # Displaying the disparity map
    cv2.imshow("disp",disparity)
 
    # Close window using esc key
    if cv2.waitKey(1) == 27:
      break
   
  else:
    CamL= cv2.VideoCapture(CamL_id)
    CamR= cv2.VideoCapture(CamR_id)

L_cam.stop()
L_cam.release()
R_cam.stop()
R_cam.release()
cv2.destroyAllWindows()