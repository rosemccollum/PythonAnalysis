from fileinput import filename
from cv2 import phase
import matlab.engine 
import h5py
import hdf5storage
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import numpy as np
import pandas as pd
import scipy.io as scio
import seaborn as sns
import matplotlib.pyplot as plt


print("starting...")
# Load matlab files
Tk().withdraw() 
file = askopenfilename()
print("File: ", file)
### file = r"C:/Users/angel/Documents/TNELab/Programming/RatData/dev2111/day1/RAW_PRE_dev2111_day1_cleandata_struct.mat" for debugging
mat = scio.loadmat(file)

# Grab necessary data
mat_phase = mat["cur_data"]["phase_data"]
mat_time = mat["cur_data"]["seconds"]

# Make array into list 
phase_list = []
for i in range(len(mat_phase[0][0][0])) :
    phase_list.append(mat_phase[0][0][0][i])

# Convert to array to correct type, then back to list 
phases = np.array(phase_list)
phases = phases.astype('int32')
phase_list = phases.tolist()

# Call function
print("calling matlab script...")
eng = matlab.engine.start_matlab()
buff = matlab.double([[200]]) ## Why am i using 200
mat_phase = matlab.double([phase_list])
torte = eng.hilbert_transformer_phase(mat_phase, buff, nargout = 3)
eng.quit()

## Torte output len is phase_list len / 59.99

# Shorten torte measurements to every 10
p = 0
phases = []
for p in range(0, len(torte[0]), 10):
    phases.append(torte[0][p])

# Put data in dataframe
df = pd.DataFrame(phases)
df.rename(columns= {0:'phase'}, inplace=True)

# Write and add time values 
t = 0
time = []
for t in range (0, len(mat_time[0][0]), 600): 
    time.append(mat_time[0][0][t][0])
df["time"] = time

# Split file name to get rat and day data
temp = file.split("/")
fileName = temp[-1]
fileName = fileName.split("_")
for word in fileName:
    if "dev" in word:
        rat = word
    elif "day" in word:
        day = word
    elif ('POST' in word) or ("PRE" in word):
        condition = word
dir = file.split("RAW")

# Graph and save plot 
print("graphing...")
fig = plt.figure(figsize = (13,7))
plot = sns.lineplot(data = df, x = 'time', y = 'phase')
plot.set_title('TORTE Phase over time ' + condition + " " + rat + " " + day)
plot.set_xlabel('Time (s)')
plot.set_ylabel('Phase')
plt.savefig(dir[0] + rat + '_' + day + "_" + condition + "_TORTEphase_over_time")
plt.show()
print("done")