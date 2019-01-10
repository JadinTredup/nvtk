import pygame
import os
import sys
import serial
import time, timeit

from threading import Thread
from openbci import cyton as bci
from openbci.plugins import StreamerTCPServer

from yapsy.PluginManager import PluginManager

# Load the plugins from the plugin directory.
manager = PluginManager()

#################################################################
#                                                               #
#                                                               #
#               Open BCI Global Variables                       #
#                                                               #
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
last_values = [0]*NB_CHANNELS

# Counter to trigger duplications...
leftover_duplications = 0

tick = timeit.default_timer()

class EEGMonitor(object):
    """
    This is a high-level wrapper for the OpenBCI Cyton
    object. This is meant to shorten many of the initialization
    steps that are all repeatable for these experiments
    """

    # Initialization functions
    def __init__(self, port_name=None, daisy_board=True):

        self.board = bci.OpenBCICyton(port='/dev/ttyUSB1',
                                      baud=BAUD_RATE,
                                      daisy=daisy_board,
                                      filter_data=False,
                                      scaled_output=True,
                                      log=None)
        self.streaming = False
        self.recording = False
        self.startMonitor()

    def startMonitor(self):
        """
        This function sends a command to the bci board
        to reset the system and prepare it for new commands.
        Command: s (append letters from OpenBCI SDK)
            s - stop board streaming
            v - soft reset of the 32-bit board
        """
        s = 'svCd'
        for c in s:
            if sys.hexversion > 0x03000000:
                self.board.ser_write(bytes(c, 'utf-8'))
            else:
                self.board.ser_write(bytes(c))


    def logData(self, sample):
        print("----------------")
        print("%f"%(sample.id))
        print(sample.channel_data)
        print(sample.aux_data)
        print("----------------")

    def startEEGStreaming(self):
        self.streaming = True
        self.board.start_streaming(self.logData)




if __name__ == "__main__":
    eeg = EEGMonitor()
    print("Here")
    eeg.startEEGStreaming()