### Import Dependencies ###
from scipy.signal import hilbert, filtfilt, butter
from scipy.stats import circmean, circvar
import scipy.io as scipy
import numpy as np
from numpy import angle
import os
import pandas as pd
import mat73
import seaborn as sns
import matplotlib.pyplot as plt

### Define Data Location ###
drive = r'Z:\projmon\virginia-dev'
location = '01_EPHYSDATA'
rat = 'dev2110'
day = 'day1'
condition = "CLOSED_LOOP_2021-10-28_10-40-21" # Include the entire name
hidden = 'hidden' # For files moved so that dev Matlab pathway doesn't run on CL section
data_dir = os.path.join(drive, location, rat, day, hidden, condition, 'Phase_Data.mat') # os.path.join() is easiest way to work with paths between unix / windows systems
data_dict = mat73.loadmat(data_dir) # mat73 allows importing matlab v7.3 files (scipy does not currently support)
coi = 1 # Channel of Interest (coi)

def load_matlab_files():
    ### Load data into numpy arrays for usage w/i Python ###
    ## Event Data ##
    event_data = data_dict['event_data']['Data'] # 3687x1 int16 data
    event_data = np.array(event_data) # Convert to np array

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
    ## Event DF ##
    df_event = pd.DataFrame(event_data)
    df_event.columns = ['event_data']
    df_event['timestamps'] = event_timestamps

    ## Event 2 DF ##
    df_event_2 = pd.DataFrame(event_data_2)
    df_event_2.columns = ['event_data']
    df_event_2['timestamps'] = event_timestamps_2

    ## Event 3 DF ##
    df_event_3 = pd.DataFrame(event_data_3)
    df_event_3.columns = ['event_data']
    df_event_3['timestamps'] = event_timestamps_3

    ### Save DFs to csv files for quicker access in future ###
    df_event.to_csv(os.path.join(drive, location, rat, day, 'df_event.csv'))
    df_event_2.to_csv(os.path.join(drive, location, rat, day, 'df_event_2.csv'))
    df_event_3.to_csv(os.path.join(drive, location, rat, day, 'df_event_3.csv'))
    print('Matlab Files Loaded')

