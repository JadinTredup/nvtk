def CreateInfo(default=True, n_channels=None, eeg_sfreq=None, gsr_sfreq=None, ch_names=None, ch_types=None):

    if default==True:
        info = {
            'n_channels' = '20',
            'eeg_sfreq' = '250',
            'gsr_sfreq' = '125',
            'ch_names' = ['EEG01', 'EEG02', 'EEG03', 'EEG04', 'EEG05', 'EEG06',
                          'EEG07', 'EEG08', 'EEG09', 'EEG10', 'EEG11', 'EEG12',
                          'EEG13', 'EEG14', 'EEG15', 'EEG16', 'ACC01', 'ACC02',
                          'ACC03', 'GSR'],
            'ch_types' = ['eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg',
                          'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg',
                          'eeg', 'eeg', 'eeg', 'eeg', 'accel', 'accel',
                          'accel', 'gsr']
        }
    else:
        info = {
            'n_channels' = '20',
            'eeg_sfreq' = '250',
            'gsr_sfreq' = '125',
            'ch_names' = ['EEG01', 'EEG02', 'EEG03', 'EEG04', 'EEG05', 'EEG06',
                          'EEG07', 'EEG08', 'EEG09', 'EEG10', 'EEG11', 'EEG12',
                          'EEG13', 'EEG14', 'EEG15', 'EEG16', 'ACC01', 'ACC02',
                          'ACC03', 'GSR'],
            'ch_types' = ['eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg',
                          'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg',
                          'eeg', 'eeg', 'eeg', 'eeg', 'accel', 'accel',
                          'accel', 'gsr']
        }

    return info