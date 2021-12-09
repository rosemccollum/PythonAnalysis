# Python Analysis
#### Updated: 03Dec2021
Project Overview: We are developing a Python-based data analysis and visualization pathway for the TNE Lab.

Short-Term Objectives (End of 2021): An Python-based architecture that pulls raw data, automatically runs it through analysis pipeline, and creates/saves figures.

Long-Term Objectives (TBD): Debug and expand to fit growing needs of TNE Lab - How can we use this project to produce visuals that contextualize what we are trying to accomplish at a lab-wide level.

## Data Visualization
### simple_GUI.py
simple_GUI contains the graph_gui() function which is used in most of the data visualization scripts.

### side_by_side_analysis.py
Graphs coherence vs. frequency for pre-stim and post-stim, which a subuplot showing delta coherence vs. frequency.

### heatmap_coh.py
Creates a coherence heatmap for a range of frequencies for pre-stim and post-stim, which a subuplot showing delta coherence vs. frequency heatplot.

### 4x4_heatmap_coh.py
Creates a coherence heatmap for 4-12 Hz frequency band between BLA and IL channel combinations

### prepwr_vs_deltapwr_scatter.py
Creates a scatterplot graphing pre-stim power vs. delta power.

### coh_vs_freq_graphs.py
Graphs coherence vs. frequency. This has largely been replaced by side_by_side_analysis, and does not integrate with simple_gui.

## Matlab Interfacing
### matlab_struct_to_pd_df_importer.py
A general framework for accessing matlab .mat files in python using scipy and pandas.

## Animal Tracking
### open_cv_object_tracker.py
Tracks region of interest (ROI) and outputs information to a save file.

### open_cv_processing.py
Reads output of open_cv_object_tracker and creates a lineplot oh average movement vs. time
