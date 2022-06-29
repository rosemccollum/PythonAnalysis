### Import Dependencies ###
from scipy.signal import hilbert, filtfilt, butter
from scipy.stats import circmean, circvar
import scipy.io as scipy
import numpy as np
from numpy import angle
import os
import pandas as pd
import mat73
import seaborn as sns
import matplotlib.pyplot as plt

### Define Data Location and Settings ###
drive = r'Z:\projmon\virginia-dev'
location = '01_EPHYSDATA'
rat = 'eric_data'
day = 'eric_rat'
condition = "CLOSED_LOOP_2021-11-17_14-22-15" # Include the entire name
hidden = 'hidden' # For files moved so that dev Matlab pathway doesn't run on CL section
data_dir = os.path.join(drive, location, rat, day, condition, 'Phase_Data.mat') # os.path.join() is easiest way to work with paths between unix / windows systems
data_dict = mat73.loadmat(data_dir) # mat73 allows importing matlab v7.3 files (scipy does not currently support)
fs = 500 # sampling rate (default: 30000)
coi = 12 # Channel of Interest (coi)
bins = 24 # number of bins in the rose plot
lowpass = 4 # Hz
highpass = 8 # Hz
bipolar_rereferencing = True # eg: 1-2 vs. 1 [we always use coi - (coi+1)]
include_stim = False # Leave false by default - cannot be used if stim was delivered. Only works if inc_event_data_ 2 is set to True
inc_event_data_2 = False # Turning off when not needed could decrease runtime significantly

def check_timestamps():
    ## LFP Timestamps to DF ##
    lfp_timestamps = data_dict['cont_data_LFP']['Timestamps']
    lfp_timestamps = np.array(lfp_timestamps)
    for i in lfp_timestamps:
        if lfp_timestamps[i+1] - lfp_timestamps[i] != 1:
            print("Skip error at position - {}".format(i))
    

def check_diff():
    lfp_timestamps = data_dict['cont_data_LFP']['Timestamps']
    lfp_timestamps = np.array(lfp_timestamps)
    lfp_timestamps = pd.DataFrame(lfp_timestamps)
    diff = lfp_timestamps.diff()
    diff = diff.where(diff > 1)
    diff = diff.dropna()
    print(diff)

#check_timestamps()
check_diff()
