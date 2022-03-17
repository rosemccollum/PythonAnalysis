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
from sklearn import preprocessing

### Chose your log_file.mat location ###
### Keep this off for de-bugging ###

# file_path = r'D:\EPHYSDATA'
# Moving this slowly to the server Z drive #
# file_path = r'Z:\projmon\virginia-dev\01_EPHYSDATA\'


### For debugging ###
drive = r'Z:\projmon\virginia-dev'
location = '01_EPHYSDATA'
rat_d = 'dev2107'
day_d = 'day9'
file_path = os.path.join(drive) # This is used only when on Z drive, otherwise use file_path on line 19

### For File Explorer ###
# matlab_file_path = askopenfilename()
## USE W/ D Drive ## matlab_file_path = os.path.join(file_path, rat_d, day_d,'log_file.mat')
matlab_file_path = os.path.join(drive, location, rat_d, day_d,'log_file.mat')

mat_log_file = scio.loadmat(matlab_file_path)
record_dir_char = 'record_dir'
rat_char = 'rat'
day_char = 'day'
paths_char = 'paths'
raw_time_char = 'rawTime'

### Search MatLab files for char info ###
mat_log_record_dir = mat_log_file[record_dir_char]

try: # See comments on line 67
    mat_log_rat = mat_log_file[rat_char]
except:
    print("Unable to find rat in log_file.m, defaulting to rat_d value")

try:
    mat_log_day = mat_log_file[day_char]
except:
    print("Unable to find day in log_file.m, defaulting to rat_d value")


mat_log_paths = mat_log_file[paths_char]
mat_log_raw_time = mat_log_file[raw_time_char]

### Linux ###
# record_dir = mat_log_record_dir[0]
# record_dir = r'/home/jon/Desktop/EPHYS/dev2107/day15/'

### Windows ###
# Issues w/ string literal
## USE W/ D Drive ## record_dir = os.path.join('D:\EPHYSDATA\dev2110\day17')
record_dir = os.path.join(drive, location, rat_d, day_d)

try: # Try is my fancy way I WANT this to go in the long run - allows you to use file explorer to pick log_file
    rat = mat_log_rat[0]
except: # Except is needed to work with older versions of log_file.m before I added rat and day to Simple_CL.py code
    rat = rat_d

try:
    day = mat_log_day[0]
except:
    day = day_d

paths = mat_log_paths #[0]
raw_time = mat_log_raw_time[0][0]

### Strip excess spaces in path names ###
paths = [i.strip(' ') for i in paths]

# Will need to create a way to read this from log_file.mat and use that logic to determine seconds
seconds = raw_time * 60
condition = "RAW_PRE"

### Linux ###
# data_dir = '{}/{}_{}_{}_cleandata_struct.mat'.format(record_dir,condition,rat,day)

### Windows ###
# Issues w/ string literal
data_dir = os.path.join(drive, location, rat, day, condition + '_' + rat + '_' + day + '_cleandata_struct.mat')

mat_file = scio.loadmat(data_dir)
struct_name_lvl1 = 'cur_data'
struct_name_lvl2 = 'ds_data'

mat_file = mat_file[struct_name_lvl1]
mat_file = mat_file[struct_name_lvl2]

cleandata_matlab_struct = mat_file[0][0]

def graph_gaussian():
    df = pd.DataFrame(cleandata_matlab_struct)

    # Reformat DataFrame
    df_final = df.iloc[32:35,:]
    df_final = df_final.T
    df_final.columns = ['aux1 (x)', 'aux2 (y)', 'aux3 (z)']
    df_final['abs'] = np.sqrt(abs(pow(df_final['aux1 (x)'],2) + pow(df_final['aux2 (y)'],2) + pow(df_final['aux3 (z)'],2)))

    df_final_seconds = df_final

    gaussian = filters.gaussian_filter1d(df_final_seconds['abs'],sigma = 20)
    # Plot results using Seaborn
    # ax = sns.lineplot(data=df_final_seconds['abs'],color='#feb236')
    ax = sns.lineplot(data=gaussian,color='#ff7b25')
    ax.set(xlim =(0,2000))
    ax.set(ylim = (-1000,2000))
    ax.set_title('Acceleration Vs. Time (s) - {} {}'.format(rat,day))
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Acceleration')
    plt.show()

