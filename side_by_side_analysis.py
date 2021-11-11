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

# Add deliniator to end of Data Frame
df_new['period'] = 'pre'
df_2_new['period'] = 'post' bele

# Pandas Concatination
df_3 = pd.concat([df_new,df_2_new])

pd.set_option("display.max_rows", None)

#Rename the channels into something easier to digest for now
df_3.rename({'IL1-IL2 - BLA5-BLA6': 'CH1', 'IL1-IL2 - BLA7-BLA8': 'CH2','IL3-IL4 - BLA5-BLA6':'CH3','IL3-IL4 - BLA7-BLA8':'CH4','IL5-IL6 - BLA5-BLA6':'CH5','IL5-IL6 - BLA7-BLA8':'CH6','IL7-IL8 - BLA5-BLA6':'CH7','IL7-IL8 - BLA7-BLA8':'CH8'}, axis=1, inplace=True)

# Pull frequency data from the index and create new 'freq' column
df_3['freq'] = df_3.index

# Remove the frequency data from the index
df_3.reset_index(drop=True, inplace=True)
# Remove index name from df_3
# Drop first column of dataframe
df_3 = df_3[['freq','CH1','CH2','CH3','CH4','CH5','CH6','CH7','CH8','period']]
# print(df_3.head())

ch_num = 8 # Number of channels - 8 by default. This defines number of while loops
loop_num = ch_num +1 # This is to make sure we can put in the channel number literally and still get the loop to run the correct number of times
m = 1

# Build df_final before while loop
column_list = ['freq','coh','period','channel']
global df_final
df_final = pd.DataFrame(columns=column_list)   # print(channel)

# while loop to create final DataFrame (df_final)
while m < loop_num:
    channel = 'CH'+str(m)
    df_loop = df_3[['freq',channel,'period']]
    df_loop['channel']=channel
    df_loop.rename({channel: 'coh'},axis=1, inplace=True)
    m +=1
    df_final = df_final.append(df_loop)
    del df_loop

# df_final postprocessing
df_final = df_final.reset_index()
df_final = df_final[['freq','coh','channel','period']]

# Prepare and print Seaborn plot
plot = sns.relplot(data =df_final,x='freq',y='coh',kind='line',col='period',hue='channel')
plot.set_xlabels('freq')
plot.set_ylabels('coh')
plot.axes[0][0].set_xticks(range(10,61,10))
plot.axes[0][0].set_xticklabels([10, 20, 30, 40, 50, 60])
plt.axvline(8,0,0.9)
plt.axvline(4,0,0.9)
plt.show()
