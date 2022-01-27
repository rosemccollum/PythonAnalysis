# Plot pre pwr vs delta pwr in scatter plot color coordinated by channel with the channel locked channel a bigger dot
from re import L
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
from tkinter import filedialog
from pathlib import Path
import pow_scatter_helper as psh
import re

print('starting...')
# Setting up figure
big_fig = plt.figure()
sns.set_style("whitegrid")
big_fig.suptitle('Delta Power vs Pre Power in Theta Freq. Band (4-8 Hz)')

# Determine formatting based on num days 
ax_var_ls = []
for k in range(psh.num_days):
    ax_var_ls.append('ax' + str(k+1))

if psh.num_days <= 4:
    row = 2
    col = 2
if psh.num_days > 4 and psh.num_days <= 6: 
    row = 2
    col = 3
if psh.num_days > 6:
    row = 3
    col = 3
for q in range(psh.num_days):
    ax_var_ls[q] = big_fig.add_subplot(row, col, q+1)

d = 0
for p in range(len(psh.arr)):
    # Tests if too many days to analyze
    if len(psh.arr) > 9:
        print('Too many days')
        break

    # Pull day out of file name
    pieces = psh.arr[p][0].split('_')
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
    prepow_name = psh.folder + '/' + day + '/' + psh.arr[p][1]
    #print("File: ", prepow_name)
    prepow_mat = scio.loadmat(prepow_name)
    postpow_name = psh.folder + '/' + day + '/' + psh.arr[p][0]
    #print("File: ", postpow_name)
    postpow_mat = scio.loadmat(postpow_name)

    # Pull needed data 
    pre_pow = prepow_mat['powspctrm'] # Goes into power data
    post_pow = postpow_mat['powspctrm']
    freq = prepow_mat['freq'][0]  # Gives list of freq values
    channels_mat = prepow_mat['chan_labels'] # Gives chan labels

    # Writes list of channels to use for plotting
    h = 0 
    channels = []
    for g in range(len(channels_mat)):
        channels.append(channels_mat[g][0][0])

    # Writes CSV value w/ pre pwr, no channel lables  
    filename = 'prepowerdata.csv'
    i = 0
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(freq)
        for i in range(len(pre_pow)):
            csvwriter.writerow(pre_pow[i])

    # Adding chan labels to pre
    temp_df = pd.read_csv(filename)
    temp_df.insert(0, column='freq', value = channels)
    temp_df.to_csv(filename, index = False)

    # Writes CSV w/ post pwr, no channel lables 
    filename = 'postpowerdata.csv'
    j = 0
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(freq) 
        for j in range(len(post_pow)):
            csvwriter.writerow(post_pow[j])

    # Adding chan label to post
    temp_df = pd.read_csv(filename)
    temp_df.insert(0, column='freq', value = channels)
    temp_df.to_csv(filename, index = False)

    # Load new csvs into Pandas DataFrame
    pre_df = pd.read_csv('prepowerdata.csv',index_col=False)
    post_df = pd.read_csv('postpowerdata.csv',index_col=False)

    # Drop unnecessary columns from pre and post (just want 4-8) 7-15index
    i = 7
    j = 16
    h = 0
    wanted_freq = pd.DataFrame()
    while i < j:
        wanted_freq.insert(h, freq[i], pre_df[str(freq[i])])
        i +=1 
        h +=1

    chan_labels = pre_df['freq']
    pre_df = wanted_freq
    pre_df.insert(0, 'freq', chan_labels)

    i = 7
    j = 16
    h = 0
    wanted_freq = pd.DataFrame()
    while i < j:
        wanted_freq.insert(h, freq[i], post_df[str(freq[i])])
        i +=1 
        h +=1

    chan_labels = post_df['freq']
    post_df = wanted_freq
    post_df.insert(0, 'freq', chan_labels)

    # Remove strings so math can be done on whole data frame 
    pre_chan_labels = pre_df['freq']
    del pre_df['freq']

    post_chan = post_df['freq']
    del post_df['freq']

    # Take log of pre and post dataframes 
    pre_df = 10 * np.log10(pre_df)
    post_df = 10 * np.log10(post_df)

    # Taking average of channels and putting into df
    avg_pre = pre_df.mean(axis = 1)
    avg_post = post_df.mean(axis = 1)

    # Taking standard deviation of channels
    std_pre = pre_df.std(axis = 1)
    std_post = post_df.std(axis = 1)

    # Adding standard deviation to average 
    pre_added = avg_pre.add(std_pre)
    post_added = avg_post.add(std_post)

    # Turning series into dataframes 
    pre_df = pre_added.to_frame()
    post_df = post_added.to_frame()

    # Put chan labels back
    pre_df.insert(0, 'chan', pre_chan_labels)
    post_df.insert(0, 'chan', post_chan)

    # Subtract post - pre coh
    delta_df = post_df.set_index('chan').subtract(pre_df.set_index('chan'), fill_value=0)

    # Transpose DataFrame
    pre_df = pre_df.T
    delta_df = delta_df.T

    # Remove index and save to new DataFrame
    pre_df.columns = pre_df.iloc[0]
    pre_df_fin = pre_df[1:]

    # Turn into long form data
    delta_melted = pd.melt(delta_df, value_vars=channels, var_name = 'chan', value_name= 'delta')
    final_df = pd.melt(pre_df_fin, value_vars=channels, var_name = 'chan', value_name= 'pre')

    # Pulling out day and rat for title
    temp = prepow_name.split('/')
    for l in range(len(temp)):
        if 'dev' in temp[l] and 'RAW' not in temp[l]:
            rat = temp[l]
        if 'day' in temp[l] and 'RAW' not in temp[l]:
            day = temp[l]

    # Adding delta column to pre data 
    delta = delta_melted['delta']
    final_df['delta'] = delta

    # Plotting data
    fig = plt.gcf()
    fig.set_size_inches(10,6)
    ax_num = ax_var_ls[p]
    plot = sns.scatterplot(data = final_df, ax = ax_num, x = 'pre', y = 'delta', hue = 'chan')
    plot.set(title = day)
    plot.set(ylim = (-4,4))
    plot.set(xlim =(15, 40))
    plot.get_legend().remove()
    plot.set_xlabel('log(pre power) (W)')
    plot.set_ylabel('delta log(power) (W)')
    plot.axhline(0, color = 'dimgray', ls = '--')


handles, labels = plot.get_legend_handles_labels()
big_fig.legend(handles, labels, loc = 'center right')
plt.tight_layout()

plt.savefig(psh.folder +  '/prepow_vs_deltapow.png')
plt.show()

print('done')