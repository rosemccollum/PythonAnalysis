# Python Analysis
#### Updated: 26Jan2022
Project Overview: Developing a Python-based data analysis/visualization pathway for the TNE Lab.

Long-Term Objectives (TBD): Debug and expand to fit growing needs of TNE Lab - How can we use this project to produce visuals that contextualize what we are trying to accomplish at a lab-wide level?

## Data Visualization
### simple_GUI.py
simple_GUI contains the graph_gui() function which is used in most of the data visualization scripts.

### side_by_side_analysis.py
Graphs coherence vs. frequency for pre-stim and post-stim, which a subuplot showing delta coherence vs. frequency.

### heatmap_coh.py
Creates a coherence heatmap for a range of frequencies for pre-stim and post-stim, which a subuplot showing delta coherence vs. frequency heatplot.

### 4x4_heatmap_coh.py
Creates a coherence heatmap for 4-12 Hz frequency band between BLA and IL channel combinations.

### prepwr_vs_deltapwr_scatter.py
Creates a scatterplot graphing pre-stim power vs. delta power.

### coh_vs_freq_graphs.py
Graphs coherence vs. frequency. This has largely been replaced by side_by_side_analysis, and does not integrate with simple_gui.

## Matlab Interfacing
### matlab_struct_to_pd_df_importer.py
A general framework for accessing matlab .mat files in python using scipy and pandas.

### create_plots.py
Variant of matlab_struct_to_pd_df_importer.py. Takes in a _log_file.mat_ file and returns a seaborn graph of acceleration over time.

## Animal Tracking
### open_cv_object_tracker.py
Tracks region of interest (ROI) and outputs information to a save file.

### open_cv_processing.py
Reads output of open_cv_object_tracker and creates a lineplot oh average movement vs. time

### dev_cam.py
A file with video recording and overlay functions written using OpenCV. This can be imported into simple_CL.py to record videos with timestamps and recording information


### convert_mp4_to_avi.py
Turns .mp4 MJPG codec videos recorded with windows camera app into an MJPG codec .avi file which Any-Maze will accept for later analysis. Slow, but works.
