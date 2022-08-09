function [lfp,seconds_ts] = single_chan_lfp(chan, volts)
% Loads and returns lfp data for single channel
% chan = channel chosen
% choose path of data before running
if ~exist('volts','var')
    % no input for volts, so keep at microvolts
     volts = 0;
end
data_channel = chan; 
path = 'Z:\projmon\virginia-dev\01_EPHYSDATA\dev2111\day1\CLOSED_LOOP_2021-11-01_16-09-48\Record Node 111\experiment1\recording1\structure.oebin';
RawData = load_open_ephys_binary(path, 'continuous',1,'mmap');
lfpdata = double(RawData.Data.Data.mapped(data_channel,:));
seconds_ts = double(RawData.Timestamps) * (1.0/double(RawData.Header.sample_rate));
% downsample data and ts
%sample_rate = 1000; % ds to 1 kHz
%ds_factor = RawData.Header.sample_rate / sample_rate;
%tempdata = downsample(RawData.Data', ds_factor)';
%tempdata = tempdata * RawData.Header.channels(data_channel).bit_volts; % convert to volts
%lfp = tempdata / 1000000;           
           
%temp_seconds = double(cont_data_111.Timestamps) * (1.0/double(cont_data_111.Header.sample_rate)); % translate from timestamps to time (seconds)
%seconds = downsample(temp_seconds, lfpdata.ds_factor); % cut down to ds_data size

lfp = lfpdata * RawData.Header.channels(data_channel).bit_volts;
if volts == 1
    lfp = lfp / 1000000;
end



% check that max timestamp minus min timestamp is equilavent to 5 min 
% will give me seconds ^ 
% before convert to seconds, diff(timestamp) should be 1 
% convert to voltage 
% lfp * 0.195 
% microV units
% add time series
% convert timestamp from int 64 into a double and shorten to seconds

