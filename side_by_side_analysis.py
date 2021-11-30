# Plots three graphs: pre, post, and delta coh vs channel in line plot, color coordinated by channel. 
import scipy.io as scio
import seaborn as sns
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import simple_GUI as sg
from tkinter import Tk   
from tkinter.filedialog import askopenfilename

print('TNEL Plotter')

# Load matlab files
print('Choose pre data file')
Tk().withdraw() 
pre_name = askopenfilename()
print("File: ", pre_name)
pre_mat = scio.loadmat(pre_name)

print('Choose post data file')
Tk().withdraw() 
post_name = askopenfilename()
print("File: ", post_name)
post_mat = scio.loadmat(post_name)

# Gathers coh, feq, and chan data
pre_coh = pre_mat['coh_spect'] # Goes into coh data
post_coh = post_mat['coh_spect']
freq = pre_mat['freq'][0]  # Gives list of freq values
channels_mat = pre_mat['cmb_labels']

# Writes list of channels to use for plotting
h = 0 
channels = []
for g in range(len(channels_mat)):
    channels.append(channels_mat[g][0][0])

# Writes CSV value w/ pre coh, no channel lables  
filename = 'precohdata.csv'
i = 0
with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(freq)
    for i in range(len(pre_coh)):
        csvwriter.writerow(pre_coh[i])

# Adding chan labels 
temp_df = pd.read_csv(filename)
temp_df.insert(0, column='freq', value = channels)
temp_df.to_csv(filename, index = False)

# Writes CSV w/ post coh, no channel lables 
filename = 'postcohdata.csv'
j = 0
with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(freq) 
    for j in range(len(post_coh)):
        csvwriter.writerow(post_coh[j])

# Adding chan label
temp_df = pd.read_csv(filename)
temp_df.insert(0, column='freq', value = channels)
temp_df.to_csv(filename, index = False)

# Load new csvs into Pandas DataFrame
df = pd.read_csv('precohdata.csv',index_col=False)
df_2 = pd.read_csv('postcohdata.csv',index_col=False)

# Subtract post - pre coh
sub_df = df_2.set_index('freq').subtract(df.set_index('freq'), fill_value=0)

# Transpose DataFrame
df = df.T
df_2 = df_2.T
sub_df = sub_df.T

# Remove index and save to new DataFrame
df.columns = df.iloc[0]
df_new = df[1:]

df_2.columns = df.iloc[0]
df_2_new = df_2[1:]

# Add deliniator to end of Data Frame
df_new['period'] = 'pre'
df_2_new['period'] = 'post' 
sub_df['period'] = 'delta'
 
# CORRECTING df_new 
# Pull frequency data from the index and create new 'freq' column
df_new['freq'] = df_new.index 

# Remove the frequency data from the index
df_new.reset_index(drop = True, inplace = True)
# Remove index name from df_3
# Drop first column of dataframe
df_new = df_new[['freq', channels[0], channels[1], channels[2], channels[3], channels[4], channels[5], channels[6], channels[7],'period']]

ch_num = 8 # Number of channels - 8 by default. This defines number of while loops
loop_num = ch_num +1 # This is to make sure we can put in the channel number literally and still get the loop to run the correct number of times
m = 1
l = 0

# Build df_pre before while loop
column_list = ['freq','coh','period','channel']
global df_final_pre
df_final_pre = pd.DataFrame(columns=column_list)  

# while loop to create final DataFrame (df_final_pre)
while m < loop_num:
    channel = channels[l]  
    df_loop = df_new[['freq',channel,'period']]
    df_loop['channel'] = channel
    df_loop.rename({channel: 'coh'},axis=1, inplace=True)
    m += 1
    l += 1
    df_final_pre = df_final_pre.append(df_loop)
    del df_loop

# df_final_pre postprocessing
df_final_pre = df_final_pre.reset_index()
df_final_pre = df_final_pre[['freq','coh','channel','period']]


# CORRECTING df_2_new 
# Pull frequency data from the index and create new 'freq' column
df_2_new['freq'] = df_2_new.index 

