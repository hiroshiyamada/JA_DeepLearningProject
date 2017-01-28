import cv2
def capture_camera(mirror=True, size=None):
    """Capture video from camera"""
    cap0 = cv2.VideoCapture(0)
    cap1 = cv2.VideoCapture(1)

    while cap0.isOpened() and cap1.isOpened():
        ret0, frame0 = cap0.read()
        ret1, frame1 = cap1.read()

        # print ret0, ret1

        if not (ret0 and ret1):
            continue

        img_size = frame0.shape[1::-1]
        img_size = (img_size[0]/2,img_size[1]/2)
        img0 = cv2.resize(frame0,img_size)
        img1 = cv2.resize(frame1,img_size)
        cv2.imshow("img0",img0)
        cv2.imshow("img1",img1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap0.release()
    cap1.release()
    cv2.destroyAllWindows()

capture_camera()
