# Adapted from: TNEL Matlab struct viewer by Jon Whear on 18Nov2021
# This Version Updated 26Jan2022 by Jon Whear
import scipy.io as scio
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from tkinter.filedialog import askopenfilename
import dev_cam as cam
import os


# What is Matlab cleandata struct file path?
# At current time, open /cleandata_struct.mat
matlab_file_path = askopenfilename()

# r'D:\EPHYSDATA\TESTS\Threading2\RAW_PRE_TESTS_Threading2_cleandata_struct.mat'

# Define what we are looking for in log_file.mat file
mat_log_file = scio.loadmat(matlab_file_path)
record_dir_char = 'record_dir'
rat_char = 'rat'
day_char = 'day'
paths_char = 'paths'
raw_time_char = 'rawTime'

# Specify structure to search MatLab files for char information
mat_log_record_dir = mat_log_file[record_dir_char]
mat_log_rat = mat_log_file[rat_char]
mat_log_day = mat_log_file[day_char]
mat_log_paths = mat_log_file[paths_char]
mat_log_raw_time = mat_log_file[raw_time_char]

# Specify exact location to find each char
record_dir = mat_log_record_dir[0]
rat = mat_log_rat[0]
day = mat_log_day[0]
paths = mat_log_paths #[0]
raw_time = mat_log_raw_time[0][0]
print(raw_time)

# Strip excess spaces in path names
paths = [i.strip(' ') for i in paths]

# Will need to create a way to read this from log_file.mat and use that logic to determine seconds
seconds = raw_time*60

for condition in paths:
    data_dir = '{}\{}_{}_{}_cleandata_struct.mat'.format(record_dir,condition,rat,day)
    mat_file = scio.loadmat(data_dir)
    struct_name_lvl1 = 'cur_data'
    struct_name_lvl2 = 'ds_data'

    mat_file = mat_file[struct_name_lvl1]
    mat_file = mat_file[struct_name_lvl2]

    cleandata_matlab_struct = mat_file[0][0]
    if not os.path.exists(r'{}\accel_png'.format(record_dir)):
        output_path = os.mkdir(r'{}\accel_png'.format(record_dir))
    png_path = r'{}\accel_png'.format(record_dir)
    cam.create_accel_png(rat,day,cleandata_matlab_struct,png_path,seconds,condition)
    cam.overlay_accel('{}\\{}_{}_{}.avi'.format(record_dir,condition,rat,day),rat,day,png_path,'{}\{}{}{}_accel.avi'.format(record_dir,condition,rat,day,))