# Remove the frequency data from the index
df_2_new.reset_index(drop = True, inplace = True)
# Remove index name from df_3
# Drop first column of dataframe
df_2_new = df_2_new[['freq', channels[0], channels[1], channels[2], channels[3], channels[4], channels[5], channels[6], channels[7],'period']]

ch_num = 8 # Number of channels - 8 by default. This defines number of while loops
loop_num = ch_num +1 # This is to make sure we can put in the channel number literally and still get the loop to run the correct number of times
m = 1
l = 0

# Build df_pre before while loop
column_list = ['freq','coh','period','channel']
global df_final_post
df_final_post = pd.DataFrame(columns=column_list)  

# while loop to create final DataFrame (df_final_post)
while m < loop_num:
    channel = channels[l]  
    df_loop = df_2_new[['freq',channel,'period']]
    df_loop['channel'] = channel
    df_loop.rename({channel: 'coh'},axis=1, inplace=True)
    m += 1
    l += 1
    df_final_post = df_final_post.append(df_loop)
    del df_loop

# df_final_post postprocessing
df_final_post = df_final_post.reset_index()
df_final_post = df_final_post[['freq','coh','channel','period']]

# CORRECTING sub_df
# Pull frequency data from the index and create new 'freq' column
sub_df['freq'] = sub_df.index 

# Remove the frequency data from the index
sub_df.reset_index(drop = True, inplace = True)
# Remove index name from df_3
# Drop first column of dataframe
sub_df = sub_df[['freq', channels[0], channels[1], channels[2], channels[3], channels[4], channels[5], channels[6], channels[7],'period']]

ch_num = 8 # Number of channels - 8 by default. This defines number of while loops
loop_num = ch_num +1 # This is to make sure we can put in the channel number literally and still get the loop to run the correct number of times
m = 1
l = 0

# Build df_pre before while loop
column_list = ['freq','coh','period','channel']
global df_final_sub
df_final_sub = pd.DataFrame(columns=column_list)  

# while loop to create final DataFrame (df_final_sub)
while m < loop_num:
    channel = channels[l]  
    df_loop = sub_df[['freq',channel,'period']]
    df_loop['channel'] = channel
    df_loop.rename({channel: 'coh'},axis=1, inplace=True)
    m += 1
    l += 1
    df_final_sub = df_final_sub.append(df_loop)
    del df_loop

# df_final_sub postprocessing
df_final_sub = df_final_sub.reset_index()
df_final_sub = df_final_sub[['freq','coh','channel','period']]

# Plot graphs in subplot
fig = plt.figure(figsize = (9,8), constrained_layout = True)
ax1 = fig.add_subplot(2, 2, 1)
ax2 = fig.add_subplot(2, 2, 2)
ax3 = fig.add_subplot(2, 2, 3)

# Prepare and print pre Seaborn plot
plot = sns.lineplot(data = df_final_pre, ax = ax1, x='freq',y='coh',hue='channel')
plot.set_xlabel('freq')
plot.set_ylabel('coh')
plot.set_xticks(range(10,61,10))
plot.set_xticklabels([5, 10, 15, 20, 25, 30])
plot.axvline(7, 0, color = 'k')
plot.axvline(15, 0, color = 'k')

# Prepare and print pre Seaborn plot
plot = sns.lineplot(data = df_final_post, ax = ax2, x='freq',y='coh', hue='channel')
plot.set_xlabel('freq')
plot.set_ylabel('coh')
plot.set_xticks(range(10,61,10))
plot.set_xticklabels([5, 10, 15, 20, 25, 30])
plot.axvline(7, 0, color = 'k')
plot.axvline(15, 0, color = 'k')

# Prepare and print delta Seaborn plot
plot = sns.lineplot(data = df_final_sub, ax = ax3, x='freq',y='coh', hue='channel')
plot.set_xlabel('freq')
plot.set_ylabel('coh')
plot.set_xticks(range(10,61,10))
plot.set_xticklabels([5, 10, 15, 20, 25, 30])
plot.axvline(7, 0, color = 'k')
plot.axvline(15, 0, color = 'k')

plt.savefig(sg.path_name + '\\' + sg.ani_num + '_' + sg.rec_day + '_coh_vs_freq.png')
plt.show()