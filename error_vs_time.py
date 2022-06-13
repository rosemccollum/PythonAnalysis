''' Graph error of TORTE and ASIC models ''' 
import imp
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import numpy as np
import pandas as pd
import scipy.io as scio
import seaborn as sns
import matplotlib.pyplot as plt
import math
import matlab.engine
from TORTE_vs_time import getTORTE 
from ground_truth import groundTruth

print("starting...")
# Load matlab files
Tk().withdraw() 
file = askopenfilename()
print("File: ", file)

# Call phase calculation functions and convert to list
df_gtp = groundTruth(file)
gtp = df_gtp.values.tolist()
torte = getTORTE(file)

# Calc circular distance b/w points
eng = matlab.engine.start_matlab()
mat_gtp = matlab.double([gtp])
mat_torte = matlab.double([torte])
mat_dist = eng.circ_dist(mat_gtp, mat_torte, nargout = 1) 
eng.quit()

# Convert to degrees
rad_dist = np.asarray(mat_dist)
rad_dist = rad_dist[0]
dist = []
d = 0
for d in range(0, len(rad_dist)):
    temp_degrees = math.degrees(rad_dist[d])
    dist.append(temp_degrees)

# # Subtract TORTE phase from GTP 
# p = 0
# torte_error = []
# for p in range (len(torte)):
#     diff = torte[p][0] - gtp[p][0]
#     torte_error.append(abs(diff))

# Write time points
t = 0
time = []
for t in range(len(torte)):
    time.append(t)

# Make dataframe
error_df = pd.DataFrame(dist)
error_df.columns = ["TORTE_Error"]
error_df['time'] = time

# Split file name to get rat and day data
temp = file.split("/")
fileName = temp[-1]
fileName = fileName.split("_")
for word in fileName:
    if "dev" in word:
        rat = word
    elif "day" in word:
        day = word
    elif ('POST' in word) or ("PRE" in word):
        condition = word
dir = file.split("RAW")

# Graph error over time 
print("graphing...")
sns.set(font_scale = 1.5)
fig = plt.figure(figsize = (13,7))
plot = sns.lineplot(data = error_df, x ="time", y = "TORTE_Error")
plot.set_title("TORTE Error Over Time")
plot.set_xticks(range(0, 1805, 20))
plot.set_xticklabels(range(0, 1805, 20))
plot.axhline(0, color = 'dimgray', ls = '--')
# plt.savefig(dir[0] + rat + '_' + day + "_" + "_CircDistDegreesSampleError_over_time")
plt.show()
print("done")