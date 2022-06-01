''' Calculates ground truth phase'''
### Import Dependencies ###
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
from tkinter.filedialog import askopenfilename
import scipy.io as scio

''' Calculates GTP and returns single column dataframe of values '''
def groundTruth(file):
    print("calculating ground truth phase...")
    ## file = r"C:\Users\TNEL_Device_8\Documents\raePython\RatData\dev2111\RAW_PRE_dev2111_day1_cleandata_struct.mat"
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
    phase_data = phase_data*180/3.14159
    
    # Shorten phase to every second
    phases = []
    p = 0 
    for p in range(0, len(phase_data)+1, 60):
        phases.append(phase_data[p])

    # Make dataframe
    df = pd.DataFrame(phases)
    df.columns = ['phase_data']
    return df

