# Goal of script is to turn initial pandas DataFrames for pre and post stimulation coherence into a 3x1 plot with pre/post/delta conherence

import scipy.io as scio
import seaborn as sns
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load in matlab files
pre_mat = scio.loadmat(r'E:\dev2111\day2\RAW_PRE_dev2111_day2_coh')
post_mat = scio.loadmat(r'E:\dev2111\day2\RAW_POST_dev2111_day2_coh')
pre_coh = pre_mat['coh_spect'] # Goes into power data
post_coh = post_mat['coh_spect']
freq = pre_mat['freq'][0]  # Gives list of freq values
channels_mat = pre_mat['cmb_labels']

# Writes list of channels to use for plotting
h = 0 
channels = []
for g in range(len(channels_mat)):
    channels.append(channels_mat[g][0][0])

# Writes CSV value w/ pre pwr, no channel lables  
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

# Writes CSV w/ post pwr, no channel lables 
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

# # Pandas Concatination
df_3 = pd.concat([df_new, df_2_new, sub_df])

pd.set_option("display.max_rows", None)

# Pull frequency data from the index and create new 'freq' column
df_3['freq'] = df_3.index

# Remove the frequency data from the index
df_3.reset_index(drop=True, inplace=True)
# Remove index name from df_3
# Drop first column of dataframe
df_3 = df_3[['freq', channels[0], channels[1], channels[2], channels[3], channels[4], channels[5], channels[6], channels[7],'period']]

ch_num = 8 # Number of channels - 8 by default. This defines number of while loops
loop_num = ch_num +1 # This is to make sure we can put in the channel number literally and still get the loop to run the correct number of times
m = 1
l = 0

# Build df_final before while loop
column_list = ['freq','coh','period','channel']
global df_final
df_final = pd.DataFrame(columns=column_list)  

# while loop to create final DataFrame (df_final)
while m < loop_num:
    channel = channels[l]  
    df_loop = df_3[['freq',channel,'period']]
    df_loop['channel'] = channel
    df_loop.rename({channel: 'coh'},axis=1, inplace=True)
    m += 1
    l += 1
    df_final = df_final.append(df_loop)
    del df_loop

# df_final postprocessing
df_final = df_final.reset_index()
df_final = df_final[['freq','coh','channel','period']]

# Prepare and print Seaborn plot
plot = sns.relplot(data =df_final,x='freq',y='coh',kind='line',col='period',hue='channel')
plot.set_xlabels('freq')
plot.set_ylabels('coh')
plot.axes[0][0].set_xticks(range(10,61,10))
plot.axes[0][0].set_xticklabels([10, 20, 30, 40, 50, 60])
plt.axvline(8,0,0.9)
plt.axvline(4,0,0.9)
plt.show()
