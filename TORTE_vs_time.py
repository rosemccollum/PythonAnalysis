from fileinput import filename
from cv2 import phase
import matlab.engine 
import math
from scipy.stats import circmean
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import numpy as np
from numpy import array
import pandas as pd
import scipy.io as scio
import seaborn as sns
import matplotlib.pyplot as plt

def getTORTE(filename = None):
    print("Starting TORTE calculation...")
    # # Load matlab files
    # if filename is None:
    #     Tk().withdraw() 
    #     file = askopenfilename()
    #     print("TORTE File: ", file)
    # else :
    #     file = filename
    # ### File for debugging
    # ### file = r"C:/Users/angel/Documents/TNELab/Programming/RatData/dev2111/day1/RAW_PRE_dev2111_day1_cleandata_struct.mat"
    # mat = scio.loadmat(file)
        
    # Load log file to grab locked channel
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

    # Call torte function
    print("calculating TORTE in matlab...")
    eng = matlab.engine.start_matlab()
    mat_chan = matlab.double([chan_list])
    buff = matlab.double([[200]]) 
    torte = eng.hilbert_transformer_phase(mat_chan, buff,  nargout = 3) 
    eng.quit()

    # Calculate mean angle
    rad_avg = circmean(torte[0])
    avg = math.degrees(rad_avg)
    
    # Convert to correct data type and convert to degrees
    temp_phases = array(torte[0])
    d = 0
    phases = []
    for d in range(0, len(temp_phases)):
        temp = float(temp_phases[d])
        phases.append(temp)

    phases = np.degrees(phases) ## change to degrees
    
    # Put data in dataframe
    df = pd.DataFrame(phases)
    df.rename(columns= {0:'phase'}, inplace=True)

    # Write and add time values 
    t = 0
    pt = 0
    time = []
    for t in range(0, len(phases)):
        time.append(t)
   
    df["time"] = time 
    
    # End function if passed file name (don't need to graph)
    if filename is not None:
        print("done with TORTE calculations")
        return phases
    else:
        # Graph and save plot 
        print("graphing...")
        sns.set(font_scale = 1.5)
        fig = plt.figure(figsize = (13,9))
        plot = sns.lineplot(data = df, x = 'time', y = 'phase')
        plot.set_title('TORTE Phase over time ')
        plot.set_xlabel('Time (s)')
        plot.set_ylabel('Phase')
        plot.set_ylim(-180,180)
        plt.text(1, -170, "Mean value: " + str(avg), horizontalalignment='left', size='medium', color='black', weight='semibold')
        plt.savefig(split_file[0] + rat + '_' + day + "_"  + "_TORTEphase_over_time")
        plt.show()
    print("done")
getTORTE()