def accel_vs_lfp():
    # Accel is in at least one of my demo datasets - I'm thinking dev9999 day99
    df = pd.DataFrame(cleandata_matlab_struct)

    # Reformat DataFrame
    df_final = df.iloc[np.r_[1:2,32:35],:20000]
    df_final = df_final.T
    
    df_final.columns = ['lfp','aux1 (x)', 'aux2 (y)', 'aux3 (z)']
    df_final['abs'] = np.sqrt(abs(pow(df_final['aux1 (x)'],2) + pow(df_final['aux2 (y)'],2) + pow(df_final['aux3 (z)'],2)))
    df_final['abs'] = df_final['abs'] - 588.897

    gaussian = filters.gaussian_filter1d(df_final['abs'],sigma=30)
    gaussian_lfp = filters.gaussian_filter1d(df_final['lfp'],sigma=20)

    df_final['gaussian'] = gaussian
    df_final['gaussian_lfp'] = gaussian_lfp

    df_final_clean = df_final[['abs','gaussian','lfp','gaussian_lfp']]
    
    # Plot results using Seaborn
    ax = sns.lineplot(data=gaussian, color='#EF3D59')
    ax = sns.lineplot(data=df_final['lfp'], color='#EFC958')
    ax = sns.lineplot(data=gaussian_lfp, color='#344E5C')
    
    
    corr_matrix = np.corrcoef(gaussian, gaussian_lfp)
    corr = corr_matrix[0,1]
    r_sq = corr**2

    ax.set_title('Acceleration Vs. Time (s) - {} {} r**2 = {}'.format(rat,day,r_sq))
    ax.set_xlabel('Time (ms)')
    ax.set_ylabel('Acceleration (mV/g)')
    ax.set(xlim =(0, 10000))
    ax.set(ylim = (-1000, 2000))

    plt.show()

def normalized_accel_vs_lfp():
    # Accel is in at least one of my demo datasets - I'm thinking dev9999 day99
    df = pd.DataFrame(cleandata_matlab_struct)

    # Reformat DataFrame
    df = df.iloc[np.r_[1:2,32:35],:1000]
    df = df.T
    df.columns = ['lfp','aux1 (x)', 'aux2 (y)', 'aux3 (z)']
    df['abs'] = np.sqrt(abs(pow(df['aux1 (x)'],2) + pow(df['aux2 (y)'],2) + pow(df['aux3 (z)'],2)))

    # Define Gaussian filters
    gaussian = filters.gaussian_filter1d(df['abs'],sigma=5)
    gaussian_lfp = filters.gaussian_filter1d(df['lfp'],sigma=5)

    df['gaussian'] = gaussian
    df['gaussian_lfp'] = gaussian_lfp

    # print(df.head(3))
    # print(df.describe())
    # The issue with this way of normalizing is that it washes out abs, which changes less than spiking
    
    # df_lfp_g_pre = df['lfp'].values.reshape(1,-1)
    # was previously using normalize

    np_lfp_g = preprocessing.scale(df['lfp'], axis=0)
    np_acc_g = preprocessing.scale(df['abs'], axis=0)
    df_scale = pd.DataFrame({'lfp':np_lfp_g, 'abs':np_acc_g})
    np_normal = np_normal = preprocessing.normalize(df_scale, axis = 0)
    df_normal = pd.DataFrame(np_normal)
    print(df_normal.head())

    # np_normal = preprocessing.normalize(df, axis = 0)
    # df_normal = pd.DataFrame(np_normal)

    # print(df_normal.info())
    # print(df_normal.describe())

    #df_normal2 = df_normal.rename(columns={'0':'A','1':'B','2':'C','3':'D','4':'E','5':'F','6':'G'})
    df_normal.columns = ['gaussian', 'gaussian_lfp']
    # print(df_normal.head(10))


    # Plot results using Seaborn
    ax = sns.lineplot(data=df_normal['gaussian'], color='#EF3D59')
    # ax = sns.lineplot(data=df_final['lfp'], color='#EFC958')
    ax = sns.lineplot(data=df_normal['gaussian_lfp'], color='#344E5C')
    
    corr_matrix = np.corrcoef(gaussian, gaussian_lfp)
    corr = corr_matrix[0,1]
    r_sq = corr**2

    ax.set_title('Acceleration Vs. Time (s) - {} {} r**2 = {}'.format(rat,day,r_sq))
    ax.set_xlabel('Time (ms)')
    ax.set_ylabel('Acceleration (mV/g)')
    ax.set(xlim =(0, 100))
    ax.set(ylim = (-0.25, 0.25))

    plt.show()

