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

# Prepare and print pre Seaborn plot
pre_plot = sns.heatmap(data = pre_df, yticklabels = y_label, cbar_kws={'label': 'Coherence'},cmap="viridis")
pre_plot.set_xticks(x_ticks)
pre_plot.set_xticklabels(x_labels)
pre_plot.set(title="Pre Coherence Spectra", xlabel="Frequency (HZ)", ylabel="Channel cmb #")
pre_plot.axvline(x=7, color = 'black')
pre_plot.axvline(x=16, color = 'black')
plt.show()

# Prepare and print post Seaborn plot
plot = sns.heatmap(data = post_df, yticklabels = y_label, cbar_kws={'label': 'Coherence'},cmap="viridis")
plot.set_xticks(x_ticks)
plot.set_xticklabels(x_labels)
plot.set(title="Post Coherence Spectra", xlabel="Frequency (HZ)", ylabel="Channel cmb #")
plot.axvline(x=7, color = 'black')
plot.axvline(x=16, color = 'black')
plt.show()

# Prepare and print delta Seaborn plot
plot = sns.heatmap(data = delta_df, yticklabels = y_label, cbar_kws={'label': 'Coherence'},cmap="viridis")
plot.set_xticks(x_ticks)
plot.set_xticklabels(x_labels)
plot.set(title="Change in Coherence Spectra", xlabel="Frequency (HZ)", ylabel="Channel cmb #")
plot.axvline(x=7, color = 'black')
plot.axvline(x=16, color = 'black')
plt.show()
