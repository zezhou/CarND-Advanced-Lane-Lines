#Use color transforms, gradients, etc., to create a thresholded binary image.
import cv2
import numpy as np

def wraped(undistorted):
    img_size = (undistorted.shape[0],undistorted.shape[1])
    src1 = np.float32(
    [[(img_size[0] / 2) - 55, img_size[1] / 2 + 100],
    [((img_size[0] / 6) - 10), img_size[1]],
    [(img_size[0] * 5 / 6) + 60, img_size[1]],
    [(img_size[0] / 2 + 55), img_size[1] / 2 + 100]])
    
    dst1 = np.float32(
    [[(img_size[0] / 4), 0],
    [(img_size[0] / 4), img_size[1]],
    [(img_size[0] * 3 / 4), img_size[1]],
    [(img_size[0] * 3 / 4), 0]])

    h,w = undistorted.shape[:2]

    # define source and destination points for transform
    src = np.float32([(575,464),
                  (707,464), 
                  (258,682), 
                  (1049,682)])
    dst = np.float32([(450,0),
                  (w-450,0),
                  (450,h),
                  (w-450,h)])
    #import pdb; pdb.set_trace()
    M = cv2.getPerspectiveTransform(src, dst)
    Minv = cv2.getPerspectiveTransform(dst, src)

    # e) use cv2.warpPerspective() to warp your image to a top-down view
    warped = cv2.warpPerspective(undistorted, M, (img_size[1], img_size[0]), flags=cv2.INTER_LINEAR)
    return warped, M, Minv

if __name__ == "__main__":
    from calibration import calibrate, undistort
    img = cv2.imread("test_images/test1.jpg")
    img_size = (img.shape[0], img.shape[1])
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, mtx, dist, rvecs, tvecs = calibrate(gray, 6, 9)
    undistort_img = undistort(img, mtx, dist)
    cv2.imwrite('examples/test_undistort_1.png', undistort_img)
    unwraped_img, M, Minv = wraped(undistort_img, img_size)
    cv2.imwrite('examples/unwraped_1.png', unwraped_img)