import numpy as np
import matplotlib.pyplot as plt
import mne

from mne import io, read_proj, read_selection
from mne.datasets import sample

from mne.time_frequency import psd_multitaper

def PowerSpectralDensity(input, window_size=None, tmin, tmax):
    time = tmax-tmin
    if window_size is None:
        window_size = time

    num_epochs = int(round(time/window_size))
    epochs = []
    for i in range(nume_epochs):
        tmin_epoch = tmin + i*window_size
        tmax_epoch = tmin_epoch + window_size
        span = (tmin_epoch, tmax_epoch)
        epochs.append(span)