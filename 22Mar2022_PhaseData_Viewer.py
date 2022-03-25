import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.io as scio
from scipy.io import savemat
import seaborn as sns
import h5py
import mat73
import math

def load_matlab_files(): # This will load files in the Matlab V7.3+ file format, which is required for >2GB
    ### Select File Locations ###
    drive = r'Z:\projmon\virginia-dev'
    location = '01_EPHYSDATA'
    rat = 'dev2110'
    day = 'day18'
    hidden = 'hidden' # This is for working on the CL or CL_pre files, which are hidden in another folder
    condition = "CLOSED_LOOP_Pre_2022-02-18_15-30-10"
    data_dir = os.path.join(drive, location, rat, day, hidden, condition, 'Phase_Data.mat') # Easiest way to work with paths between unix / windows systems
    data_dict = mat73.loadmat(data_dir) # mat73 allows importing matlab v7.3 files (scipy does not currently support)

    ### Load data into numpy arrays for usage w/i Python ###
    ## Phase Data ##
    phase_data = data_dict['phase_data']['Data'] # Access Data double values - 40x9026304 double
    phase_data = np.array(phase_data) # Convert to np array
    phase_data = phase_data[6,:] # This should select channel 7 (0 indexed)

    phase_timestamps = data_dict['phase_data']['Timestamps'] # Access Timestamp 9026304x1 int64 values
    phase_timestamps = np.array(phase_timestamps) # Convert to np array

    ## Event Data ##
    event_data = data_dict['event_data']['Data'] # 3687x1 int16 data
    event_data = np.array(event_data)

    event_timestamps = data_dict['event_data']['Timestamps'] # 3687x1 int64 data
    event_timestamps = np.array(event_timestamps)
    
    ## Event Data 2 - Stim Crossing Detector ##
    event_data_2 = data_dict['event_data_2']['Data'] # 3687x1 int16 data
    event_data_2 = np.array(event_data_2) # Convert to np array

    event_timestamps_2 = data_dict['event_data_2']['Timestamps'] # 3687x1 int64 data
    event_timestamps_2 = np.array(event_timestamps_2)

    ## Event Data 3 - Sham Crossing Detector ##
    event_data_3 = data_dict['event_data_3']['Data'] # 3687x1 int16 data
    event_data_3 = np.array(event_data_3) # Convert to np array

    event_timestamps_3 = data_dict['event_data_3']['Timestamps'] # 3687x1 int64 data
    event_timestamps_3 = np.array(event_timestamps_3)

    ### Turn np arrays into pandas Dataframes ###
    ## Phase DF ##
    df_phase = pd.DataFrame(phase_data*0.195) # 0.195 is the bit_volt conversion in the header file
    df_phase.columns = ['phase_data']
    df_phase['phase_timestamps'] = phase_timestamps

    ## Event DF ##
    df_event = pd.DataFrame(event_data)
    df_event.columns = ['event_data']
    df_event['event_timestamps'] = event_timestamps

    ## Event 2 DF ##
    df_event_2 = pd.DataFrame(event_data_2)
    df_event_2.columns = ['event_data_2']
    df_event_2['event_timestamps_2'] = event_timestamps_2

    ## Event 3 DF ##
    df_event_3 = pd.DataFrame(event_data_3)
    df_event_3.columns = ['event_data_3']
    df_event_3['event_timestamps_3'] = event_timestamps_3


    ### Save DFs to csv files for quicker access in future ###

    df_phase.to_csv(os.path.join(drive, location, rat, day, 'df_phase.csv'))

    df_event.to_csv(os.path.join(drive, location, rat, day, 'df_event.csv'))
    df_event_2.to_csv(os.path.join(drive, location, rat, day, 'df_event_2.csv'))
    df_event_3.to_csv(os.path.join(drive, location, rat, day, 'df_event_3.csv'))
    print('Done!')

def load_csv_files():
    drive = r'Z:\projmon\virginia-dev'
    location = '01_EPHYSDATA'
    rat = 'dev2110'
    day = 'day18'
    condition = "RAW_PRE"
    df_phase = pd.read_csv(os.path.join(drive, location, rat, day, 'df_phase.csv')) # load in csv file
    df_event_3 = pd.read_csv(os.path.join(drive, location, rat, day, 'df_event_3.csv'))
    df_event_3 = df_event_3.where(df_event_3['timestamps'] > 0) # This is a little lazy, but it works!
    df_event_3 = df_event_3.where(df_event_3['event_data_3'] > 1)
    df_event_3 = df_event_3.dropna()
    print(df_event_3.head()) # Mostly left on so that I can tell it's working

    df_event_2 = pd.read_csv(os.path.join(drive, location, rat, day, 'df_event_2.csv'))
    df_event_2 = df_event_2.where(df_event_2['timestamps'] > 0) # This is a little lazy, but it works!
    df_event_2 = df_event_2.where(df_event_2['event_data_2'] > 1)
    df_event_2 = df_event_2.dropna()
    print(df_event_2.head()) # Mostly left on so that I can tell it's working


    df_event = pd.read_csv(os.path.join(drive, location, rat, day, 'df_event.csv'))
    df_event = df_event.where(df_event['timestamps'] > 0) # This is a little lazy, but it works!
    df_event = df_event.where(df_event['event_data'] > 0)
    df_event = df_event.dropna()
    print(df_event.head()) # Mostly left on so that I can tell it's working

    range_lower = 820000
    range_upper = 1000000

    x_lim_lower = 24000000
    x_lim_upper = 24120000 # 150k is 5 seconds @ 30k sampling rate

    y_lim_lower = -180
    y_lim_upper = 180
    sample_rate = 1

    # All 3 events
    # legend

    # x_labels = [str(x_lim_lower/sample_rate),str((x_lim_lower+((x_lim_upper-x_lim_lower)/2))/sample_rate),str(x_lim_upper/sample_rate)]
    x_ticks = [24000000, 24030000, 24060000, 24090000, 24120000]
    x_labels = ['0', '1', '2', '3', '4']
    # y_pos = np.arange(len(x_labels))

    df_phase = df_phase[range_lower:range_upper]
    ax = sns.lineplot(data=df_phase, x=df_phase['timestamps'], y=df_phase['phase_data'])
    ax.set(ylim = (y_lim_lower, y_lim_upper))
    ax.set(xlim = (x_lim_lower, x_lim_upper))
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_labels)
    # ax.set_xticklabels(x_labels)

    ax.set_title("Phase \u00b0 vs Recording Time (S)")
    ax.set_xlabel('Time (S)')
    ax.set_ylabel('Phase \u00b0')

    for i in df_event_3['timestamps']:
        ax.axvline(i,0,1, color='#efc83d') # linewidth arg = x

    for i in df_event_2['timestamps']:
        ax.axvline(i,0,1, color='#EF3D59')
    
    for i in df_event['timestamps']:
        ax.axvline(i,0.25,0.75, color='#3defc3')

    plt.legend(labels=["Phase", "Sham (OEP Event Ch. 3)", "Stim (OEP Event Ch. 2)", "Phase Crossing (OEP Event Ch. 1)"], title = "Legend", loc = 2)
    plt.grid()
    plt.show()

# load_matlab_files()
load_csv_files()
