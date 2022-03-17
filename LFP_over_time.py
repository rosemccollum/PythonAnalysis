'''Graphs the LFP signal over time during closed loop stimulation. Created 25 Feb. rae McCollum'''
from fileinput import filename
import scipy.io as scio
import seaborn as sns
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk   
from tkinter.filedialog import askopenfilename

print("starting...")
# Load matlab files
Tk().withdraw() 
file = askopenfilename()
print("File: ", file)
mat = scio.loadmat(file)

# Grab necessary info
mat_time = mat['cur_data']['seconds']
mat_channels = mat['cur_data']['labels']
lfp = mat['cur_data']['ds_data']

# Split file name to get rat and day data
temp = file.split("/")
fileName = temp[-1]
fileName = fileName.split("_")
for word in fileName:
    if "dev" in word:
        rat = word
    elif "day" in word:
        day = word

dir = file.split("CLOSED")

## len(lfp[0][0]) = 16 
## lfp[0][0][0] = lfp over time
## len(lfp[0][0][x]) = time (sec) at channel x (1,803,288 time points)

## mat_channels[0][0][0][0][0] = channel name, 3rd is index to change
## len(mat_channels[0][0]) = 16

## mat_time[0][0][x][0] = gets single time value
## len(mat_time[0][0]) = seconds 

# Make smaller dataset to work with first
shorter_lfp = []
i = 1
while i <= 16:
    lfp_short = []
    for j in range(0, len(lfp[0][0][0]), 1000):
        lfp_short.append(lfp[0][0][0][j])
    shorter_lfp.append(lfp_short)
    i += 1

# Make list of time values (every second)
t = 0
time = []
for t in range (0, len(mat_time[0][0]), 1000): 
    time.append(mat_time[0][0][t][0])

# Writes list of channels to use for plotting
g = 0 
channels = []
for g in range(len(mat_channels[0][0])):
    channels.append(mat_channels[0][0][g][0][0])

# # Writes list of ALL time values
# t = 0
# time = []
# for t in range(len(mat_time[0][0])):
#     time.append(mat_time[0][0][t][0])

# Writes CSV of values  
sheet = 'stimdata.csv' 
i = 0
with open(sheet, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(time)
    for i in range(len(shorter_lfp)):
        csvwriter.writerow(shorter_lfp[i])

print("CSV Written")
# Adding chan labels 
temp_df = pd.read_csv(sheet)
temp_df.insert(0, column='time', value = channels)
temp_df.to_csv(sheet, index = False)

# Load new csvs into Pandas DataFrame
lfp_df = pd.read_csv('stimdata.csv',index_col=False)

# Transpose df 
lfp_df = lfp_df.T

# Get rid ofindex
lfp_df.columns = lfp_df.iloc[0]
df = lfp_df[1:]

# Pull frequency data from the index and create new 'freq' column
df['time'] = df.index 

# Remove the frequency data from the index
df.reset_index(drop = True, inplace = True)

# Reorganize into correct channel labels
i = 0
while i < (len(channels)):
    df.rename(columns = {df.columns[i]: channels[i]}, inplace = True)
    i += 1

time_col = df.pop('time')
df.insert(0, 'time', time_col)

ch_num = 2 # Number of channels This defines number of while loops
loop_num = ch_num +1 # This is to make sure we can put in the channel number literally and still get the loop to run the correct number of times
m = 1
l = 0

# Build df_pre before while loop
column_list = ['time','lfp', 'channel']
global df_final
df_final = pd.DataFrame(columns=column_list)  

# while loop to create final DataFrame (df_final_pre)
while m < loop_num:
    channel = channels[l]  
    df_loop = df[['time',channel]]
    df_loop['channel'] = channel
    df_loop.rename({channel: 'lfp'},axis=1, inplace=True)
    m += 1
    l += 1
    df_final = df_final.append(df_loop)
    del df_loop

# df_final_pre postprocessing
df_final = df_final.reset_index()
df_final = df_final[['time','lfp','channel',]]

print('graphing')

# Graph
fig = plt.figure(figsize = (13,7))
plot = sns.lineplot(data = df_final, x='time',y='lfp',hue='channel')
plot.set_title('LFP over time')
plot.set_xlabel('Time (s)')
plot.set_ylabel('LFP')
plot.set(ylim = (-2000, 2000))
plot.get_legend().remove()
time_labels = (range(0, 1804, 60))
plot.set_xticks(time_labels)
plot.set_xticklabels(time_labels, rotation = 45)
plt.tight_layout()
plt.savefig(dir[0] + rat + '_' + day + "_LFP_over_time")
print("done")
plt.show()