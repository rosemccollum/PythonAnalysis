''' Calculates ground truth phase'''
### Import Dependencies ###
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from scipy.signal import hilbert, filtfilt, butter
from scipy.stats import circmean
from numpy import angle
import math
import matlab.engine 
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from tkinter import Tk
import scipy.io as scio

''' Calculates GTP and returns single column dataframe of values if file given, otherwise graph data '''
def groundTruth(filename = None):
    print("calculating ground truth phase...")
   
    # Load matlab files
    # if filename is None:
    #     Tk().withdraw() 
    #     file = askopenfilename()
    #     print("File: ", file)
    # else :
    #     file = filename
    # ### Files for debugging
    # ## file = r"C:\Users\TNEL_Device_8\Documents\raePython\RatData\dev2111\RAW_PRE_dev2111_day1_cleandata_struct.mat" #lab rig
    # ### file = r"C:/Users/angel/Documents/TNELab/Programming/RatData/dev2111/day1/RAW_PRE_dev2111_day1_cleandata_struct.mat" #laptop
    # mat = scio.loadmat(file)

    # # Grab necessary data
    # mat_phase = mat["cur_data"]["phase_data"]
    # mat_time = mat["cur_data"]["seconds"]

    ## pull in lfp data, then event timestaps, go to these indexes and take 0.5 sec before after

    print("choose log file:")
    Tk().withdraw()
    file = askopenfilename()
    log_mat = scio.loadmat(file)
    print("File chosen: ", file)
    mat_channel = log_mat["watchChannel"]
    chosen_chan = int(mat_channel[0][0])
    split_file = file.split("log")

    # Split file name to get rat and day data
    dir = log_mat["record_dir"]
    dir = dir.tolist()
    dir = dir[0].split("\\")  
    rat = dir[-2]
    day = dir[-1]

    # Pull lfp data for selected channel
    print("grabbing raw lfp data for channel....")
    eng = matlab.engine.start_matlab()
    chan = matlab.double([chosen_chan])
    chan_phase = eng.single_chan_lfp(chan, nargout = 2)

    ## chan_phase[0] = lfp data
    ## chan_phase [1] = seconds
    chans = np.asarray(chan_phase[0])
    chans = chans[0].tolist()
    
    # Downsample data, might do in matlab but doesn't seem to take crazy long to import
    c = 0
    chan_list = []
    for c in range(0, len(chans), 2000):
        chan_list.append(chans[c])

    ### Set some params ###
    fs = 30000 # sampling rate (default: 30000)
    lowpass = 4.0 # Hz
    low = lowpass / (fs/2)
    highpass = 12.0 # Hz
    high = highpass / (fs/2)
    order = 2
    data = chan_list

    ### Filter / Get Phase ###
    [b, a] = butter(order, [low, high], btype = 'band') # Butterworth digital and analog filter
    filtered_data = filtfilt(b, a, data)
    analytic_data = hilbert(filtered_data)
    phase_data = angle(analytic_data)

    # Calculate mean angle
    rad_avg = circmean(phase_data)
    avg = math.degrees(rad_avg)
  
    phase_data = phase_data*180/3.14159 ## Converting to degrees
    
    # Shorten phase to every second
    phases = []
    p = 0 
    for p in range(0, len(phase_data),1000):
        phases.append(phase_data[p])

    # # Write and add time values 
    # t = 0
    # pt = 0
    # time = []
    # for t in range(0, len(mat_time[0][0]), 1000):
    #     time.append(pt)
    #     pt += 1
    
    # Make dataframe
    df = pd.DataFrame(phases)
    df.columns = ['phase_data']

    if filename is not None:
        print("done calculating ground truth")
        return df
    else:
        #df["time"] = time 
        print("graphing")
        sns.set(font_scale = 1.5)
        fig = plt.figure(figsize = (13,9))
        plot = sns.lineplot(data = df, x = 'time', y ='phase_data')
        plot.set_title('Ground Truth Phase ' +  " " + rat + " " + day)
        plot.set_xlabel('Time (s)')
        plot.set_ylabel('Phase')
        plt.text(20, -170, "Mean phase:" +str(avg), horizontalalignment='left', size='medium', color='black', weight='semibold')
        plt.savefig(split_file[0] + rat + '_' + day + "_" +  "_GroundTruthPhase_over_time")
        plt.show()
        print("done")
groundTruth()