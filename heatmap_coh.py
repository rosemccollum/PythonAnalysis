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
#precoh_name = os.path.join(sg.path_name, 'RAW_PRE_' + sg.ani_num + "_" + sg.rec_day + "_coh")
precoh_mat = scio.loadmat(precoh_name)

# Choose and open post file
print('Choose post data file')
Tk().withdraw()
postcoh_name = askopenfilename()
print("File: ", postcoh_name)
#postcoh_name = os.path.join(sg.path_name, 'RAW_POST_' + sg.ani_num + "_" + sg.rec_day + "_coh")
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

# Create delta dataframe
delta_df = post_df.subtract(pre_df)

# Label x and y axis
y_label = np.arange(1, num_chan + 1, 1)
x_ticks = np.arange(0,61,10)
x_labels = range(0,31,5)

# Plot all three graphs 
fig = plt.figure(figsize = (9,8), constrained_layout = True)
ax1 = fig.add_subplot(2, 2, 1)
ax2 = fig.add_subplot(2, 2, 2)
ax3 = fig.add_subplot(2, 2, 3)

pre_plot = sns.heatmap(data = pre_df, ax = ax1, yticklabels = y_label, cbar_kws={'label': 'Coherence'},cmap="viridis")
pre_plot.set_xticks(x_ticks)
pre_plot.set_xticklabels(x_labels)
pre_plot.set(title="Pre Coherence Spectra", xlabel="Frequency (HZ)", ylabel="Channel cmb #")
pre_plot.axvline(x=7, color = 'black')
pre_plot.axvline(x=16, color = 'black')

post_plot = sns.heatmap(data = post_df, ax = ax2, yticklabels = y_label, cbar_kws={'label': 'Coherence'},cmap="viridis")
post_plot.set_xticks(x_ticks)
post_plot.set_xticklabels(x_labels)
post_plot.set(title="Post Coherence Spectra", xlabel="Frequency (HZ)", ylabel="Channel cmb #")
post_plot.axvline(x=7, color = 'black')
post_plot.axvline(x=16, color = 'black')

d_plot = sns.heatmap(data = delta_df, ax = ax3, yticklabels = y_label, cbar_kws={'label': 'Coherence'},cmap="viridis")
d_plot.set_xticks(x_ticks)
d_plot.set_xticklabels(x_labels)
d_plot.set(title="Change in Coherence Spectra", xlabel="Frequency (HZ)", ylabel="Channel cmb #")
d_plot.axvline(x=7, color = 'black')
d_plot.axvline(x=16, color = 'black')
plt.show()
print('done')
