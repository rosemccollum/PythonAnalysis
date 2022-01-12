% function logfile_folder = create_ds_data()
close all
clear all
% This function does the *.binary to *.mat conversion of Open Ephys

% Key Assumptions for this script:
% 1. Assumes an a prior understanding of Recording Nodes (& their names) 
%    within the OEP signal chain used for recording. (111 for raw data and
%    112 for event/phase data) ***** WE WILL BE NEEDING EVENT/PHASE DATA

% 2. Assumes data to be analyzed is located at "\experiment1\recording1\"
% Outputs:
% 1. creates *.mat files next to log_file.mat for each corresponding
% recording
% 2. returns the folder that the logfile was from
%
% Created on 12Jan2022 by J. Whear, adapted from 'create_ds_data.m' by M. Schatza
% Last updated: 12Jan2022

% Before for loop get log file and creates a folder list
[file, logfile_folder] = uigetfile;
% get data from log file
log_data = load([logfile_folder, '\log_file.mat']);
% get all folders next to log file
folder_list = ls(logfile_folder);
% loop through all paths in log data path file
% I loop is what you are indeterested in
for i = 1:size(log_data.paths)
    % get cur path
   cur_path = strtrim(log_data.paths(i,:)); % paths save with whitespace, strtrim makes words looks nice
   cur_data = struct();
   % find corresponding folder in path
   % goes though folders
   for j = 1:size(folder_list)
       if ~isempty(strfind(folder_list(j,:), cur_path))
          % this is my folder 
           cur_data.path = [logfile_folder, strtrim(folder_list(j,:))];
           cur_data.label = cur_path;
           % load cont and events
           cont_data_111 = load_open_ephys_binary([cur_data.path, '/Record Node 111/experiment1/recording1/structure.oebin'], 'continuous', 1);
           event_data = load_open_ephys_binary([cur_data.path, '/Record Node 112/experiment1/recording1/structure.oebin'], 'events', 1);
                % downsample data and ts
           cur_data.sample_rate = 1; % ds to 1 kHz
           cur_data.ds_factor = cont_data_111.Header.sample_rate / cur_data.sample_rate; 
           tempdata = downsample(cont_data_111.Data', cur_data.ds_factor)';
           tempdata = tempdata * cont_data_111.Header.channels(1).bit_volts; % convert to volts

           temp_seconds = double(cont_data_111.Timestamps) * (1.0/double(cont_data_111.Header.sample_rate)); % translate from timestamps to time (seconds)
           cur_data.seconds = downsample(temp_seconds, cur_data.ds_factor); % cut down to ds_data size
           
           % trim data line to match timeline
           % rows 1-16, size matches timeline
           % will need to specify which channel is interesting
      
           cur_data.ds_data = tempdata(1:35,1:size(cur_data.seconds,1)); % Want 16 + 3 AUX Channels 
           cur_data.labels = {'IL1'; 'IL2'; 'IL3'; 'IL4'; 'IL5'; 'IL6'; 'IL7'; 'IL8'; ...
               'BLA1'; 'BLA2'; 'BLA3'; 'BLA4'; 'BLA5'; 'BLA6'; 'BLA7'; 'BLA8';'a'; 'b'; 'c'; 'd'; 'e'; 'f'; 'g'; 'h'; ...
               'i'; 'j'; 'k'; 'l'; 'm'; 'n'; 'o'; 'p';'AUX1';'AUX2';'AUX3'}; % make chan labels
           cur_data.log_data = log_data;
           cur_data.event_data = event_data;
           cur_data.header = cont_data_111.Header;
           % write new mat file with only relevant info
           if ispc
                folder_split = split(logfile_folder, '\');
            else
                folder_split = split(logfile_folder, '/');
           end
           save([logfile_folder, cur_data.label, '_', char(folder_split(end-2)), '_', char(folder_split(end-1)), '_cleandata_struct.mat'], 'cur_data');
       end
   end
end 
