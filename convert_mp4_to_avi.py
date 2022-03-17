# Written by JHW on 03Feb2022 to convert MP4 to avi in a codec usable by AnyMaze
# Modified 25Feb2022 - Uses os.path (the correct way to join paths, and works on all os's)

import os

import cv2
import numpy as np

### Path Selection ###
mp4_file_path = r'C:\Users\Ephys\Pictures\Camera Roll\rats_24Feb2022\dev2110\mp4'
png_file_path = r'C:\Users\Ephys\Pictures\Camera Roll\rats_24Feb2022\dev2110\png'
avi_file_path = r'C:\Users\Ephys\Pictures\Camera Roll\rats_24Feb2022\dev2110\avi'

### Name of Recording ###
file_name = r'dev2110_24Feb2022'

### Final Path for Read/Write Locations ###
mp4_path = os.path.join(mp4_file_path, file_name + '.mp4')
png_path = os.path.join(png_file_path, file_name + '.png')
avi_path = os.path.join(avi_file_path, file_name + '.avi')

### Number of Frames ### - 30*60*minutes [18000 for 10 minutes @ 30fps]
frames = 18000

def convert_mp4_to_png(mp4_path, png_path):
    cap = cv2.VideoCapture(mp4_path)
    fourcc = cv2.VideoWriter_fourcc(*'MJPG') # Was MJPG
    fps = 30
    writer = cv2.VideoWriter(png_path, fourcc, fps, (640, 480))

    for i in range(frames):
        ret, frame = cap.read()
        cv2.imwrite('{}\\avi{}.png'.format(png_file_path,i), frame)
        print('.png Writing Percent Complete: ' + str(i/frames*100))

def create_avi(png_file_path, avi_file_path):
    fps = 30
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    writer = cv2.VideoWriter('{}\\WIN_20220203_10_22_19_Pro_converted_30fps.avi'.format(avi_file_path), fourcc, fps,(1920, 1080))

    for i in range(frames):
        img = cv2.imread('{}\\avi{}.png'.format(png_file_path, i))
        writer.write(img)
        print('.avi Writing Percent Complete: ' + str(i/frames*100))

    writer.release()
    cv2.destroyAllWindows()
    print('Done!')

if __name__ == '__main__':
    print('Creating .png from .mp4')
    convert_mp4_to_png(mp4_path, png_path)
    print('creating .avi from .png')
    create_avi(png_file_path, avi_file_path)