def accel_vs_lfp_scatter():
    df = pd.DataFrame(cleandata_matlab_struct)

    ### Reformat DataFrame ###
    df = df.iloc[np.r_[1:2,32:35],:100000]
    df = df.T
    df.columns = ['lfp','aux1 (x)', 'aux2 (y)', 'aux3 (z)']
    df['abs'] = np.sqrt(abs(pow(df['aux1 (x)'],2) + pow(df['aux2 (y)'],2) + pow(df['aux3 (z)'],2)))

    ### Define Gaussian filters ###
    gaussian = filters.gaussian_filter1d(df['abs'],sigma=20)
    gaussian_lfp = filters.gaussian_filter1d(df['lfp'],sigma=5)

    df['gaussian'] = gaussian
    df['gaussian_lfp'] = gaussian_lfp

    np_lfp_g = preprocessing.scale(df['lfp'], axis=0)
    np_acc_g = preprocessing.scale(df['abs'], axis=0)
    df_scale = pd.DataFrame({'lfp':np_lfp_g, 'abs':np_acc_g})
    np_normal = np_normal = preprocessing.normalize(df_scale, axis = 0)
    df_normal = pd.DataFrame(np_normal)
    df_normal.columns = ['gaussian', 'gaussian_lfp']
    
    ### Plot results w/ sns ###
    ax = sns.scatterplot(data=df_normal, x ='gaussian', y = 'gaussian_lfp')
    ax.set_title('Acceleration Vs. LFP (scaled/normalized')
    ax.set_xlabel('Acceleration')
    ax.set_ylabel('LFP')
    # ax.set(xlim =(0, 100))
    # ax.set(ylim = (-0.25, 0.25))

    plt.show()

def accel_vs_lfp_scatter_raw():
    df = pd.DataFrame(cleandata_matlab_struct)

    ### Reformat DataFrame ###
    df = df.iloc[np.r_[1:2,32:35],:100000]
    df = df.T
    df.columns = ['lfp','aux1 (x)', 'aux2 (y)', 'aux3 (z)']
    df['abs'] = np.sqrt(abs(pow(df['aux1 (x)'],2) + pow(df['aux2 (y)'],2) + pow(df['aux3 (z)'],2)))
    
    ### Plot results w/ sns ###
    ax = sns.scatterplot(data=df, x ='abs', y = 'lfp')
    ax.set_title('Acceleration Vs. LFP')
    ax.set_xlabel('Acceleration (mV/g)')
    ax.set_ylabel('LFP')
    
    plt.show()

def accel_vs_lfp_scatter_raw_heat():
    df = pd.DataFrame(cleandata_matlab_struct)

    ### Reformat DataFrame ###
    df = df.iloc[np.r_[1:2,32:35],:30000]
    df = df.T
    df.columns = ['lfp','aux1 (x)', 'aux2 (y)', 'aux3 (z)']
    df['abs'] = np.sqrt(abs(pow(df['aux1 (x)'],2) + pow(df['aux2 (y)'],2) + pow(df['aux3 (z)'],2)))
    
    ### Plot results w/ sns ###
    ax = sns.scatterplot(data=df, x ='abs', y = 'lfp')
    sns.histplot(data=df, x ='abs', y = 'lfp', bins=100, pthresh=.001, cmap="mako")
    # sns.kdeplot(data=df, x ='abs', y = 'lfp', levels=5, color="w", linewidths=1)
    ax.set_title('Acceleration Vs. LFP')
    ax.set_xlabel('Acceleration (mV/g)')
    ax.set(xlim =(0, 500))
    ax.set_ylabel('LFP')

    plt.show()

