# Plot pre pwr vs delta pwr in scatter plot color coordinated by channel with the channel locked channel a bigger dot
import scipy.io as scio
import seaborn as sns
import pandas as pd
import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import math
import simple_GUI as sg
from tkinter import Tk   
from tkinter.filedialog import askopenfilename

# Choose and open pre and post file
Tk().withdraw() 
prepow_name = askopenfilename()
print("File: ", prepow_name)
prepow_mat = scio.loadmat(prepow_name)

Tk().withdraw() 
postpow_name = askopenfilename()
print("File: ", postpow_name)
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

# Remove strings so math can be done on whole data frame 
pre_chan_labels = pre_df['freq']
del pre_df['freq']

post_chan = post_df['freq']
del post_df['freq']

# Take log of pre and post dataframes 
pre_df = 10 * np.log10(pre_df)
post_df = 10 * np.log10(post_df)

# Put chan labels back 
pre_df.insert(0, 'freq', pre_chan_labels)
post_df.insert(0, 'freq', post_chan)

# Subtract post - pre coh
delta_df = post_df.set_index('freq').subtract(pre_df.set_index('freq'), fill_value=0)

# Transpose DataFrame
pre_df = pre_df.T
delta_df = delta_df.T

# Remove index and save to new DataFrame
pre_df.columns = pre_df.iloc[0]
pre_df_fin = pre_df[1:]

# FIXING DELTA DF
# Remove the frequency data from the index
delta_df.reset_index(drop = True, inplace = True)

# Drop first column of dataframe
delta_df = delta_df[[channels[0], channels[1], channels[2], channels[3], channels[4], channels[5], channels[6], channels[7]]]

# Turn into long form data
delta_melted = pd.melt(delta_df, value_vars=channels, var_name = 'chan', value_name= 'delta')

# FIXING PRE DF
# Remove the frequency data from the index
pre_df_fin.reset_index(drop = True, inplace = True)

# Drop first column of dataframe
pre_df_fin = pre_df_fin[[channels[0], channels[1], channels[2], channels[3], channels[4], channels[5], channels[6], channels[7]]]

# Turn into long form data
final_df = pd.melt(pre_df_fin, value_vars=channels, var_name = 'chan', value_name= 'pre')

# Adding delta column to pre data 
delta = delta_melted['delta']
final_df['delta'] = delta

plot = sns.scatterplot(data = final_df, x = 'pre', y = 'delta', hue = 'chan')
plot.set_title('Pre Power vs Delta Power')
plt.savefig(sg.path_name + '\\' + sg.ani_num + '_' + sg.rec_day + '_pre_pwr_vs_delta_pwr_scatterplot.png')
plt.show()
