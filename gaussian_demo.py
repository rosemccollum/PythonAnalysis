import scipy.io as scio
import scipy.ndimage.filters as filters
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from tkinter.filedialog import askopenfilename

matlab_file_path = askopenfilename()
mat_log_file = scio.loadmat(matlab_file_path)
record_dir_char = 'record_dir'
rat_char = 'rat'
day_char = 'day'
paths_char = 'paths'

# Specify structure to search MatLab files for char information
mat_log_record_dir = mat_log_file[record_dir_char]
mat_log_rat = mat_log_file[rat_char]
mat_log_day = mat_log_file[day_char]
mat_log_paths = mat_log_file[paths_char]

# Specify exact location to find each char
record_dir = mat_log_record_dir[0]
rat = mat_log_rat[0]
day = mat_log_day[0]
paths = mat_log_paths #[0]
# Strip excess spaces in path names
paths = [i.strip(' ') for i in paths]

# Will need to create a way to read this from log_file.mat and use that logic to determine seconds
seconds = 600
condition = "RAW_PRE"

data_dir = '{}\{}_{}_{}_cleandata_struct.mat'.format(record_dir,condition,rat,day)
mat_file = scio.loadmat(data_dir)
struct_name_lvl1 = 'cur_data'
struct_name_lvl2 = 'ds_data'

mat_file = mat_file[struct_name_lvl1]
mat_file = mat_file[struct_name_lvl2]

cleandata_matlab_struct = mat_file[0][0]

df = pd.DataFrame(cleandata_matlab_struct)

# Reformat DataFrame
df_final = df.iloc[32:35,:]
df_final = df_final.T
df_final.columns = ['aux1 (x)', 'aux2 (y)', 'aux3 (z)']
df_final['abs'] = np.sqrt(abs(pow(df_final['aux1 (x)'],2) + pow(df_final['aux2 (y)'],2) + pow(df_final['aux3 (z)'],2)))

print(df_final.head(30))

df_final_seconds = df_final
# Plot results using Seaborn
ax = sns.lineplot(data=df_final_seconds,) #color='#FF5733')
ax.set(ylim = (0,2000))
ax.set(xlim =(0,seconds))
ax.set_title('Acceleration Vs. Time (s) - {} {}'.format(rat,day))
ax.set_xlabel('Time (s)')
ax.set_ylabel('Acceleration')

gaussian = filters.gaussian_filter1d(df_final_seconds['abs'],sigma = 20)

ax = sns.lineplot(data=gaussian,color='#581845') #FFC300')
ax.set(ylim = (0,2000))
ax.set(xlim =(0,seconds))
ax.set_title('Acceleration Vs. Time (s) - {} {}'.format(rat,day))
ax.set_xlabel('Time (s)')
ax.set_ylabel('Acceleration')
plt.show()
