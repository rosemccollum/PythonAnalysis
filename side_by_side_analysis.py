# Goal of script is to turn initial pandas DataFrames for pre and post stimulation coherence into a 3x1 plot with pre/post/delta conherence
# To simplify, I imported these as .csv files, but in the actual code we will be using load/save mat method of scipy

import scipy.io as scio
import seaborn as sns
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load new csvs into Pandas DataFrame
df = pd.read_csv('RAW_PRE_dev2107_day1_TFR_coh.csv',index_col=False)
df_2 = pd.read_csv('RAW_POST_dev2107_day1_TFR_coh.csv',index_col=False)

# Transpose DataFrame
df = df.T
df_2 = df_2.T


# Remove index and save to new DataFrame
df.columns = df.iloc[0]
df_new = df[1:]

df_2.columns = df.iloc[0]
df_2_new = df_2[1:]

# Add deliniator to end of Data Frame - to deliniate if this datapoint is before or after stimulation
df_new['period'] = 'pre'
df_2_new['period'] = 'post'

# Pandas Concatination - Combine both Data Frames
df_3 = pd.concat([df_new,df_2_new])

#Rename the channels into something easier to digest for now
df_3.rename({'IL1-IL2 - BLA5-BLA6': 'CH1', 'IL1-IL2 - BLA7-BLA8': 'CH2','IL3-IL4 - BLA5-BLA6':'CH3','IL3-IL4 - BLA7-BLA8':'CH4','IL5-IL6 - BLA5-BLA6':'CH5','IL5-IL6 - BLA7-BLA8':'CH6','IL7-IL8 - BLA5-BLA6':'CH7','IL7-IL8 - BLA7-BLA8':'CH8'}, axis=1, inplace=True)
df_3['Freq'] = df_3.index # The Frequency (at least in my code) was getting saved to the index, this will create a new column

ch_num = 1 # Number of channels - 8 by default. This defines number of while loops
loop_num = ch_num +1 # This is to make sure we can put in the channel number literally and still get the loop to run the correct number of times
m = 1

# Seaborn will not let us use date in the "wide" format, and we will need to break it out into a "long" format
# While loop needs to be run x number of times, and then the append the final df for analysis
# After all 8 have been melted then we'll have to find a way to add delta data to the df as well, probably a "delta" in the "period" column
# It might end up being easier getting deltas before the while loop, but cross that bridge when we get there

while m < loop_num:
    channel = 'CH'+str(m)
    # print(channel)
    # value = channel+'value'
    df_loop = df_3[['freq',channel,'period']]
    df_loop['channel']=channel
    df_loop.rename({channel: 'coh'},axis=1, inplace=True)
    # rename the CH1/etc channel to 'coh' - this way they can all be appended together in the future
    print(df_loop.head())
    m +=1
    # print('Channel is: '+channel)
