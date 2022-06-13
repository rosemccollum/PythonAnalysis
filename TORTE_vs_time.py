from fileinput import filename
from cv2 import phase
import matlab.engine 
import h5py
import hdf5storage
import math
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import numpy as np
from numpy import array
import pandas as pd
import scipy.io as scio
import seaborn as sns
import matplotlib.pyplot as plt

def getTORTE(filename = None):
    print("torte starting...")
    # Load matlab files
    if filename is None:
        Tk().withdraw() 
        file = askopenfilename()
        print("TORTE File: ", file)
    else :
        file = filename
    ### File for debugging
    ### file = r"C:/Users/angel/Documents/TNELab/Programming/RatData/dev2111/day1/RAW_PRE_dev2111_day1_cleandata_struct.mat"
    mat = scio.loadmat(file)

    # Grab necessary data
    mat_phase = mat["cur_data"]["phase_data"]
    mat_time = mat["cur_data"]["seconds"]

    # Make array into list 
    phase_list = []
    for i in range(len(mat_phase[0][0][0])) :
        phase_list.append(mat_phase[0][0][0][i])

    # Convert to array to correct type, then back to list 
    phases = np.array(phase_list)
    phases = phases.astype('int32')
    phase_list = phases.tolist()

    # Call function
    print("calling matlab script...")
    eng = matlab.engine.start_matlab()
    buff = matlab.double([[200]]) 
    mat_phase = matlab.double([phase_list])
    ht_b = matlab.double([[500]])
    band = matlab.double([[4,8]])
    Fs = matlab.double([[1000]])
    upsamp = matlab.double([[True]])
    torte = eng.hilbert_transformer_phase(mat_phase, buff, ht_b, band, Fs, upsamp, nargout = 3)
    eng.quit()

    ## Torte output len is phase_list len / 59.99

    # Convert to degrees and shorten measurements to every second
    temp_phases = array(torte[0])
    d = 0
    phases = []
    for d in range(0, len(temp_phases), 1000):
        temp = float(temp_phases[d])
        phases.append(math.degrees(temp))

    # Put data in dataframe
    df = pd.DataFrame(phases)
    df.rename(columns= {0:'phase'}, inplace=True)

    # Find mean of phase
    avg = df['phase'].mean()
    #avg = sum/len(temp_phases)

    # Write and add time values 
    t = 0
    pt = 0
    time = []
    for t in range(0, len(mat_time[0][0]), 1000):
        time.append(pt)
        pt += 1
    df["time"] = time 
    
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

    # Determing step for time labels
    if (len(mat_time[0][0]) > 300000):
        step = 60
    else:
        step = 1; 
    
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
        plot.set_title('TORTE Phase over time ' + condition +  " " + rat + " " + day)
        plot.set_xlabel('Time (s)')
        plot.set_ylabel('Phase')
        plot.set_ylim(-180,180)
        plt.text(1, -170, "Mean value:" + str(avg), horizontalalignment='left', size='medium', color='black', weight='semibold')
        plt.savefig(dir[0] + rat + '_' + day + "_" + condition + "_TORTEphase_over_time")
        plt.show()
    print("done")

getTORTE()