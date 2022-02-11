import scipy.io as scio
import seaborn as sns
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from tkinter import Tk   
from tkinter.filedialog import askopenfilename
from graphs_helper import heatmap_help
import re

print('starting...')

# Call file grabber
arr, num_days, folder = heatmap_help()

# Pull day out of file name
pieces = arr[0][0].split('_')
rat = ''
for l in pieces:
    if 'dev' in l:
        rat = l 

# Setting up figure
big_fig = plt.figure()
big_fig.suptitle('Delta Coherence in ' + rat)

# Determine formatting based on num days 
ax_var_ls = []
for k in range(num_days):
    ax_var_ls.append('ax' + str(k+1))

if num_days <= 4:
    row = 2
    col = 2
if num_days > 4 and num_days <= 6: 
    row = 2
    col = 3
if num_days > 6:
    row = 3
    col = 3
for q in range(num_days):
    ax_var_ls[q] = big_fig.add_subplot(row, col, q+1)

for p in range(len(arr)):
    # Tests if too many days to analyze
    if len(arr) > 9:
        print('Too many days')
        break

    # Pull day out of file name
    pieces = arr[p][0].split('_')
    day = ''
    for l in pieces:
        if 'day' in l:
            day = l 
    
    # Make sure its just day and number 
    temp = re.search('\w+\d+', day)
    begin = temp.span()[0]
    end = temp.span()[1]
    day = day[begin:end]

    # Open pre and post files
    precoh_name = folder + '/' + day + '/' + arr[p][1]
    #print("File: ", prepow_name)
    precoh_mat = scio.loadmat(precoh_name)
    postcoh_name = folder + '/' + day + '/' + arr[p][0]
    #print("File: ", postpow_name)
    postcoh_mat = scio.loadmat(postcoh_name)

    # Pull coh, freq, and chan data
    pre_coh = precoh_mat['coh_spect']
    post_coh = postcoh_mat['coh_spect']
    freq = precoh_mat['freq'][0]
    num_chan = len(precoh_mat['cmb_labels'])

    # Writes CSV with values 
    def writeCSV(filename, df):
        i = 0
        with open(filename, 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(freq)
            for i in range(len(df)):
                csvwriter.writerow(df[i])
    
    writeCSV('precohdata.csv', pre_coh)
    writeCSV('postcohdata.csv', post_coh)

    # Load into pandas data frame
    pre_df = pd.read_csv('precohdata.csv',index_col=False)
    post_df = pd.read_csv('postcohdata.csv', index_col= False)

    # Create delta dataframe
    delta_df = post_df.subtract(pre_df)

    # Pulling out day and rat for title
    temp = precoh_name.split('/')
    for l in range(len(temp)):
        if 'dev' in temp[l] and 'RAW' not in temp[l]:
            rat = temp[l]
        if 'day' in temp[l] and 'RAW' not in temp[l]:
            day = temp[l]
    
    # Label x and y axis
    y_label = np.arange(1, num_chan + 1, 1)
    x_ticks = np.arange(0,61,10)
    x_labels = range(0,31,5)

    # Plotting data
    fig = plt.gcf()
    fig.set_size_inches(10,6)
    ax_num = ax_var_ls[p]
    d_plot = sns.heatmap(data = delta_df, ax = ax_num, yticklabels = y_label, cbar_kws={'label': 'Coherence'}, cmap="viridis", vmin = -0.2, vmax = 0.2)
    d_plot.set_xticks(x_ticks)
    d_plot.set_xticklabels(x_labels, rotation = 0)
    d_plot.set(title=day, xlabel="Frequency (HZ)", ylabel="Channel cmb #")
    d_plot.axvline(x=7, color = 'black')
    d_plot.axvline(x=16, color = 'black')

plt.tight_layout()
plt.savefig(folder +  '/deltacoh_heatmaps.png')
plt.show()
print('done')