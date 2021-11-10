# coh vs freq graphs for coh mat files 
# looking at freq 4 - 8 Hz (col 8 - 16)
import scipy.io as scio
import seaborn as sns
import pandas as pd
import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Load necessary data from matlab file and oganizes necessary variables
pre_mat = scio.loadmat(r'E:\dev2111\day1\CLOSED_LOOP_dev2111_day1_coh')
pre_coh = pre_mat['coh_spect']
freq = pre_mat['coh']['freq'][0][0][0]
channels_mat = pre_mat['coh']['labelcmb']
#print('loaded file')

# Writes list of channel labels to use for plot
h = 0 
g = 0
channels = []
temp_chan = []
both_chan = ''
for g in range(len(channels_mat[0][0])):
    for h in range(2):
        temp_chan.append(channels_mat[0][0][g][h][0])
    both_chan = temp_chan[0] + ' ' + temp_chan[1]
    channels.append(both_chan)
    temp_chan = []
    both_chan = ''
#print('Channels:', channels)

# Writes CSV value w/ freq and coh for each channel, no channel lables  
filename = 'replicatecohdata.csv'
i = 0
with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(freq)
    for i in range(len(pre_coh)):
        csvwriter.writerow(pre_coh[i])
#print('wrote file')

# Turns CSV file into pandas dataframe to use for plotting
coh_df = pd.read_csv('replicatecohdata.csv', index_col= False)
coh_df = coh_df.transpose()

# Labels each column as channels 
l = 0
for l in range(len(channels)):
    coh_df = coh_df.rename(columns= {l: channels[l]})
#print(coh_df)
#print('created dataframe')

# Plots data w/ correct labels and ticks marks 
plot = sns.relplot(data = coh_df, kind = 'line')
plot.set_xlabels('freq')
plot.set_ylabels('coh')
plot.axes[0][0].set_xticks(range(10,61,10))
plot.axes[0][0].set_xticklabels([10, 20, 30, 40, 50, 60])
plt.axvline(8,0,0.9)
plt.axvline(4,0,0.9)
plt.show()
#print('done')