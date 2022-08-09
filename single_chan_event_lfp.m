function [seconds_ts] = single_chan_event_lfp()
% Loads and returns lfp data around sham events
% grabs 0.5 sec before and after each event
%data_channel = 3; 
path = 'Z:\projmon\virginia-dev\01_EPHYSDATA\dev2111\day1\CLOSED_LOOP_2021-11-01_16-09-48\Record Node 112\experiment1\recording1\structure.oebin';
RawData = load_open_ephys_binary(path, 'events',3);
seconds_ts = double(RawData.Timestamps) * (1.0/double(RawData.Header.sample_rate));


