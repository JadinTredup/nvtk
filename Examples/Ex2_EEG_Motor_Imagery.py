import argparse
import os
import timeit

import pygame

from NVTK.Experiments.EEGDataCollection import eegMotorImageryHandsFeet

# from NVTK.Sensors import EEG

IMAGE_DIR = "Images"
PLACEHOLDER_FN = "RandomGnome.png"
IMG = os.path.join(IMAGE_DIR, PLACEHOLDER_FN)

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

    parser = argparse.ArgumentParser(description="NVTK - ERP Experiment")
    parser.add_argument('--trials', default=50, type=int,
                        help="Number of times to repeat stimulus presentation.")
    parser.add_argument('--sd', default=False,
                        help="Sets recording to SD card on-board.")

    args = parser.parse_args()
    num_trials = args.trials
    record_sd = args.sd
    time_per_trial = 5  # Seconds
    total_time = num_trials * time_per_trial

    experiment = eegMotorImageryHandsFeet()
    experiment.Run()
