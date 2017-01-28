import numpy as np
import cv2

cap0= cv2.VideoCapture(0)
cap1 = cv2.VideoCapture(1)

def is_opencv_v3():
    return cv2.__version__.startswith("3")

if is_opencv_v3():
    cap0.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
    cap0.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)
    cap1.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
    cap1.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)
else:
    cap0.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,1920)
    cap0.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,1080)
    cap1.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,1920)
    cap1.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,1080)

width0 = cap0.get(cv2.CAP_PROP_FRAME_WIDTH) if is_opencv_v3() else cap0.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
height0 = cap0.get(cv2.CAP_PROP_FRAME_HEIGHT) if is_opencv_v3() else cap0.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
width1 = cap1.get(cv2.CAP_PROP_FRAME_WIDTH) if is_opencv_v3() else cap1.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
height1 = cap1.get(cv2.CAP_PROP_FRAME_HEIGHT) if is_opencv_v3() else cap1.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)

ret0 = ret1 = False
frame0 = frame1 = 0
while ret0 is False or ret1 is False:
    ret0, frame0 = cap0.read()
    ret1, frame1 = cap1.read()

size0 = frame0.shape[1::-1]
size1 = frame1.shape[1::-1]
print size0, size1

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'X264') if is_opencv_v3() else cv2.cv.CV_FOURCC(*'MJPG')
out0 = cv2.VideoWriter('output0.avi',fourcc, 30.0, size0)
out1 = cv2.VideoWriter('output1.avi',fourcc, 30.0, size1)
while(True):
    # Capture frame-by-frame
    ret0, frame0 = cap0.read()
    ret1, frame1 = cap1.read()

    if ret0 and ret1:
        frame0 = cv2.flip(frame0,-1)
        frame1 = cv2.flip(frame1,-1)

        out0.write(frame0)
        out1.write(frame1)

        # Display the resulting frame
        cv2.imshow('frame0',frame0)
        cv2.imshow('frame1',frame1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        print "Frame dropped"
        break
    # When everything done, release the capture
cap0.release()
cap1.release()
cv2.destroyAllWindows()

