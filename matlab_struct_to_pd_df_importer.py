# TNEL Matlab struct viewer, 18Nov2021
import scipy.io as scio
import numpy as np
import pandas as pd

# What is Matlab file path?
matlab_file_path = r'/media/jon/My Passport/dev_2111/day1/CLOSED_LOOP_dev_2111_day1_cleandata_struct.mat'
mat_file = scio.loadmat(matlab_file_path)

# Specify struct name
struct_name_lvl1 = 'cur_data' # Edit this to the name of the struct you are interested in. Continue as needed
struct_name_lvl2 = 'seconds'
### struct_name_lvl3 = ''
mat_file = mat_file[struct_name_lvl1]
mat_file = mat_file[struct_name_lvl2]
### mat_file = mat_file[struct_name_lvl3]

layer1 = mat_file[0]
layer2 = mat_file[0][0]
layer3 = mat_file[0][0][0]
layer4 = mat_file[0][0][0][0]

# Remove excess array layers - stop when you are at the base array
print(layer1,layer2,layer3,layer4)

final_file = layer2 # change this as needed, each layer strips an array

df = pd.DataFrame(final_file) # Columns can be added with Columns = [] argument

# Optional - export array to .csv
### df.to_csv('myfile.csv')
### Optional - print first 10 rows of data
print(df.head())
