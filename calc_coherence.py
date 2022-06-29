import mne
import mne_connectivity
import scipy.io as scio
import numpy as np
import matlab.engine 
import random
from tkinter import Tk   
from tkinter.filedialog import askopenfilename

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
chan_phase = eng.single_chan_lfp(chan, nargout = 2)

    ## chan_phase[0] = lfp data
    ## chan_phase [1] = seconds
chans = np.asarray(chan_phase[0])
chans = chans[0].tolist()
    
c = 0
chan_list = []
for c in range(0, len(chans), 3000): ## figure out how to actually downsample 
    chan_list.append(chans[c])
data.append(chan_list)

# t = 0
# event_data = []
# for t in range(0, len(data[0])):
#     temp_event = []
#     temp_event.append(t)
#     temp_event.append(0)
#     randLFP = random.randint(0, len(chans))
#     temp_event.append(t + chans[randLFP])  ## make this add a random lfp number to it? 
#     event_data.append(temp_event)
# print("=======figuring out adding lfps=======")
# print(len(chans)) ## 9 mil
# print(chans[0]) ## a float 
print("===========structuring data============")
chan_info = mne.create_info(1,18000, ch_types='ecog')
rawData = mne.io.RawArray(data, chan_info)

# stim_info = mne.create_info(['SHAM'], 30000, ch_types='stim')
# stim_data = np.zeros((1, len(event_data)))
# stim_raw = mne.io.RawArray(stim_data, stim_info)
# rawData.add_channels([stim_raw], force_update_info=True)
# rawData.add_events(event_data, stim_channel='SHAM') ## all epochs match and all are "bad" and dropped ???s
epochs = mne.make_fixed_length_epochs(rawData, id=1, duration = max(rawData.times))

print("==========CALCULATING COHERENCE========")
frequencies = np.logspace(np.log10(5), np.log10(50), 32) 
num_cycles = np.logspace(np.log10(3), np.log10(7), 32)
coh = mne_connectivity.spectral_connectivity_time(epochs, method ='coh', sfreq = 18000.0, mode = 'multitaper', freqs = frequencies, n_cycles = num_cycles) ## add frequency and cycles 
#coh[0] (i.e., the first list in coh)= the connectivity measure
#which is an 3D array with shape 2 (left and right coherence) by 32 (frequencies) by 201 (timestamps)
#coh[1] = an array of the frequencies used (n = 32)
#coh[2] = an array of the samples (time points; n = 201; means that they are computing csd at each sample across all the epochs
#coh[3] = number of epochs used
#coh[4] = number of tapers used (only for multitaper)
print(coh)
