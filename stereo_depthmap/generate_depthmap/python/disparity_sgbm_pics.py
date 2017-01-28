import cv2
import numpy as np
import sys
import os

if not len(sys.argv) > 1:
    print "USAGE: python disparity_sgbm.py path_to_parent_dir"
    exit(0)

parent_dir = sys.argv[1] + "/"
rectified_pics_dir = parent_dir + "rectified_pics/"
output_dir = parent_dir + "disparity_pics/"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def compute_disparity(StereoSGBM,img_left,img_right,setting):
    disparity = stereoSGBM.compute(img_left,img_right)
    disparity = cv2.normalize(disparity, disparity,alpha=1, beta=100, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)

    disparity = np.reciprocal(disparity)

    disparity = cv2.normalize(disparity, disparity,alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    
    disparity = cv2.applyColorMap(disparity, cv2.COLORMAP_HOT)

    img_size = disparity.shape[1::-1]
    img_size = (img_size[0]/3,img_size[1]/3)
    img_left = cv2.resize(img_left,img_size)
    img_right = cv2.resize(img_right,img_size)
    disparity = cv2.resize(disparity,img_size)

    # cv2.imshow("img_left",img_left)
    # cv2.imshow("img_right",img_right)
    # cv2.imshow("disparity",disparity)
    # cv2.waitKey(0)
    cv2.imwrite(output_dir + "%d-%d-%d_%d.png"%(setting),disparity)

for max_disparity_power in range(8,10):
    max_disparity = 2**max_disparity_power
    for grid_size in range(1,11,2):
        for uniqueness in range(2,20,4):
            stereoSGBM = cv2.StereoSGBM(0,max_disparity,grid_size,uniquenessRatio=uniqueness)
            for ii in range(16,17):
                setting = (max_disparity,grid_size,uniqueness,ii)
                img_left = cv2.imread(rectified_pics_dir + "left_%02d.ppm"%ii)
                img_right = cv2.imread(rectified_pics_dir + "right_%02d.ppm"%ii)
                compute_disparity(stereoSGBM,img_left,img_right,setting)
