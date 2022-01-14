# NOTE: This version has not officially been saved as dev_cam.py, but is under open_cv_demo.py on Jon's computer until it is finished
# Existing version of dev_cam.py contains some additional functions and classes for recording
##
##
import cv2
from datetime import datetime

foreground = r'D:\EPHYSDATA\TESTS\OpenCV\coh.PNG'
image = cv2.imread(foreground)
scale_percent = 40 # percent of the original image
height = int(image.shape[0] * scale_percent / 100)
width = int(image.shape[1] * scale_percent / 100)
dim = (width,height)
image_resized = cv2.resize(image,dim, interpolation = cv2.INTER_AREA)
# cv2.imshow('Test',image_resized)
print('Image size is: '+str(image_resized.shape)) # this should be about 200*250

# This is what I added for 
def run_rec(camera, path, rat, day, cond): # Takes rat,day, and condition to overlay on video
    cap = cv2.VideoCapture(camera)
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    width= int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height= int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = 30
    writer = cv2.VideoWriter(path, fourcc, fps, (640,  480))
    # Overlayed image will go here
    img_loc = r''
    font = cv2.FONT_HERSHEY_SIMPLEX
    alpha = 0.4

    while(cap.isOpened()):
        ret, frame = cap.read()
        # added_image can be changed to another name in the future
        # Select the region in the background where we want to add the image and add the images using cv2.addWeighted()
        added_image = cv2.addWeighted(frame[280:480,440:640,:],alpha,image_resized[0:200,0:200,:],1-alpha,0)
        # Change the region with the result
        # It will be nice in the future to find a way to turn these into vars so they don't need to be changed frequently
        frame[280:480,440:640] = added_image # X then Y
        cv2.putText(frame,str(rat+day+cond),(5,20),font,0.7,(0,0,255),1) # Color is in BGR
        cv2.putText(frame,str(datetime.now()),(5,40),font,0.5,(0,0,255),1) # Location format is X,Y
        writer.write(frame)
        cv2.imshow('TNEL Dev. Proj '+rat+day,frame)
        # Show the frame
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            writer.release()
            cv2.destroyAllWindows()
            print(path+' Video Saved Successfully!')
            break


if __name__ == '__main__': # This is here for de-bugging and testing only
    record_dir = 'D:\EPHYSDATA\TESTS\OpenCV'
    rat='dev2999'
    day = 'day1000'
    run_rec(0,record_dir + "\\RAW_PRE"+rat+day+".avi",rat,day,'RAW_PRE')
