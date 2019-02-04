import numpy as np
import os

class RawNVTK():

    def __init__(self, info, eeg_fn, gsr_fn):
        self.info = info
        self.eeg_data = np.genfromtxt(eeg_fn, delimiter=',')
        self.gsr_data = np.genfromtxt(gsr_fn, delimiter=',')


channels = {
    "ch1" : {
        "name" :
        "type" :
        "data" :
        "sfreq":
    }
}