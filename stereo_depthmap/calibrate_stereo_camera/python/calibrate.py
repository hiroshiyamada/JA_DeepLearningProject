import numpy as np
import cv2
import glob
import sys
import os 

if not len(sys.argv) > 1:
    print "USAGE: python calibration.py path_to_parent_dir"
    exit(1)

def is_opencv_v3():
    return cv2.__version__.startswith("3")
    
parent_dir = sys.argv[1] + "/"
calib_pics_dir = parent_dir + "calib_pics/"
output_dir = parent_dir + "stereo_params/"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

chessboard_width = 9
chessboard_height = 6

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((chessboard_height*chessboard_width,3), np.float32)
objp[:,:2] = np.mgrid[0:chessboard_width,0:chessboard_height].T.reshape(-1,2)

objp = objp*2.1

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints_left = [] # 2d points in image plane.
imgpoints_right = [] # 2d points in image plane.

images_left = glob.glob(calib_pics_dir + 'left_*.ppm')
images_right = glob.glob(calib_pics_dir + 'right_*.ppm')

if len(images_left) == 0 or len(images_right) == 0:
    print "Pictures not found in " +  calib_pics_dir
    exit(0)

def show_chessboard_corners(img):
    img = cv2.drawChessboardCorners(img, (chessboard_width,chessboard_height), corners,ret)
    cv2.imshow('%s'%fname,img)
    cv2.waitKey(0)
    cv2.destroyWindow('%s'%fname)    
    
def chessboard_corners(imgs):
    imgpoints = []
    for fname in imgs:
        img = cv2.imread(fname)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(img, (chessboard_width,chessboard_height),None)

        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)
            imgpoints.append(corners)
            # show_chessboard_corners(img)

    return objpoints, imgpoints, img.shape[1::-1]

objpoints, imgpoints_left, size = chessboard_corners(images_left)
objpoints, imgpoints_right, size = chessboard_corners(images_right)
objpoints = objpoints[0:len(objpoints)/2]
img_size = size

def show_undistort_images(imgs, K, d):
    for fname in imgs:
        img = cv2.imread(fname)
        img = cv2.undistort(img,K,d)

        img_size = img.shape[1::-1]
        img_size = (img_size[0]/2,img_size[1]/2)
        img = cv2.resize(img,img_size)

        cv2.imshow('img',img)
        cv2.waitKey(0)

rms_left, camMat_left, distCoef_left, r_left, t_left = cv2.calibrateCamera(objpoints,imgpoints_left,img_size,None,None,flags=cv2.CALIB_FIX_ASPECT_RATIO,criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 100, 1e-6))

print "camMat_left_init"
print camMat_left
print "distCoef_left_init"
print distCoef_left

np.save(output_dir + "camMat_left_init.npy",camMat_left)
np.save(output_dir + "distCoef_left_init.npy",distCoef_left)

#show_undistort_images(images_left,camMat_left,distCoef_left)

rms_right, camMat_right, distCoef_right, r_right, t_right = cv2.calibrateCamera(objpoints,imgpoints_right,img_size,None,None,flags=cv2.CALIB_FIX_ASPECT_RATIO,criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 100, 1e-6))

print "camMat_right_init"
print camMat_right
print "distCoef_right_init"
print distCoef_right

# K_left = camMat_left
# K_right = camMat_right
# d_left = distCoef_left
# d_right = distCoef_right

np.save(output_dir + "camMat_right_init.npy",camMat_right)
np.save(output_dir + "distCoef_right_init.npy",distCoef_right)

#show_undistort_images(images_right,camMat_right,distCoef_right)

# for OpenCV 3.1
#retval, camMat_left, distCoef_left, camMat_right, distCoef_right,R,T,E,F = cv2.stereoCalibrate(objpoints,imgpoints_left,imgpoints_right,camMat_left,distCoef_left,camMat_right,distCoef_right,img_size,flags=cv2.CALIB_USE_INTRINSIC_GUESS | cv2.CALIB_SAME_FOCAL_LENGTH | cv2.CALIB_FIX_ASPECT_RATIO,criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 100, 1e-6))

retval, camMat_left, distCoef_left, camMat_right, distCoef_right,R,T,E,F = cv2.stereoCalibrate(objpoints,imgpoints_left,imgpoints_right,img_size,camMat_left,distCoef_left,camMat_right,distCoef_right,flags=cv2.CALIB_USE_INTRINSIC_GUESS | cv2.CALIB_SAME_FOCAL_LENGTH | cv2.CALIB_FIX_ASPECT_RATIO,criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 100, 1e-6))

print "retval"
print retval
print "camMat_left"
print camMat_left
print "distCoef_left"
print distCoef_left
print "camMat_right"
print camMat_right
print "distCoef_right"
print distCoef_right
print "R"
print R
print "T"
print T
print "E"
print E
print "F"
print F

np.save(output_dir + "camMat_left.npy",camMat_left)
np.save(output_dir + "distCoef_left.npy",distCoef_left)
np.save(output_dir + "camMat_right.npy",camMat_right)
np.save(output_dir + "distCoef_right.npy",distCoef_right)
np.save(output_dir + "R.npy",R)
np.save(output_dir + "T.npy",T)
np.save(output_dir + "E.npy",E)
np.save(output_dir + "F.npy",F)

R1 = np.zeros(shape=(3,3))
R2 = np.zeros(shape=(3,3))
P1 = np.zeros(shape=(3,4))
P2 = np.zeros(shape=(3,4))

R1, R2, P1, P2, Q, ROI1, ROI2 = cv2.stereoRectify(camMat_left, distCoef_left, camMat_right, distCoef_right,img_size, R, T, R1, R2, P1, P2, Q=None, flags=cv2.CALIB_ZERO_DISPARITY, alpha=-1, newImageSize=(0,0))

print "R1"
print R1
print "P1"
print P1
print "R2"
print R2
print "P2"
print P2

map1_left,map2_left = cv2.initUndistortRectifyMap(camMat_left,distCoef_left,R1,P1,img_size,cv2.CV_32FC1)
map1_right,map2_right = cv2.initUndistortRectifyMap(camMat_right,distCoef_right,R2,P2,img_size,cv2.CV_32FC1)
# map1_left,map2_left = cv2.initUndistortRectifyMap(K_left,d_left,R1,P1,img_size,cv2.CV_32FC1)
# map1_right,map2_right = cv2.initUndistortRectifyMap(K_right,d_right,R2,P2,img_size,cv2.CV_32FC1)

print "map1_left"
print map1_left
print "map2_left"
print map2_left
print "map1_right"
print map1_right
print "map2_right"
print map2_right

np.save(output_dir + "map1_left.npy",map1_left)
np.save(output_dir + "map1_right.npy",map1_right)
np.save(output_dir + "map2_left.npy",map2_left)
np.save(output_dir + "map2_right.npy",map2_right)
