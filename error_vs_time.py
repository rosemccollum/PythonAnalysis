''' Calculate and graph error of TORTE and ASIC models '''
import imp
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import numpy as np
import pandas as pd
import scipy.io as scio
import seaborn as sns
import matplotlib.pyplot as plt
import math
from TORTE_vs_time import getTORTE
from ground_truth import groundTruth

print("starting...")
# Load matlab files
Tk().withdraw() 
file = askopenfilename()
print("File: ", file)
gtp = groundTruth(file)
torte = getTORTE()

