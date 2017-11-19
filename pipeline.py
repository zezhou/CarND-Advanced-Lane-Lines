

def pipeline(img):
    gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    ret, mtx, dist, rvecs, tvecs = calibrate(gray, 6, 9) # camera calibration
    undistort_img = undistort(img, mtx, dist) # distortion correction  
    binary_warped, M, Minv,src = warped(undistort_img) # perspective transform
    
    # Sobel Absolute (using default parameters)

    gradx = abs_sobel_thresh(binary_warped)
    grady = abs_sobel_thresh(image, orient='y', thresh=(120, 255))
    mag_binary = mag_thresh(binary_warped)
    dir_binary = dir_threshold(binary_warped)
    # HLS S-channel Threshold (using default parameters)
    img_SThresh = hls_sthresh(binary_warped)

    # HLS L-channel Threshold (using default parameters)
    img_LThresh = hls_lthresh(binary_warped)

    # Lab B-channel Threshold (using default parameters)
    img_BThresh = lab_bthresh(binary_warped)
    
    # Combine HLS and Lab B channel thresholds
    combined = np.zeros_like(img_BThresh)
    combined[(gradx == 1)| (mag_binary ==1)|(dir_binary == 1)|(img_LThresh == 1) |(img_BThresh == 1)] = 1
    # use less than 3 thresh to improve speed and accuracy
    #combined[(img_LThresh == 1) |(img_BThresh == 1)] = 1

    return combined, Minv

