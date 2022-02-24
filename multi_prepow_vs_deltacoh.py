# Plot delta coh (y) vs pre pow (x) to determine if relationship exists
import scipy.io as scio
import seaborn as sns
import pandas as pd
import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import math
import os
from tkinter import Tk   
from tkinter.filedialog import askopenfilename
from graphs_helper import pow_vs_coh_help
import re

# Call file grabber
arr, num_days, folder = pow_vs_coh_help()

# Pull day out of file name
pieces = arr[0][0].split('_')
rat = ''
for l in pieces:
    if 'dev' in l:
        rat = l 

# Setting up figure
big_fig = plt.figure()
sns.set_style("whitegrid")
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
    prepow_name = folder + '/' + day + '/' + arr[p][2]
    #print("File:", prepow_name)
    prepow_mat = scio.loadmat(prepow_name)

    # Gathers coh, pow, feq, and chan data
    pre_coh = precoh_mat['coh_spect'] 
    post_coh = postcoh_mat['coh_spect']
    freq = precoh_mat['freq'][0]  # Gives list of freq values
    channels_mat = precoh_mat['cmb_labels']
    pow_chan_mat = prepow_mat['chan_labels']
    pre_pow = prepow_mat['powspctrm']

    # Writes list of channels to use for plotting
    g = 0 
    channels = []
    for g in range(len(channels_mat)):
        channels.append(channels_mat[g][0][0])

    g = 0 
    pow_channels = []
    for g in range(len(pow_chan_mat)):
        pow_channels.append(pow_chan_mat[g][0][0])

    def writeCSV(filename, data):
        # Writes CSV of values   
        i = 0
        with open(filename, 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(freq)
            for i in range(len(data)):
                csvwriter.writerow(data[i])
        # Adding chan labels 
        chan = channels 
        if 'pow' in filename:
            chan = pow_channels 
        temp_df = pd.read_csv(filename)
        temp_df.insert(0, column='freq', value = chan)
        temp_df.to_csv(filename, index = False)
        
    writeCSV('precohdata.csv', pre_coh)
    writeCSV('postcohdata.csv', post_coh)
    writeCSV('prepowerdata.csv', pre_pow)

    # Load into pandas data frame
    precoh_df = pd.read_csv('precohdata.csv',index_col=False)
    postcoh_df = pd.read_csv('postcohdata.csv', index_col= False)
    prepow_df = pd.read_csv('prepowerdata.csv', index_col = False)

    # Drop unnecessary columns from dfs (just want 4-12) 
    def get_theta_band(df):
        i = 7
        j = 24
        h = 0
        wanted_freq = pd.DataFrame()
        while i < j:
            wanted_freq.insert(h, freq[i], df[str(freq[i])])
            i +=1 
            h +=1

        chan_labels = df['freq']
        df = wanted_freq
        df.insert(0, 'freq', chan_labels)
        return df
    get_theta_band(precoh_df)
    get_theta_band(postcoh_df)
    get_theta_band(prepow_df)

    # Take of chan labels to do math
    pre_coh_labels = precoh_df['freq']
    del precoh_df['freq']

    post_coh_labels = postcoh_df['freq']
    del postcoh_df['freq']

    pre_pow_labels = prepow_df['freq']
    del prepow_df['freq']

    # Take log of pre and post dataframes 
    prepow_df = 10 * np.log10(prepow_df)

    # Averaging across theta band
    avg_pre_coh = precoh_df.mean(axis = 1)
    avg_post_coh = postcoh_df.mean(axis = 1)
    avg_pre_pow = prepow_df.mean(axis = 1)

    # Taking standard deviation of channels
    std_pre = prepow_df.std(axis = 1)

    # Adding standard deviation to average 
    pre_added = avg_pre_pow.add(std_pre)

    # Turning avg series back into dataframe
    precoh_df = avg_pre_coh.to_frame()
    postcoh_df = avg_post_coh.to_frame()
    prepow_df = pre_added.to_frame()

    # Put chan labels back
    precoh_df.insert(0, 'chan', pre_coh_labels)
    postcoh_df.insert(0, 'chan', post_coh_labels)
    prepow_df.insert(0, 'chan', pre_pow_labels)

    # Create delta dataframe
    delta_df = postcoh_df.set_index('chan').subtract(precoh_df.set_index('chan'), fill_value=0)

    # Create final dataframe
    final_df = pd.DataFrame()
    final_df = final_df.reindex(columns = ['IL', 'BLA', 'coh'] )

    # Split IL and BLA into columns 
    for i in range(len(delta_df.index)):
        comb = delta_df.index[i]
        split = comb.split()
        final_df.loc[-1] = [split[0], split[2], delta_df[0][i]]
        final_df.index = final_df.index + 1
    final_df = final_df.sort_index()
    
    # Add IL pow value in final column
    final_df['pow'] = ''
    for k in range(len(final_df['IL'])):
        for j in range(len(prepow_df)):
            if final_df['IL'][k] == prepow_df['chan'][j]:
                index = final_df[final_df['IL']==final_df['IL'][k]].index.values
                final_df['pow'][index] = prepow_df[0][j]

    # Pull IL pow values for tick and labels 
    pow_labels = []
    pow_values = []
    for h in range(len(prepow_df)):
        if 'IL' in prepow_df['chan'][h]:
            pow_labels.append(prepow_df['chan'][h])
            pow_values.append(prepow_df[0][h])
    for m in range(len(pow_labels)):
        pow_labels[m] = pow_labels[m] + ' (' + str(round(pow_values[m], 1)) + ')'

    # Pull rat and day for saving and title
    temp = precoh_name.split('/')
    for l in range(len(temp)):
        if 'dev' in temp[l] and 'RAW' not in temp[l]:
            rat = temp[l]
        if 'day' in temp[l] and 'RAW' not in temp[l]:
            day = temp[l]

    # Graph it
    fig = plt.gcf()
    fig.set_size_inches(10,6)
    ax_num = ax_var_ls[p]
    plot = sns.scatterplot(data = final_df, ax = ax_num, x = 'pow', y = 'coh', hue = 'BLA')
    plot.set_title(day)
    plot.set_xlabel('Pre Power ((μV)²/Hz)')
    plot.set_ylabel('Delta Coherence in \n Theta Band (4-12 Hz)')
    plot.set_xticks(pow_values)
    plot.set_xticklabels(pow_labels, rotation = 45 )
    plot.set(ylim = (-0.2,0.2))
    plot.set(xlim = (0, 40))
    plot.get_legend().remove()
    plot.axhline(0, color = 'dimgray', ls = '--')
    plt.tight_layout()
    plt.grid()

handles, labels = plot.get_legend_handles_labels()
big_fig.legend(handles, labels, loc = 'center')    
plt.savefig(folder + '/all_prepow_vs_deltacoh.png')
plt.show()
print('done')