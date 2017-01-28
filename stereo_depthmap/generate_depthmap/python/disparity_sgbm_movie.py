import numpy as np
import cv2
import sys
import os

if not len(sys.argv) > 1:
    print "USAGE: python rectification.py path_to_parent_dir"
    exit(0)



def compute_disparity(StereoSGBM,img_left,img_right):
    disparity = stereoSGBM.compute(img_left,img_right)
    disparity = cv2.normalize(disparity, disparity,alpha=1, beta=100, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)

    disparity = np.reciprocal(disparity)

    disparity = cv2.normalize(disparity, disparity,alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

    disparity = cv2.applyColorMap(disparity, cv2.COLORMAP_HOT)

    return disparity

parent_dir = sys.argv[1] + "/"
output_dir = parent_dir + "rectified_movie/"

cap_left= cv2.VideoCapture(parent_dir + "left_rectified.avi")
cap_right = cv2.VideoCapture(parent_dir + "right_rectified.avi")

if not (cap_left.isOpened() and cap_right.isOpened()):
    print "movies not found."
    exit(1)

fourcc = int(cap_left.get(cv2.cv.CV_CAP_PROP_FOURCC))
fps = cap_left.get(cv2.cv.CV_CAP_PROP_FPS)
height = int(cap_left.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
width = int(cap_left.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
size = (width,height)

video_disparity = cv2.VideoWriter(parent_dir + "disparity.avi",fourcc,30,size)

if not video_disparity.isOpened():
    print "Failed to create video files"
    exit(1)

max_disparity = 256 ## should be divisible by 16
grid_size = 7
uniqueness = 14

stereoSGBM = cv2.StereoSGBM(0,max_disparity,grid_size,uniquenessRatio=uniqueness)

while True:
    ret_left, frame_left = cap_left.read()
    ret_right, frame_right = cap_right.read()

    if not (ret_left and ret_right):
        break

    frame_disparity = compute_disparity(stereoSGBM,frame_left,frame_right)

    print frame_disparity.shape

    video_disparity.write(frame_disparity)

    frame_size = frame_left.shape[1::-1]
    frame_size = (frame_size[0]/2,frame_size[1]/2)
    frame_left = cv2.resize(frame_left,frame_size)
    frame_disparity = cv2.resize(frame_disparity,frame_size)
    cv2.imshow("frame_left",frame_left)
    cv2.imshow("frame_disparity",frame_disparity)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap_left.release()
cap_right.release()
cv2.destroyAllWindows()
