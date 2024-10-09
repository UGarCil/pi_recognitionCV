#!usr/bin/env/python
'''
This program was created on Dec. 12th 2020 by Uriel Garcilazo Cruz. It produces a motion detector
from a live view using a GOPRO HERO4 as input with ELGATO CAMLINK.

This script differs from those already found in this folder in the source of information taken as a tutorial.
source: https://www.youtube.com/watch?v=MkcUgPhOlP8&ab_channel=ProgrammingKnowledge
The type of motion detection changes as well. Intead of using the initial frame as a reference, it
updates the frame before taking the next one, evaluating the difference and identifying the motion.

Some relevant information regarding the file duration:
The cutoff of the files is not given by recording time but file size.
You might want to make a test to see how many megabytes is 1 second in your recordings.
I got 7.26 MB : 1 sec. For 5 min, the cutoff should be around 2000.
The cutoff can be found in the variable named desired_files_size

This version V8 was created with the intention to customize the script to take the higher resolutions of a GoPro
connected to a UVC card reader with a maximum output of 1920 x 1080.

I returned the USV card form Toscomax and bought a camlink instead. The resolution should be now the same as GoPro4:
4K: 3840 x 2160
2.7K: 2704 x 1520
1440p: 1920 x 1440
1080p: 1920 x 1080

The program opens and saves the image with its native resolution. It's important to remember to match the
camera resolution to the given resolution.

V9 works from a functional version of V8. It adds however argparse to be able to run form the command promt.

To run this script, go to the folder using cd in batch at the CMD prompt. There, run:
conda activate opencvenv
python V9_motion_detector.py -r <your_res>

V10 deals with the fps and frame ratio of different resolutions of the GoPro Silver 4.
In particular, I experienced issues with the 960p because the ratio of width/height distorted the animals being recorded.
Also, the fps was fixed to 30fps, which is not desirable if we want to record high speed.

V11 There are some issues with the current V10, which doesn't find the camera from time to time, especiall using the GoPro5 Black edition at 4K 30fps.
The version V11 is inteded to troubleshoot.
'''

##For changing the video capture from cv2 follow C:\Python35\lib\site-packages\imutils\video\webcamvideostream.py -> class WebcamVideoStream -> self.stream = cv2.VideoCapture(#)
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2
from os.path import join as jn
import os

##Set the variables from argparse
parser = argparse.ArgumentParser(description='Start motion detection with GOPRO+CAMLINK at a given resolution')
parser.add_argument('-r','--res', type=str, help='4K/2_7K/1440p/1080p/960p/720p/480p')
args = parser.parse_args()
print(args)
working_path = r"D:\Garcilazo\Python\00Exercises\images_for_CV2\DEC2020_Motion_detector"
os.chdir(working_path)
# vs = VideoStream(src=1).start()
# VideoStream(src=1).start()
# time.sleep(2)
min_area = 1000 #The lowest (~20) the finest and higher number of squares. It will also depend on the resolution.
'''
For 4K 1500
For 2.7K 1200
For 1440p 1000
For 1080p 700
'''


# Details on the size of the video file to save
# I use cv2 in this script only to get the width and height of the frame
cap = cv2.VideoCapture(0) #CamLink is channel 4 when no other webcam is connected, or sometimes 2

# Changing the resolution
res = '4K'

'''DONT' FORGET TO ADJUST THE CAMERA RESOLUTION MANUALLY!!!'''

prefix = "timelapse"

GOPROres = [{'name':'4K', 'width':3840, 'height':2160, 'fps':30},
            {'name':'2_7K', 'width':2704, 'height':1520, 'fps':30},
            {'name':'1440p', 'width':2704, 'height':1520, 'fps':48},
            {'name':'1080p', 'width':1920, 'height':1080, 'fps':60},
            {'name':'960p', 'width':1280, 'height':960, 'fps':100},
            {'name':'720p', 'width':1280, 'height':720, 'fps':120},
            {'name':'480p', 'width':848, 'height':480, 'fps':240}]

set_res = [(x['width'],x['height'],x['fps']) for x in GOPROres if x['name']==res][0]
width = set_res[0]
height = set_res[1]
fps = set_res[2] #I'm not really using this in the script. It was used to specify the fps to write audio file but made it too fast. Better to keep at 30fps in the variable result

