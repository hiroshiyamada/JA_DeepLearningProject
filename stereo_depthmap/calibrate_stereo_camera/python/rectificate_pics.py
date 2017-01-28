import numpy as np
import cv2
import sys
import os 

if not len(sys.argv) > 1:
    print "USAGE: python rectification.py path_to_parent_dir"
    exit(0)

parent_dir = sys.argv[1] + "/"
calib_pics_dir = parent_dir + "calib_pics/"
mapfile_dir = parent_dir + "stereo_params/"
output_dir = parent_dir + "rectified_pics/"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

map1_left = np.load(mapfile_dir + "map1_left.npy")
map1_right = np.load(mapfile_dir + "map1_right.npy")
map2_left = np.load(mapfile_dir + "map2_left.npy")
map2_right = np.load(mapfile_dir + "map2_right.npy")
    
for ii in range(1,51):
    img_left = cv2.imread(calib_pics_dir + "left_%02d.ppm"%ii)
    img_right = cv2.imread(calib_pics_dir + "right_%02d.ppm"%ii)

    img_left = cv2.remap(img_left,map1_left,map2_left,cv2.INTER_LINEAR)
    img_right = cv2.remap(img_right,map1_right,map2_right,cv2.INTER_LINEAR)

    cv2.imwrite(output_dir + "left_%02d.ppm"%ii,img_left)
    cv2.imwrite(output_dir + "right_%02d.ppm"%ii,img_right)

    img_size = img_left.shape[1::-1]
    img_size = (img_size[0]/2,img_size[1]/2)
    img_left = cv2.resize(img_left,img_size)
    img_right = cv2.resize(img_right,img_size)
    cv2.imshow("img_left",img_left)
    cv2.imshow("img_right",img_right)
    cv2.waitKey(0)

