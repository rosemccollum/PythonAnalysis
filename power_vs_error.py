''' Graph error of TORTE and ASIC models ''' 
import imp
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import math
import scipy.io as scio
import matlab.engine
from scipy.signal import hilbert, filtfilt, butter
from scipy.stats import circmean
from numpy import angle, array
import mne

print("starting...")
# Load matlab files
Tk().withdraw() 
file = askopenfilename()
log_mat = scio.loadmat(file)
print("File: ", file)
mat_channel = log_mat["watchChannel"]
chosen_chan = int(mat_channel[0][0])

# Pull lfp data for selected channel
print("grabbing raw lfp data for channel....")
eng = matlab.engine.start_matlab()
chan = matlab.double([chosen_chan])
chan_phase = eng.single_chan_lfp(chan, nargout = 2)

chans = np.asarray(chan_phase[0])
chans = chans[0].tolist()

### Calculating Ground Truth ### 
### Calculating Ground Truth ### 
print("calculating ground truth")

# Set some params #
fs = 30000 # sampling rate (default: 30000)
lowpass = 4.0 # Hz
low = lowpass / (fs/2)
highpass = 12.0 # Hz
high = highpass / (fs/2)
order = 2
data = chans
# Filter / Get Phase ###
[b, a] = butter(order, [low, high], btype = 'band') # Butterworth digital and analog filter
filtered_data = filtfilt(b, a, data)
analytic_data = hilbert(filtered_data)
phase_data = angle(analytic_data)

# Calculate mean angle
rad_avg = circmean(phase_data)
avg = math.degrees(rad_avg)
  
phase_data = phase_data*180/3.14159 ## Converting to degrees
    
# Shorten phase to every second
phases = []
p = 0 
for p in range(0, len(phase_data), 60):
    phases.append(phase_data[p])
print(len(phases))
### Calculating TORTE ###

# Call torte function
print("calculating TORTE in matlab...")
mat_chan = matlab.double([chans])
buff = matlab.double([[200]]) 
torte = eng.hilbert_transformer_phase(mat_chan, buff,  nargout = 3) 

# Calculate mean angle
rad_avg = circmean(torte[0])
avg = math.degrees(rad_avg)
    
# Convert to correct data type and convert to degrees
temp_phases = array(torte[0])
d = 0
torte_phases = []
for d in range(0, len(temp_phases)):
    temp = float(temp_phases[d])
    torte_phases.append(temp)

torte_phases = np.degrees(torte_phases) ## change to degrees    

# Call phase calculation functions and convert to list
print("calculating error")
#df_gtp = groundTruth(file)
gtp = phases
torte = torte_phases
print(len(gtp))
print(len(torte))
# Calc circular distance b/w points
eng = matlab.engine.start_matlab()
mat_gtp = matlab.double([gtp])
mat_torte = matlab.double([torte])
mat_dist = eng.circ_dist(mat_gtp, mat_torte, nargout = 1) 
eng.quit()

# Convert to degrees
rad_dist = np.asarray(mat_dist)
rad_dist = rad_dist[0]
dist = []
d = 0
for d in range(0, len(rad_dist)):
    temp_degrees = math.degrees(rad_dist[d])
    dist.append(temp_degrees)

print("starting power calculations")
c = 0
chan_list = []
for c in range(0, len(chans), 30): ## downsample to 1k hz 
    chan_list.append(chans[c])

print("===========structuring data============")
chan_info = mne.create_info(1,1000, ch_types='ecog')
rawData = np.array([[chan_list]]) ## (1,1,18033) (epochs, chans, times)
epochs = mne.EpochsArray(data=rawData, info=chan_info)

print("==========CALCULATING POWER========")
frequencies = np.logspace(np.log10(1), np.log10(30), 32) 
num_cycles = np.logspace(np.log10(3), np.log10(7), 32)
power = mne.time_frequency.tfr_array_multitaper(epochs, 1000, frequencies,time_bandwidth = 3.0, output = 'power', n_cycles=num_cycles)
## output is (n_epochs, n_chans, n_freqs, n_times)
## epoch_data = shape(epochs, chan, time), sfreq = 30,000 (1k ds), freqs = [1-30], 
#   n_cycles=7.0, zero_mean=True, time_bandwidth=3, use_fft=True, decim=1, output='power', n_jobs=1, verbose=None)[source]
power = power[0][0]
f = 1
freqs = []
for f in range(32):
    freqs.append(f)
power_df = pd.DataFrame(power)
power_means = power_df.mean(axis=0)

means = power_df.values.tolist()
