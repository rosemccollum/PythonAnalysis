close all 
clear all

tic

data_channel=1; % INPUT DATA CHANNEL HERE **
closedloopPath_1 = ['Z:\projmon\virginia-dev\01_EPHYSDATA\dev2111\day3\CLOSED_LOOP_2021-12-02_14-03-21\Record Node 111\experiment1\recording1\structure.oebin'];
closedloopPath_2 = 'Z:\projmon\virginia-dev\01_EPHYSDATA\dev2111\day3\CLOSED_LOOP_2021-12-02_14-03-21\Record Node 112\experiment1\recording1\structure.oebin';

%% Determine Bipolar Channel References
if data_channel==8
    data_channel1=1;
else
    data_channel1=data_channel+1;
end

%% Get binary data (LFP on 1st Node)
% Convert both continuous LFP  *.mat
RawData = load_open_ephys_binary(closedloopPath_1, 'continuous',1,'mmap');
%lfpdata = double(RawData.Data.Data.mapped(data_channel,:)-RawData.Data.Data.mapped(data_channel1,:));
lfpdata = double(RawData.Data.Data.mapped(data_channel,:));
%lfpdata = double(RawData.Data.Data.mapped(7,:));
lfptime=RawData.Timestamps;


%% Get binary data (Phase on 2nd Node)
RawData_ev3=load_open_ephys_binary(closedloopPath_2, 'events',3);
% RawData_Phase=load_open_ephys_binary(closedloopPath_2,'continuous',1,'mmap');
% phasedata = double(RawData_Phase.Data.Data.mapped(1,:))*RawData_Phase.Header.channels(1).bit_volts;
% phasetime=RawData_Phase.Timestamps;



%% Compute Gnd Truth phase
% bandpass filter
band = [4 8]; % 4 to 8hz bandpass
Fs = 30000;
[b, a] = butter(2, band/(Fs/2)); % 2nd order butterworth filter
data_filt = nan(size(lfpdata,1),size(lfpdata,2));
data_complex = data_filt; %#ok<NASGU>
phase = data_filt; %#ok<NASGU>
% calculate phases
   
        data_filt = filtfilt(b, a, lfpdata); % bandpassed data
        data_complex = hilbert(data_filt); % perform a hilbert transform on the data to get the complex component.
        phase = angle(data_complex); % phase in radians! Use rad2deg() if you prefer things in degrees.
        
        %% Marks changes %%
        % have to convert event timestamps into continuous data index
         event_ts = RawData_ev3.Timestamps(RawData_ev3.Data==3);
         [dat, data_inds] = ismember(event_ts, RawData.Timestamps);
         data2plot = phase(data_inds);
         %%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      

% figure()
% plot(phasetime,phasedata);
% hold on; 
% plot(lfptime,rad2deg(phase));
% plot(event_ts,ones(length(event_ts))*180,'x');
% ylim([-190 190])
% legend('Calculated Phase', 'Ground Truth Phase', 'Sham Events')

mean=rad2deg(circ_mean(data2plot));
if mean<0
    mean=mean+360; % Makes sure the mean is reported as a positive value
end


%% Make Rose Plot
figure()
ph = polarhistogram(data2plot,24,'BinWidth',pi/12,'FaceColor','none','EdgeColor','#0072BD');
%set(gca, 'FontName', 'Arial', 'FontSize', 34, 'FontWeight', 'bold')
%ax = polaraxes;
%ax.FontSize = 10;
set(gca,'FontSize',15)
ax = gca;
ax.RAxis.FontSize=10;
hold on
polarplot([circ_mean(data2plot');circ_mean(data2plot')], [0;max(ph.Values)],'Color','r','LineWidth',3)   
title('TORTE Error')

%% Display Mean and Standard Deviation
mean=mean
sdev=rad2deg(circ_std(data2plot))

toc
