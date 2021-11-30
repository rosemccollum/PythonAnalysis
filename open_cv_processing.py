### Process raw location data from opencv recording - downsample, average mvmt, euclidian distance, and sns plotting
# Updated 24Nov2021
### 
from time import time
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import cv2 #Import openCV
import datetime
import scipy.io as scio
import scipy.spatial as sps

def ds_cord_log():
    df = pd.read_csv('tracking_data.csv')
    df = df.round(0)
    df_ds = df
    total_rec_time = df['run_time'].iloc[-1]
    print('Beginning downsampling of '+ str(total_rec_time) +' seconds of recording')

    x_avg = []
    y_avg = []
    w_avg = []
    h_avg = []
    run_time = []

    for i in range(int(total_rec_time)+1):
        df_temp = df.loc[df['run_time']==i]

        df_temp_2 = df_temp.mean(axis=0)
        x_avg.append(df_temp_2['x'])
        y_avg.append(df_temp_2['y'])
        w_avg.append(df_temp_2['w'])
        h_avg.append(df_temp_2['h'])
        run_time.append(df_temp_2['run_time'])

    df_final = pd.DataFrame({'x':x_avg, 'y':y_avg,'w':w_avg,'h':h_avg,'run_time':run_time})
    print(df_final)
    df_final.to_csv('ds_tracking_data.csv')

def dist_moved():
    df_dist_in = pd.read_csv('ds_tracking_data.csv')
    dist = []
    run_time = []

    for i in range(len(df_dist_in)-1):
        x1 = df_dist_in['x'].loc[i]
        y1 = df_dist_in['y'].loc[i]
        x2 = df_dist_in['x'].loc[i+1]
        y2 = df_dist_in['y'].loc[1+1]

        run_time_cur = df_dist_in['run_time'].loc[i+1]

        euclid = sps.distance.euclidean((x1,y1,0),(x2,y2,0))

        dist.append(euclid)
        run_time.append(run_time_cur)
        df_dist_out = pd.DataFrame({'dist':dist,'run_time':run_time})
        df_dist_out.to_csv('ds_tracking_data_dist.csv')


def visualize_dist():
    df_visualize = pd.read_csv('ds_tracking_data_dist.csv')
    sns.lineplot(data=df_visualize,x='run_time',y='dist')
    plt.show()

ds_cord_log()
dist_moved()
visualize_dist()
