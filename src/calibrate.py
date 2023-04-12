import numpy as np
import cv2
import glob
import pickle

################ FIND CHESSBOARD CORNERS - OBJECT POINTS AND IMAGE POINTS #############################

chessboardSize = (8, 6)
# frameSize = (848, 480)

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboardSize[0], 0:chessboardSize[1]].T.reshape(-1, 2)

size_of_chessboard_squares_mm = 20
objp = objp * size_of_chessboard_squares_mm

# Arrays to store object points and image points from all the images.
objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane.

images = glob.glob('calibrate_imgs/*.jpg')
for image in images:

    img = cv2.imread(image)
    # img = cv2.resize(img, frameSize)  # resize img to our preferred frame size
    height, width, channels = img.shape
    frameSize = (width, height)
    
    cv2.imshow('img', img)
    cv2.waitKey(100)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert RGB to Grayscale

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray,
                                             chessboardSize,
                                             cv2.CALIB_CB_ADAPTIVE_THRESH +
                                             cv2.CALIB_CB_FAST_CHECK +
                                             cv2.CALIB_CB_NORMALIZE_IMAGE)
    # If found, add object points, image points (after refining them)
    if ret is True:
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        cv2.drawChessboardCorners(img, chessboardSize, corners2, ret)
        cv2.imshow('img', img)
        cv2.waitKey(1000)

cv2.destroyAllWindows()

############## CALIBRATION #######################################################

ret, cameraMatrix, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, frameSize, None, None)

# print
print(f'Camera Matrix := \n{cameraMatrix}')
# Save the camera calibration result for later use (we won't worry about rvecs / tvecs)
pickle.dump((cameraMatrix, dist), open("calibrate_imgs/intrinsics/calibration.pkl", "wb"))
pickle.dump(cameraMatrix, open("calibrate_imgs/intrinsics/cameraMatrix.pkl", "wb"))
pickle.dump(dist, open("calibrate_imgs/intrinsics/dist.pkl", "wb"))