ret, frame1 = cap.read()
ret, frame2 = cap.read()
while True:
    # imS0 = cv2.resize(frame1, (int(width/3),int(height/3)))
    cv2.imshow("Security Feed", frame1)
        # cv2.imshow("Thresh", thresh)
        # cv2.imshow("Frame Delta", frameDelta)
        
    frame1 = frame2
    ret, frame2 = cap.read()

    
    key = cv2.waitKey(1) & 0xFF
    
    # if the `q` key is pressed, break from the lop
    if key == ord("q"):
        end_script = True
        break


#Set the camera to the parameters of the input camera resolution
# cap.set(cv2.CAP_PROP_FPS, fps)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


size = (width, height)


# capture.set(cv2.CAP_PROP_FOURCC, fourcc)


# size = (640,480) #ratio is 1.33:1 width to height
# width = 3840
# height = int(width/1.33)
# size = (width,height)

# initialize the first frame in the video stream
firstFrame = None

# Decide the file number to allocate the video.
if 'video_lapse' not in os.listdir(working_path):
    os.mkdir(jn(working_path,'video_lapse'))

vidlapse_storage = jn(working_path,'video_lapse')

ret, frame1 = cap.read()
ret, frame2 = cap.read()


stop_recording_nomotion = 5 #time difference in seconds to keep recording after no motion has been detected...
desired_files_size = 500 #value given in Megabytes. 2000 is around 5 min. of recording at low resolutions
#Loop over the time lapse videos saved based on their duration
new_avi_time = 40 #time in seconds each timelapse will last
end_script = False


while not end_script:
    print('running')
    files = [int(x.replace('.avi','').split('_')[1]) for x in os.listdir(vidlapse_storage) if prefix in x]
    if len(files) == 0:
        ext = '1'
    else:
        ext = max(files) + 1
    result = cv2.VideoWriter('filename2.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10, size)
    file_name = 'video_lapse\{}_{}_{}.mp4'.format(prefix,ext,res)
    result = cv2.VideoWriter(file_name, cv2.VideoWriter_fourcc(*'MP4V'), fps,size)
    first_rec = True
    size_file = 0

    while size_file <= desired_files_size:
    
        text = ""

        if frame1 is None:
            break
        
        diff = cv2.absdiff(frame1,frame2)
        
        # resize the frame, convert it to grayscale, and blur it
        # frame = imutils.resize(frame, width=800)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (21, 21), 0)
        
        # compute the absolute difference between the current frame and
        # first frame
        thresh = cv2.threshold(blur, 25, 255, cv2.THRESH_BINARY)[1]
        
        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        dilated = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[1]
        # print(len(cnts))



        # else:
            # result.release()
            # None
    # draw the text and timestamp on the frame

        # cv2.putText(frame1, "test".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2) #commented to avoid the title of the frame to appear in the recorded video
        cv2.putText(frame1, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame1.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        if first_rec:
            if len(cnts) !=0:
                # ret, framecv = cap.read()
                start_clock = time.time()
                # print(count)
                b = cv2.resize(frame1,(width,height),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
                result.write(b)
                first_rec = False

        else:
            if len(cnts) !=0:
                # ret, framecv = cap.read()
                start_clock = time.time()
                # print(count)
                b = cv2.resize(frame1,(width,height),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
                result.write(b)
            
            elif  int(time.time() - start_clock) < stop_recording_nomotion:
                b = cv2.resize(frame1,(width,height),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
                result.write(b)
                # pass

            else:
                None



        # loop over the contours
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < min_area:
                continue
    
            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = ""
        

        # resize and show the frame and record if the user presses a key
        # factor = 2 #Integer that shrinks an image by that factor when shown in monitor
        imS0 = cv2.resize(frame1, (int(width/3),int(height/3)))
        cv2.imshow("Security Feed", imS0)
        # cv2.imshow("Thresh", thresh)
        # cv2.imshow("Frame Delta", frameDelta)
        

        frame1 = frame2
        ret, frame2 = cap.read()

    
        key = cv2.waitKey(1) & 0xFF
    
        # if the `q` key is pressed, break from the lop
        if key == ord("q"):
            end_script = True
            break
        # size_file = os.path.getsize(file_name)/1000000 # Size in Mbytes
        # print(size_file)
    result.release()
# cleanup the camera and close any open windows
# vs.stop() #if args.get("video", None) is None else vs.release()
result.release()
cv2.destroyAllWindows()