def accel_vs_lfp_scatter_raw_heat_delta():
    df = pd.DataFrame(cleandata_matlab_struct)
    png_save_path = os.path.join(record_dir,"Accel-v-LFP-{}-{}-{}.png".format(rat, day, condition))

    ### Reformat DataFrame ###
    df = df.iloc[np.r_[1:2,32:35],:120000]
    df = df.T

    
    df.columns = ['lfp','aux1 (x)', 'aux2 (y)', 'aux3 (z)']
    df['abs'] = np.sqrt(abs(pow(df['aux1 (x)'],2) + pow(df['aux2 (y)'],2) + pow(df['aux3 (z)'],2)))

    abs_list = df['abs']
    delta_list = []
    j = 1
    k = 0
    
    for i in range(119999):
        delta_list.append(abs_list[j]-abs_list[k])
        j = j+1
        k = k+1

    delta_list.append('0')
    df['abs_delta'] = delta_list
    
    ### Plot results w/ sns ###
    ax = sns.scatterplot(data=df, x ='abs_delta', y = 'lfp')
    sns.histplot(data=df, x ='abs_delta', y = 'lfp', bins=100, pthresh=.001, cmap="mako")
    # sns.kdeplot(data=df, x ='abs', y = 'lfp', levels=5, color="w", linewidths=1)
    ax.set_title('Acceleration Vs. LFP - {} {} {}'.format(rat, day, condition))
    ax.set_xlabel('Acceleration (mV/g)')
    #ax.set(xlim =(0, 500))
    ax.set_ylabel('LFP')

    ax.set(ylim = (-1000,1000))
    ax.set(xlim = (-20,20))
    plt.savefig(png_save_path)
    plt.show()

def timeseries_viewer():
    png_save_path = os.path.join(record_dir,"LFP-{}-{}-{}.png".format(rat, day, condition))
    ### Build DF ###
    df = pd.DataFrame(cleandata_matlab_struct)

    ### Reformat DF ###
    df = df.iloc[3,:120000]
    df = df.T
    gaussian = filters.gaussian_filter1d(df,sigma=1)
    
    df_gaussian = pd.DataFrame(gaussian)

    ### Plot ###
    ax = sns.lineplot(data=df, color='#ff7b25')
    ax.set(xlim =(0,120000))
    ax.set(ylim = (-2000,2000))
    ax.set_title('LFP (\u03BCv) vs. Time (ms) - {} {} {}'.format(rat, day, condition)) # Unicode Char for micro
    ax.set_xlabel('Time (ms)')
    ax.set_ylabel('LFP (\u03BCv)')
    plt.savefig(png_save_path)
    plt.show()
    

def accel_vs_lfp_delta():
    df = pd.DataFrame(cleandata_matlab_struct)

    # Reformat DataFrame
    df_final = df.iloc[np.r_[1:2,32:35],:120000]
    df_final = df_final.T
    
    df_final.columns = ['lfp','aux1 (x)', 'aux2 (y)', 'aux3 (z)']
    df_final['abs'] = np.sqrt(abs(pow(df_final['aux1 (x)'],2) + pow(df_final['aux2 (y)'],2) + pow(df_final['aux3 (z)'],2)))
    abs_list = df_final['abs']
    delta_list = []
    j = 1
    k = 0

    
    for i in range(119999):
        delta_list.append(abs_list[j]-abs_list[k])
        j = j+1
        k = k+1

    delta_list.append('0')

    df_final['abs_delta'] = delta_list

    gaussian = filters.gaussian_filter1d(df_final['abs'],sigma=5)
    gaussian_lfp = filters.gaussian_filter1d(df_final['lfp'],sigma=5)

    df_final['gaussian'] = gaussian
    df_final['gaussian_lfp'] = gaussian_lfp

    df_final_clean = df_final[['abs','gaussian','lfp','gaussian_lfp','abs_delta']]
    print(df_final_clean)
    
    # Plot results using Seaborn
    ax = sns.lineplot(data=df_final_clean['abs_delta'], color='#EF3D59')
    #ax = sns.lineplot(data=df_final_clean['lfp'], color='#EFC958')

    plt.show()
    
# graph_gaussian()
accel_vs_lfp()
# normalized_accel_vs_lfp() # This finally works (line_plot) for scaled and then normalized data
# accel_vs_lfp_scatter() # This works really well! I wonder if my filters are making my data weird
# accel_vs_lfp_scatter_raw() # A scatter plot of the raw lfp data and raw accel data
# accel_vs_lfp_scatter_raw_heat() # scatter as above w/ heat map over top to display result density
# accel_vs_lfp_scatter_raw_heat_delta() # same as abocve but w/ Delta Accel
# timeseries_viewer()
# accel_vs_lfp_delta()