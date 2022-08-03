import mne
import scipy.io as scio
import numpy as np
import matlab.engine 
from tkinter import Tk   
from tkinter.filedialog import askopenfilename
import pandas as pd

print("starting...")
 # ecog channel
 # set reference 
 # create single epoch for coherence calculation
# Load log file to grab locked channel
print("choose log file:")
Tk().withdraw()
file = askopenfilename()
log_mat = scio.loadmat(file)
print("File chosen: ", file)
mat_channel = log_mat["watchChannel"]
chosen_chan = int(mat_channel[0][0])

data = []

print("grabbing raw lfp data for channels....")
eng = matlab.engine.start_matlab()
chan = matlab.double([1])
volts = matlab.double([1])
chan_phase = eng.single_chan_lfp(chan, volts, nargout = 2)
## chan_phase[0] = lfp data
## chan_phase [1] = seconds
chans = np.asarray(chan_phase[0])
chans = chans[0].tolist()

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