# Plots 4x4 heat map of average coh by channel combination
import scipy.io as scio
import seaborn as sns
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from tkinter import Tk   
from tkinter.filedialog import askopenfilename

# Choose and open pre file
print('Choose pre data file')
Tk().withdraw() 
precoh_name = askopenfilename()
print("File: ", precoh_name)
precoh_mat = scio.loadmat(precoh_name)

# Choose and open post file
print('Choose post data file')
Tk().withdraw()
postcoh_name = askopenfilename()
print("File: ", postcoh_name)
postcoh_mat = scio.loadmat(postcoh_name)

# Pull coh, freq, and chan data
pre_coh = precoh_mat['coh_spect']
post_coh = postcoh_mat['coh_spect']
freq = precoh_mat['freq'][0]
num_chan = len(precoh_mat['cmb_labels'])

# Write pre data into CSV
filename = 'precohdata.csv'
i = 0
with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(freq)
    for i in range(len(pre_coh)):
        csvwriter.writerow(pre_coh[i])

# Write post data into CSV
filename = 'postcohdata.csv'
i = 0
with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(freq)
    for i in range(len(post_coh)):
        csvwriter.writerow(post_coh[i])

# Load into pandas data frame
pre_df = pd.read_csv('precohdata.csv',index_col=False)
post_df = pd.read_csv('postcohdata.csv', index_col= False)

# Use iloc (integer position-based location) to focus on channels in freq range 4-12Hz
pre_df = pre_df.iloc[:,7:24]
post_df = post_df.iloc[:,7:24]

# Use .mean() to get the average coherence for each frequency
pre_df = pre_df.mean(axis=1)
post_df = post_df.mean(axis=1)

# Create 4x4 dfs with data
pre = {'BLA1-BLA2':[pre_df.loc[0],pre_df.loc[1],pre_df.loc[2],pre_df.loc[3]],'BLA3-BLA4':[pre_df.loc[4],pre_df.loc[5],pre_df.loc[6],pre_df.loc[7]],'BLA5-BLA6':[pre_df.loc[8],pre_df.loc[9],pre_df.loc[10],pre_df.loc[11]],'BLA7-BLA8':[pre_df.loc[12],pre_df.loc[13],pre_df.loc[14],pre_df.loc[15]]}
post = {'BLA1-BLA2':[post_df.loc[0],post_df.loc[1],post_df.loc[2],post_df.loc[3]],'BLA3-BLA4':[post_df.loc[4],post_df.loc[5],post_df.loc[6],post_df.loc[7]],'BLA5-BLA6':[post_df.loc[8],post_df.loc[9],post_df.loc[10],post_df.loc[11]],'BLA7-BLA8':[post_df.loc[12],post_df.loc[13],post_df.loc[14],post_df.loc[15]]}

# Build dfs and add index
pre_df = pd.DataFrame(data=pre,index=['IL1-IL2','IL3-IL4','IL5-IL6','IL7-IL8'])
post_df = pd.DataFrame(data=post, index=['IL1-IL2','IL3-IL4','IL5-IL6','IL7-IL8'])

# Cut pre and post down to the frequency we are looking at

# Create delta dataframe
delta_df = post_df.subtract(pre_df)

# Plot all three graphs 
fig = plt.figure(figsize = (9,8), constrained_layout = True)
ax1 = fig.add_subplot(2, 2, 1)
ax2 = fig.add_subplot(2, 2, 2)
ax3 = fig.add_subplot(2, 2, 3)

pre_plot = sns.heatmap(data = pre_df, cmap = "viridis", ax = ax1, vmin = -.2, vmax = 0.8)
pre_plot.set(title="Pre Coherence Spectra", xlabel="BLA Channel", ylabel="IL Channel")
pre_plot.set_xticklabels(pre_plot.get_xticklabels(),rotation=45)

post_plot = sns.heatmap(data = post_df, cmap = "viridis", ax = ax2, vmin = -.2, vmax = 0.8)
post_plot.set(title="Post Coherence Spectra", xlabel="BLA Channel", ylabel="IL Channel")
post_plot.set_xticklabels(post_plot.get_xticklabels(),rotation=45)

d_plot = sns.heatmap(data=delta_df, cmap = "viridis", ax = ax3, vmin = -.2, vmax = 0.2)
d_plot.set(title="Change in Coherence Spectra", xlabel="BLA Channel", ylabel="IL Channel")
d_plot.set_xticklabels(d_plot.get_xticklabels(),rotation=45)

# Show the plot
plt.show()
print('done')
