import cv2
import imutils

################ DATA DEFS ##################
# DD. CAPTURE
# cap = cv2.VideoCapture(int)
# interp. the capture of the webcam, video or streaming device, registered in the user's computer
cap = cv2.VideoCapture(0)

# DD. FIRST
# firstFrame = [[[int, int, int],...],...]
# interp. an array of pixels representing the first frame of video input
firstFrame = None

MIN_AREA = 1200

# frame1 = cap.read()
# frame2 = cap.read()

################ CODING SECTION #############

def readCamera(w,h):
    global frame1
    global frame2

    # Read CAPTURE to get 3D array of pixels
    _, frame1 = cap.read()
    frame1 = cv2.resize(frame1, (w,h))
    frame1 = cv2.flip(frame1, 1)
    _, frame2 = cap.read()
    frame2 = cv2.resize(frame2, (w,h))
    frame2 = cv2.flip(frame2, 1)

    # compute the absolute difference between the current frame and
    # first frame
    diff = cv2.absdiff(frame1, frame2)

    # resize the frame, convert it to grayscale, and blur it
    # frame = imutils.resize(frame, width=800)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (21, 21), 0)

    # compute the absolute difference between the current frame and
    # first frame
    thresh = cv2.threshold(blur, 25, 255, cv2.THRESH_BINARY)[1]
    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[1] if imutils.is_cv2() else cnts[0]

    # loop over the contours
    if len(cnts) > 0:
        # pick the square with the biggest area
        bigg_Area = 0
        (bx, by, bw, bh) = (0 for it in range(4))
        for idx, c in enumerate(cnts):
            (x, y, w, h) = cv2.boundingRect(c)
            if w*h > bigg_Area:
                big_IDX = idx
                (bx, by, bw, bh) = (x, y, w, h)
        return(bx + (bw//2),by + (bh//2))
    else:
        return (None)
    
    
