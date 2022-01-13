# Adapted from: TNEL Matlab struct viewer by Jon Whear on 18Nov2021
# This Version (intan_accelerometry_struct_viewer.py) Createdn 12Jan2022 by Jon Whear
import scipy.io as scio
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import math

# What is Matlab file path?
matlab_file_path = r'D:\EPHYSDATA\TESTS\Accelerometry\RAW_PRE_TESTS_Accelerometry_cleandata_struct.mat'
mat_file = scio.loadmat(matlab_file_path)

# Specify struct name
struct_name_lvl1 = 'cur_data' # Edit this to the name of the struct you are interested in. Continue as needed
struct_name_lvl2 = 'ds_data'
mat_file = mat_file[struct_name_lvl1]
mat_file = mat_file[struct_name_lvl2]

# Specify layer configurations
layer1 = mat_file[0]
layer2 = mat_file[0][0]
final_file = layer2 # change this as needed, each layer strips an array

df = pd.DataFrame(final_file)
df_final = df.iloc[32:35,:] # This corresponds to 33-35 in MatLab (0 index 33-1 ==32, and 35-1 == 34)

# Transpose DataFrame
df_final = df_final.T

# Add columns to DataFrame
df_final.columns = ['aux1 (x)', 'aux2 (y)', 'aux3 (z)']

# Add logic for finding absolute acceleration (from Rebecca's 14Dec2021 lab presentation)
df_final['abs'] = np.sqrt(abs(pow(df_final['aux1 (x)'],2) + pow(df_final['aux2 (y)'],2) + pow(df_final['aux3 (z)'],2)))

# Optional - export array to .csv for future usage
### csv_file_name = 'my_file.csv' # Change this to clarify what this .csv actually is showing
### df.to_csv(csv_file_name)

# Optional - print first 10 rows of data to inspect for changes
### print(df_final.head(10))

# Plot results using Seaborn
ax = sns.lineplot(data=df_final['abs'])
plt.show()
