''' Calculates ground truth phase'''
### Import Dependencies ###
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from cv2 import phase
from scipy.signal import hilbert, filtfilt, butter
from scipy.stats import circmean, circvar
import scipy.io as scipy
import numpy as np
from numpy import angle
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from tkinter import Tk
import scipy.io as scio

''' Calculates GTP and returns single column dataframe of values if file given, otherwise graph data '''
def groundTruth(filename = None):
    print("calculating ground truth phase...")
   
    # Load matlab files
    if filename is None:
        Tk().withdraw() 
        file = askopenfilename()
        print("File: ", file)
    else :
        file = filename
    ### Files for debugging
    ## file = r"C:\Users\TNEL_Device_8\Documents\raePython\RatData\dev2111\RAW_PRE_dev2111_day1_cleandata_struct.mat" #lab rig
    ### file = r"C:/Users/angel/Documents/TNELab/Programming/RatData/dev2111/day1/RAW_PRE_dev2111_day1_cleandata_struct.mat" #laptop
    mat = scio.loadmat(file)

    # Grab necessary data
    mat_phase = mat["cur_data"]["phase_data"]
    mat_time = mat["cur_data"]["seconds"]

    ### Set some params ###
    fs = 30000 # sampling rate (default: 30000)
    lowpass = 4.0 # Hz
    low = lowpass / (fs/2)
    highpass = 12.0 # Hz
    high = highpass / (fs/2)
    order = 2
    data = mat_phase[0][0][0]

    ### Filter / Get Phase ###
    [b, a] = butter(order, [low, high], btype = 'band') # Butterworth digital and analog filter
    filtered_data = filtfilt(b, a, data)
    analytic_data = hilbert(filtered_data)
    phase_data = angle(analytic_data)
    phase_data = phase_data*180/3.14159 ## Converting to degrees
    
    # Shorten phase to every second
    phases = []
    p = 0 
    for p in range(0, len(phase_data),1000):
        phases.append(phase_data[p])

    # Write and add time values 
    t = 0
    time = []
    for t in range(0, len(mat_time[0][0]),1000):
        time.append(mat_time[0][0][t][0])

    # Split file name to get rat and day data
    temp = file.split("/")
    fileName = temp[-1]
    fileName = fileName.split("_")
    for word in fileName:
        if "dev" in word:
            rat = word
        elif "day" in word:
            day = word
        elif ('POST' in word) or ("PRE" in word) or ("CLOSED" in word):
            condition = word
    if condition == "CLOSED":
        dir = file.split("CLOSED")
    else:
        dir = file.split("RAW")    
    
    # Make dataframe
    df = pd.DataFrame(phases)
    df.columns = ['phase_data']
    avg = df['phase_data'].mean()

    if filename is not None:
        print("done calculating ground truth")
        return df
    else:
        df["time"] = time 
        print("graphing")
        sns.set(font_scale = 1.5)
        fig = plt.figure(figsize = (13,9))
        plot = sns.lineplot(data = df, x = 'time', y ='phase_data')
        #plt.savefig(dir[0] + rat + '_' + day + "_" + condition + "_GroundTruthPhase_over_time")
        plt.text(20, -170, "Mean phase:" +str(avg), horizontalalignment='left', size='medium', color='black', weight='semibold')
        plt.show()
        print("done")
    