import cv2
import numpy as np

def abs_sobel_thresh(gray, orient='x', thresh_min=25, thresh_max=255):
    
    # Apply the following steps to img
    # 1) Convert to grayscale
    # 2) Take the derivative in x or y given orient = 'x' or 'y'
    if orient == 'x':
        sobel = cv2.Sobel(gray, cv2.CV_64F,1, 0)
    else:
        sobel = cv2.Sobel(gray, cv2.CV_64F, 0, 1)
    # 3) Take the absolute value of the derivative or gradient
    abs_sobel = np.abs(sobel)
    # 4) Scale to 8-bit (0 - 255) then convert to type = np.uint8
    scaled_sobel = np.uint8(255*abs_sobel/np.max(abs_sobel))
    # 5) Create a mask of 1's where the scaled gradient magnitude 
            # is > thresh_min and < thresh_max
    binary_output = np.zeros_like(scaled_sobel)
    #import pdb; pdb.set_trace()
    binary_output[(scaled_sobel >= thresh_min) & (scaled_sobel <= thresh_max)] = 1
    # 6) Return this mask as your binary_output image

    return binary_output

if __name__ == "__main__":
    from calibration import calibrate, undistort
    from unwraped import unwraped
    import matplotlib.image as mpimg
    img = mpimg.imread("test_images/test1.jpg")
    #img = cv2.imread("test_images/test1.jpg")
    img_size = (img.shape[0], img.shape[1])

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #cv2.imwrite('examples/gray_1.png', gray)

    ret, mtx, dist, rvecs, tvecs = calibrate(gray, 6, 9)
    undistort_img = undistort(img, mtx, dist)
    #cv2.imwrite('examples/undistort_img_1.png', undistort_img)
    
    #gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)


    unwraped_img = unwraped(undistort_img, img_size)
    hls = cv2.cvtColor(unwraped_img, cv2.COLOR_RGB2HLS).astype(np.float)
    l_channel = hls[:,:,1]
    s_channel = hls[:,:,2]
    x_binary_output = abs_sobel_thresh(unwraped_img, orient='x', thresh_min=20, thresh_max=100)
    cv2.imwrite('examples/sobel_x_1.png', x_binary_output)
    cv2.imwrite('examples/sobel_y_1.png', y_binary_output)
    l_chanel_output = abs_sobel_thresh(l_channel, orient='x', thresh_min=20, thresh_max=255)
    cv2.imwrite('examples/l_chanel_1.png', l_chanel_output)
