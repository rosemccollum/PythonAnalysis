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

# Load matlab files
print("Choose the pre coherence file")
Tk().withdraw() 
precoh_name = askopenfilename()
print("File: ", precoh_name)
precoh_mat = scio.loadmat(precoh_name)

print("Choose the post coherence file")
Tk().withdraw() 
postcoh_name = askopenfilename()
print("File: ", postcoh_name)
postcoh_mat = scio.loadmat(postcoh_name)

print("Choose the pre power file")
Tk().withdraw()
prepow_name = askopenfilename()
print("File: ", prepow_name)
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

# Adding chan labels
temp_df = pd.read_csv(filename)
temp_df.insert(0, column='freq', value = channels)
temp_df.to_csv(filename, index = False)

# Writes CSV value w/ pre pwr, no channel lables  
filename = 'prepowerdata.csv'
i = 0
with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(freq)
    for i in range(len(pre_pow)):
        csvwriter.writerow(pre_pow[i])

# Adding chan labels 
temp_df = pd.read_csv(filename)
temp_df.insert(0, column='freq', value = pow_channels)
temp_df.to_csv(filename, index = False)

# Load into pandas data frame
precoh_df = pd.read_csv('precohdata.csv',index_col=False)
postcoh_df = pd.read_csv('postcohdata.csv', index_col= False)
prepow_df = pd.read_csv('prepowerdata.csv', index_col = False)

# Drop unnecessary columns from dfs (just want 4-12) 
i = 7
j = 24
h = 0
wanted_freq = pd.DataFrame()
while i < j:
    wanted_freq.insert(h, freq[i], precoh_df[str(freq[i])])
    i +=1 
    h +=1

chan_labels = precoh_df['freq']
precoh_df = wanted_freq
precoh_df.insert(0, 'freq', chan_labels)

i = 7
j = 24
h = 0
wanted_freq = pd.DataFrame()
while i < j:
    wanted_freq.insert(h, freq[i], postcoh_df[str(freq[i])])
    i += 1 
    h +=1

chan_labels = postcoh_df['freq']
postcoh_df = wanted_freq
postcoh_df.insert(0, 'freq', chan_labels)

i = 7
j = 24
h = 0
wanted_freq = pd.DataFrame()
while i < j:
    wanted_freq.insert(h, freq[i], prepow_df[str(freq[i])])
    i +=1 
    h +=1

chan_labels = prepow_df['freq']
prepow_df = wanted_freq
prepow_df.insert(0, 'freq', chan_labels)

# Take of chan labels to do math
pre_coh_labels = precoh_df['freq']
del precoh_df['freq']

post_coh_labels = postcoh_df['freq']
del postcoh_df['freq']

pre_pow_labels = prepow_df['freq']
del prepow_df['freq']

# Averaging across theta band
avg_pre_coh = precoh_df.mean(axis = 1)
avg_post_coh = postcoh_df.mean(axis = 1)
avg_pre_pow = prepow_df.mean(axis = 1)

# Turning avg series back into dataframe
precoh_df = avg_pre_coh.to_frame()
postcoh_df = avg_post_coh.to_frame()
prepow_df = avg_pre_pow.to_frame()

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

# Graph it
fig = plt.figure(figsize = (11,6))
plot = sns.scatterplot(data = final_df, x = 'pow', y = 'coh', hue = 'BLA')
plot.set_xlabel('Pre Power')
plot.set_ylabel('Delta Coherence')
plot.set_xticks(pow_values)
plot.set_xticklabels(pow_labels)
plt.grid()

# Save fig w/ day and name
dir = precoh_name.split('RAW')
temp = precoh_name.split('/')
for l in range(len(temp)):
    if 'dev' in temp[l] and 'RAW' not in temp[l]:
        rat = temp[l]
    if 'day' in temp[l] and 'RAW' not in temp[l]:
        day = temp[l]
    
plt.savefig(dir[0] + rat + '_' + day + '_prepow_vs_deltacoh.png')
plt.show()
print('done')