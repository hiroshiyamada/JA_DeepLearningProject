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
output_dir = parent_dir + "rectified_movie/"

cap_left= cv2.VideoCapture(parent_dir + "left.avi")
cap_right = cv2.VideoCapture(parent_dir + "right.avi")

if not (cap_left.isOpened() and cap_right.isOpened()):
    print "movies not found."
    exit(1)

fourcc = int(cap_left.get(cv2.cv.CV_CAP_PROP_FOURCC))
fps = cap_left.get(cv2.cv.CV_CAP_PROP_FPS)
height = int(cap_left.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
width = int(cap_left.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
size = (width,height)

map1_left = np.load(mapfile_dir + "map1_left.npy")
map1_right = np.load(mapfile_dir + "map1_right.npy")
map2_left = np.load(mapfile_dir + "map2_left.npy")
map2_right = np.load(mapfile_dir + "map2_right.npy")

video_left = cv2.VideoWriter(parent_dir + "left_rectified.avi",fourcc,30,size)
video_right = cv2.VideoWriter(parent_dir + "right_rectified.avi",fourcc,30,size)

if not (video_left.isOpened() and video_right.isOpened()):
    print "Failed to create video files"
    exit(1)

while True:
    ret_left, frame_left = cap_left.read()
    ret_right, frame_right = cap_right.read()

    if not (ret_left and ret_right):
        break

    frame_left = cv2.remap(frame_left,map1_left,map2_left,cv2.INTER_LINEAR)
    frame_right = cv2.remap(frame_right,map1_right,map2_right,cv2.INTER_LINEAR)

    video_left.write(frame_left)
    video_right.write(frame_right)

    frame_size = frame_left.shape[1::-1]
    frame_size = (frame_size[0]/2,frame_size[1]/2)
    frame_left = cv2.resize(frame_left,frame_size)
    frame_right = cv2.resize(frame_right,frame_size)
    cv2.imshow("frame_left",frame_left)
    cv2.imshow("frame_right",frame_right)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap_left.release()
cap_right.release()
cv2.destroyAllWindows()
