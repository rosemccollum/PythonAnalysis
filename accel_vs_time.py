''' Most code borrowed from Jon's gaussian_demo, manipulated to show just accelerometry data. rae McCollum, 17 Mar 22'''    
import os
from tkinter.filedialog import askopenfilename
from urllib.parse import parse_qs

from cv2 import GaussianBlur
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.io as scio
import scipy.ndimage.filters as filters
import seaborn as sns
from tkinter import Tk
from sklearn import preprocessing
import math

print("starting...")
# Load matlab files
Tk().withdraw() 
file = askopenfilename()
print("File: ", file)
mat = scio.loadmat(file)

# Grab necessary information
mat_data =  mat['cur_data']['ds_data']
mat_time = mat['cur_data']['seconds']

cleandata_matlab_struct = mat_data[0][0] 

if len(cleandata_matlab_struct) < 35:
    print("This file does not contain accelerometry data, please run again with a new file")
    exit()

# Split file name to get condition, rat and day data
temp = file.split("/")
fileName = temp[-1]
fileName = fileName.split("_")
for word in fileName:
    if "dev" in word:
        rat = word
    elif "day" in word:
        day = word

dir = file.split("RAW")
condition = dir[1].split("_")
condition = condition[1]

# Make dataframe 
df = pd.DataFrame(cleandata_matlab_struct)
print("making data frame")

# Reformat DataFrame
df_final = df.iloc[np.r_[1:2,32:35],:20000] ## Channels 33-35 hold accelerometry data 
df_final = df_final.T
    
df_final.columns = ['lfp','aux1 (x)', 'aux2 (y)', 'aux3 (z)']
df_final['abs'] = np.sqrt(abs(pow(df_final['aux1 (x)'],2) + pow(df_final['aux2 (y)'],2) + pow(df_final['aux3 (z)'],2)))

# Apply filter 
gaussian = filters.gaussian_filter1d(df_final['abs'],sigma=15)
df_final['gaussian'] = gaussian
df_final_clean = df_final[['abs','gaussian','lfp',]]

# Taking difference of acc data 
acc = df_final['gaussian']
delta_list = []
j = 1
for i in range(0, len(acc)-1) :
    delta_list.append(acc[j] - acc[i])
    j += 1 
delta_list.append(0)
df_final['gaussian'] = delta_list

print("graphing...")    
# Plot results using Seaborn
sns.set(font_scale = 1.5)
fig = plt.figure(figsize = (13,8))
ax = sns.lineplot(data=gaussian, color='#EF3D59')
ax.set_title('Acceleration Vs. Time (s) - {} {} {}'.format(rat,day,condition))
ax.set_xlabel('Time (s)')
ax.set_ylabel('Acceleration (mV/g)')
ax.set_xticklabels([0, 60, 120, 180, 240, 300], rotation = 45)
ax.set(xlim =(0, 10000))
print("done")
plt.savefig(dir[0] + rat + '_' + day + "_" + condition + "_filteredAccel_over_time")
plt.show()