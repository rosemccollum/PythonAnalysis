import scipy.io as scio
import seaborn as sns
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# load demo dataset
df_final = pd.read_csv('heat_demo.csv')

# Label x and y axis
y_label = np.arange(1,9,1)
# Prepare and print Seaborn plot
plot = sns.heatmap(data =df_final,xticklabels = x_label, yticklabels = y_label, cbar_kws={'label': 'Coherence'},cmap="viridis")
plot.set(title="Change in Coherence Spectra", xlabel="Frequency (HZ)", ylabel="Channel cmb #")
plt.show()
