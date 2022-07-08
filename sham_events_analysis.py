import matlab.engine
import math
from scipy.stats import circmean
from scipy.signal import hilbert, filtfilt, butter
from scipy.stats import circmean
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import numpy as np
from numpy import angle
import pandas as pd
import scipy.io as scio
import seaborn as sns
import matplotlib.pyplot as plt

''' Working on pulling sham event data and calculating ground truth from 1 sec window of event'''

print("Starting TORTE calculation...")
# Load log file to grab locked channel
print("choose log file:")
Tk().withdraw()
file = askopenfilename()
log_mat = scio.loadmat(file)
print("File chosen: ", file)
mat_channel = log_mat["watchChannel"]
chosen_chan = int(mat_channel[0][0])
if chosen_chan == 8:
    reref_chan = 1
else:
    reref_chan = chosen_chan + 1

# Pull lfp data for selected channel
print("grabbing raw lfp data for channel....")
eng = matlab.engine.start_matlab()
chan = matlab.double([chosen_chan])
chan_phase = eng.single_chan_lfp(chan, nargout=2)

ref_chan = matlab.double([reref_chan])
ref_chan_phase = eng.single_chan_lfp(ref_chan, nargout=2)

### chan_phase[0] = lfp data
### chan_phase [1] = seconds
chans = np.asarray(chan_phase[0])
lfp_data = chans[0].tolist()

ref_chans = np.asarray(ref_chan_phase[0])
ref_lfp_data = ref_chans[0].tolist()

# Pull event timeseries
print("getting event time stamps")
event_data = eng.single_chan_event_lfp(nargout=1) ## gotta figure out how to pass path

# Correct data type
event_data = np.asarray(event_data)
event_data = event_data.tolist()

lfp_time = np.asarray(chan_phase[1])
lfp_time_data = lfp_time.tolist()

def binarySearch(arr, l, r, x):
    if r >= l:
        mid = l + (r - l) // 2
        if arr[mid][0] == x:
            return mid
        elif arr[mid][0] > x:
            return binarySearch(arr, l, mid-1, x)
        else:
            return binarySearch(arr, mid + 1, r, x)
    else:
        return -1

print("searching for indexes")        
lfp_index = []
e = 0
for e in range(len(event_data)):
    time = event_data[e][0]
    indx = binarySearch(lfp_time_data, 0, len(lfp_time_data)-1, time)
    lfp_index.append(indx)

print("create continuous event time array")
def cont_timeseries(data):
    event_phase_data = []
    m = 0
    for i in lfp_index:
        low = i - 1500
        if low < 0:
            low = 0
        high = i + 1500
        if high >= len(data):
            high = len(data) - 1
        interval = data[low:high]
        event_phase_data.extend(interval)
    return event_phase_data

chan_event_data = cont_timeseries(lfp_data)
ref_chan_event_data = cont_timeseries(ref_lfp_data)

chan_event_data = np.array(chan_event_data)
ref_chan_event_data = np.array(ref_chan_event_data)

# Bipolar rereferencing 
data = (chan_event_data - ref_chan_event_data)

### Set some params ###
fs = 30000 # sampling rate (default: 30000)
lowpass = 4.0 # Hz
low = lowpass / (fs/2)
highpass = 12.0 # Hz
high = highpass / (fs/2)
order = 2

### Filter / Get Phase ###
[b, a] = butter(order, [low, high], btype = 'band') # Butterworth digital and analog filter
filtered_data = filtfilt(b, a, data)
analytic_data = hilbert(filtered_data)
phase_data = angle(analytic_data)

# Calculate mean angle
rad_avg = circmean(phase_data)
avg = math.degrees(rad_avg)
  
#phase_data = phase_data*180/3.14159 ## Converting to degrees

# Downsample data
c = 0
ds_gt_data = []
for c in range(0, len(phase_data), 2000):
    ds_gt_data.append(phase_data[c])

# Calc circular distance b/w ground truth and 180 (TORTE)
gtp = matlab.double([phase_data])
torte = matlab.double([180])
mat_dist = eng.circ_dist(gtp, torte, nargout = 1) ## need to convert to degrees 
eng.quit()