def create_rose_plot():
    ### Load data into numpy arrays for usage w/i Python ###
    ### Large files are chopped at ~1 million cells by excel when opened as .csv ###

    ## LFP Timestamps to DF ##
    lfp_timestamps = data_dict['cont_data_LFP']['Timestamps']
    lfp_timestamps = np.array(lfp_timestamps)
    lfp_timestamps = pd.DataFrame(lfp_timestamps)

    ## LFP Data to DF ##
    lfp_data = data_dict['cont_data_LFP']['Data'] # Access Data double values - 40x9026304 double
    lfp_data = np.array(lfp_data) # Convert to np array
    lfp_data = lfp_data[coi-1,:] # coi-1 b/c Python is 0 indexed
    lfp_data = pd.DataFrame(lfp_data*0.195)
    lfp_data.columns = ['lfp_data']
    lfp_timestamps.columns = ['lfp_timestamps']

    ### Prepare DFs for off-line phase calc ###
    df = lfp_data['lfp_data']*5.12820512821 # New DF w/ only the phase_data information for now
    data = df # Get it to same syntax in Virginia's Matlab code

    ### Set some params ###
    fs = 30000 # sampling rate (default: 30000)
    lowpass = 4.0 # Hz
    low = lowpass / (fs/2)
    highpass = 8.0 # Hz
    high = highpass / (fs/2)
    order = 2

    ### Filter / Get Phase ###
    [b, a] = butter(order, [low, high], btype = 'band') # Butterworth digital and analog filter
    filtered_data = filtfilt(b, a, data)
    analytic_data = hilbert(filtered_data)
    phase_data = angle(analytic_data)
    phase_data = phase_data*180/3.14159

    df = pd.DataFrame(phase_data)
    df.columns = ['phase_data']
    df['timestamps'] = lfp_timestamps['lfp_timestamps']

    ### Read in previously saved .csv files ###

    ## DF Event 3 - Sham ##
    df_event_3 = pd.read_csv(os.path.join(drive, location, rat, day, 'df_event_3.csv')) # These .csv files can be read in b/c length is far under 10^6 rows
    df_event_3 = df_event_3.where(df_event_3['timestamps'] > 0) # This is a little lazy, but it works!
    df_event_3 = df_event_3.where(df_event_3['event_data'] > 1) # Turn negative events into NAN
    df_event_3 = df_event_3.dropna() # Remove all rows with NAN values
    
    ## Toggle on/off using stim for 2x data ##
    ## THIS ONLY WORKS IF STIM WAS NOT DELIVERED (No artifacts) ##
    include_stim = False # False for off (default)

    if include_stim == True:
        df_event_2 = pd.read_csv(os.path.join(drive, location, rat, day, 'df_event_2.csv')) # These .csv files can be read in b/c length is far under 10^6 rows
        df_event_2 = df_event_2.where(df_event_3['timestamps'] > 0) # This is a little lazy, but it works!
        df_event_2 = df_event_2.where(df_event_3['event_data'] > 1) # Turn negative events into NAN
        df_event_2 = df_event_2.dropna() # Remove all rows with NAN values
        df_event_3 = pd.concat([df_event_3, df_event_2])
        print(df_event_3.head(100))
        print(df_event_3.info())
        print(df_event_3.describe())

    df = df.merge(df_event_3, on='timestamps', how='inner') # Merge the DFs
    df_save_path = os.path.join(drive, location, rat, day) # Create a save path for .csv files (in phase)
    df.to_csv('{}\\{}_{}_{}_phase-event_data.csv'.format(df_save_path,rat, day, condition)) # Save csv

    ### Visualize Data ###
    bins = 10
    starting_deg = -180
    ending_deg = 180
    density = []
    step = 10
    total_deg = ending_deg - starting_deg

    for i in range(int(total_deg/step)):
        filter = df['phase_data'] > float(starting_deg)
        filter_2 = df['phase_data'] < float(starting_deg + step)
        df_small = df.where(filter)
        df_smaller = df_small.where(filter_2)
        phase_count = int(df_smaller['phase_data'].count())
        density.append(phase_count)
        starting_deg += 10
        print('Starting Deg : {}'.format(starting_deg))

    ### FIX IN THE 30MAR2022 IMPLEMENTATION ###
    ### WARNING - This is cheating to get it done, so DO NOT change bin size or this will fail!!! ###
    density_chop_1 = density[18:]
    density_chop_2 = density[:17]
    density = density_chop_1 + density_chop_2

    ### Create a final DF for plotting ###
    df = pd.DataFrame(density)
    df.columns = ['Value']
    print(df.head(3)) # Show 3 first rows

    plt.figure(figsize=(20,10)) # set figure size
    ax = plt.subplot(111, polar=True)
    # plt.axis('off') # This removes the grid lines

    ### Set some Rose Plot parameters ###
    upper = 100 # Max % for bar height
    lower = 0 # Min % for bar height
    max = df['Value'].max()
    slope = (max-lower)/max
    heights = slope * df.Value + lower
    width = 2*np.pi / len(df.index)
    indexes = list(range(1, len(df.index)+1))
    angles = [element * width for element in indexes]
    angles

    bars = ax.bar(
        x=angles, 
        height=heights, 
        width=width, 
        bottom=lower,
        linewidth=2, 
        edgecolor="white",
        color='#EF3D59')
    plot_save_path = os.path.join(drive, location, rat, day,"{}_{}_{}_sham_events_GT_offline".format(rat, day, condition)) # Plot save location
    plt.savefig(plot_save_path) # Save plot before showing
    plt.show()
    print('Rose Plots Created')

def calc_error():
    '''
    Process of saving/reloading .csv is redundant
    My justification (for this and calc_stats functions):
        - Loading small DF from .csv is fast
        - A seperate phase and error file is good logging
        - It's nice to be able to run calculate_error() quickly
            - Loading phase data from previous function is time-consuming
    '''
    ## Load Data ##
    df_save_path = os.path.join(drive, location, rat, day) # Load/Save path for error csv files

    ## Exporting Error Data (Degrees) ##
    df = pd.read_csv('{}\\{}_{}_{}_phase-event_data.csv'.format(df_save_path, rat, day, condition)) # Load CSV
    df['error_data'] = df['phase_data'] + 180
    df.to_csv('{}\\{}_{}_{}_error_data_degrees.csv'.format(df_save_path,rat, day, condition)) # Save data in degrees

    ## Exporting Error Data (Radians) ##
    df['error_data_radians'] = df['error_data'] * 0.0174533
    df = df['error_data_radians']
    df.to_csv('{}\\{}_{}_{}_error_data_radians.csv'.format(df_save_path,rat, day, condition)) # Save data in radians
    print('Error Files Created')

def calc_stats():
    df_save_path = os.path.join(drive, location, rat, day)
    df = pd.read_csv('{}\\{}_{}_{}_error_data_radians.csv'.format(df_save_path, rat, day, condition)) # Load CSV
    circmean_result = circmean(df['error_data_radians']) / 3.14159 * 180 # Converts to degrees
    circvar_result = circvar(df['error_data_radians'])
    print("Circular Mean : {}".format(circmean_result))
    print("Circular Variance : {}".format(circvar_result))
    print('Stats Calculated')

load_matlab_files()
create_rose_plot()
calc_error() # Convert phase data into error data (sep. log files for degrees and radians)
calc_stats() # This will fail until you run the circ_plot matlab functions on the data
# note: In matalb you will need to add 180 to all degrees and then convert to radians before running through circ_plot
