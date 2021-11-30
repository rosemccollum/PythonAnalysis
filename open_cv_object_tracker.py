### Select ROI and have OpenCV track location and save to log file
# Updated Nov 24
#### This tutorial is really good https://www.youtube.com/watch?v=1FJWXOO1SRI

from time import time
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib as plt
import cv2 #Import openCV
import datetime

# Create a VideoCapture object - 0 is the default setting for built in camera
cap = cv2.VideoCapture(0)
tracker = cv2.legacy.TrackerMOSSE_create()
# tracker = cv2.TrackerCSRT_create()
success, img = cap.read()
bbox = cv2.selectROI("Tracking",img,False)
tracker.init(img,bbox)

# Start a recording timer
start_time = datetime.datetime.now()

x_list = []
y_list = []
w_list = []
h_list = []
time_list = []

# Do this once so there is a 0.0 mark
run_time_sec = 0

def drawBox(img,bbox):
    x,y,w,h = int(bbox[0]),int(bbox[1]),int(bbox[2]),int(bbox[3])
    cv2.rectangle(img,(x,y),((x+w),(y+h)),(255,0,255),3,1) #15:00min
    cv2.putText(img,"Tracking",(75,75),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)
    x_list.append(x)
    y_list.append(y)
    w_list.append(w)
    h_list.append(h)
    time_list.append(run_time_sec)
    df = pd.DataFrame({'x':x_list, 'y':y_list,'w':w_list,'h':h_list,'run_time':time_list})
    df.to_csv('tracking_data.csv')

while True:
    timer  = cv2.getTickCount()
    success, img = cap.read()
    success, bbox = tracker.update(img)
    print(bbox)
    if success:
        drawBox(img,bbox)

    else:
        cv2.putText(img,"Lost",(75,75),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)

    fps = cv2.getTickFrequency()/(cv2.getTickCount()-timer)
    cv2.putText(img,str(int(fps)),(75,50),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
    cv2.imshow("Tracking",img)
    cur_time = datetime.datetime.now()
    run_time = cur_time - start_time
    run_time_sec = run_time.total_seconds()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
