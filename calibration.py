import numpy as np
import cv2
import glob
import matplotlib.pyplot as plt
#%matplotlib qt
def get_calibrating_points( calibrate_img_path = './camera_cal/calibration*.jpg'):
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((6*9,3), np.float32)
    objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d points in real world space
    imgpoints = [] # 2d points in image plane.

    # Make a list of calibration images
    images = glob.glob(calibrate_img_path)
    ret_images = []
    # Step through the list and search for chessboard corners
    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        # Find the chessboard corners
        ret, corners = cv2.findChessboardCorners(gray, (9,6),None)

        # If found, add object points, image points
        if ret == True:
            ret_images.append(fname)
            objpoints.append(objp)
            imgpoints.append(corners)
            if is_print == True:
                # Draw and display the corners
                img = cv2.drawChessboardCorners(img, (9,6), corners, ret)
                cv2.imshow('img',img)
                cv2.waitKey(500)

    cv2.destroyAllWindows()
    return ret_images, objpoints, imgpoints

def calibrate(gray, row_n = 6, col_n = 9):
    images, objpoints, imgpoints = get_calibrating_points()
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
            objpoints, imgpoints, gray.shape[::-1], None, None)
    return  ret, mtx, dist, rvecs, tvecs

def undistort(img, mtx, dist):
    dst = cv2.undistort(img, mtx, dist, None, mtx)
    return dst

if __name__ == "__main__":
    img = cv2.imread("camera_cal/calibration1.jpg")
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, mtx, dist, rvecs, tvecs = calibrate(gray, 6, 9)
    undistort_img = undistort(img, mtx, dist)
    #print (ret, mtx, dist,rvecs,tvecs)
    cv2.imwrite('examples/undistort_1.png',undistort_img)
