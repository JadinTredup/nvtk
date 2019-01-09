import argparse
import os
import timeit

import pygame
from NVTK.Experiments.EEGDataCollection import eegBaseline

# from NVTK.Sensors import EEG

#################################################################
#                                                               #
#               Open BCI Global Variables                       #
#                                                               #
#################################################################
BAUD_RATE = 115200
NB_CHANNELS = 8
SAMPLING_FACTOR = -1.024
SAMPLING_RATE = 256
SERVER_PORT = 12345
SERVER_IP = "localhost"
DEBUG = False
STD_PORT = '/dev/ttyUSB0'

# Check packet drop
last_id = -1

# Counter for sampling rate
nb_samples_in = -1
nb_samples_out = -1

# last seen values for interpolation
last_values = [0] * NB_CHANNELS

# Counter to trigger duplications...
leftover_duplications = 0

tick = timeit.default_timer()

if __name__ == "__main__":
    experiment = eegBaseline()
    experiment.Run()