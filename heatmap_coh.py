import scipy.io as scio
import seaborn as sns
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import simple_GUI as sg
import os

# Load coh matlab
coh_name = os.path.join(sg.path_name, 'RAW_PRE_' + sg.ani_num + "_" + sg.rec_day + "_coh")
coh_mat = scio.loadmat(coh_name)

# Pull coh, freq, and chan data
coh = coh_mat['coh_spect']
freq = coh_mat['freq'][0]
num_chan = len(coh_mat['cmb_labels'])

# Write into CSV
filename = 'cohdata.csv'
i = 0
with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(freq)
    for i in range(len(coh)):
        csvwriter.writerow(coh[i])

# Load into pandas data frame
df = pd.read_csv('cohdata.csv',index_col=False)

# Label x and y axis
y_label = np.arange(1, num_chan + 1, 1)
x_ticks = np.arange(0,61,10)
x_labels = range(0,31,5)

# Prepare and print Seaborn plot
plot = sns.heatmap(data = df, yticklabels = y_label, cbar_kws={'label': 'Coherence'},cmap="viridis")
plot.set_xticks(x_ticks)
plot.set_xticklabels(x_labels)
plot.set(title="Change in Coherence Spectra", xlabel="Frequency (HZ)", ylabel="Channel cmb #")
plot.axvline(x=7, color = 'black')
plot.axvline(x=16, color = 'black')
plt.show()
