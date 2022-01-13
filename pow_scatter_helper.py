# This program will determine # days to analyze and pull all post and pre files, then call the plotter program to graph all of them 
import os
from tkinter import Tk   
from tkinter import filedialog

# Determine num folders in directory
Tk().withdraw() 
folder = filedialog.askdirectory()
num_folders = len(next(os.walk(folder))[1])
subfolders = os.listdir(folder)

# Pulls out folders with 'day' and counts them 
folders_ls = []
for i in subfolders:
    if 'day' in i:
        folders_ls.append(i)

num_days = len(folders_ls)

# Pulls out pre and post files
rows, cols = (num_days, 2)
arr = [[0]*cols]*rows
files_ls = []
for i in range(len(folders_ls)):
    day_folder = os.path.join(folder, folders_ls[i])
    pow_files = []
    for (root, dirs, files) in os.walk(day_folder):
        print(files)
        file_names = files
    for j in file_names:
        if 'TFR' in j and ('PRE' in j or 'POST' in j) and 'xls' not in j:
            pow_files.append(j)
    files_ls.append(pow_files)

# Creats 2D array of post and pre files 
for i in range(len(files_ls)):
    arr[i] = files_ls[i]

# Pass to prepwr...scatter

