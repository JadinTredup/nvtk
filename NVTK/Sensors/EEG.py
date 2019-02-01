import sys
import timeit
import time
from openbci import cyton as bci
from NVTK.utils.EEGUtils import parse_eeg_data

STD_PORT = '/dev/ttyUSB0'
BAUD_RATE = 115200

class EEGMonitor(object):
    """
    This is a high-level wrapper for the OpenBCI Cyton
    object. This is meant to shorten many of the initialization
    steps that are all repeatable for these experiments
    """

    # Initialization functions
    def __init__(self, port_name=STD_PORT, daisy_board=True, save_fn=None, channel_num=16):

        self.board = bci.OpenBCICyton(port=STD_PORT,
                                      baud=BAUD_RATE,
                                      daisy=daisy_board,
                                      filter_data=False,
                                      scaled_output=True,
                                      log=None,
                                      timeout=None)
        self.channel_num = 16
        self.sample_rate = 256
        self.streaming = False
        self.recording = False
        self.data = []
        self.StartMonitor()
        print("Monitor Started")
        if save_fn is None:
            save_fn = 'EEG-Temp.txt'

        self.InitSaveFile(save_fn)
        print("Save File Initialized")


    def StartMonitor(self):
        """
        This function sends a command to the bci board
        to reset the system and prepare it for new commands.
        Command: s (append letters from OpenBCI SDK)
            s - stop board streaming
            v - soft reset of the 32-bit board
        """
        s = 'svCd'
        for c in s:
            print(c)
            if sys.hexversion > 0x03000000:
                self.board.ser_write(bytes(c, 'utf-8'))
            else:
                self.board.ser_write(bytes(c))


    def InitSaveFile(self, fn):
        self.f = open(fn, 'w+')


    def printData(self, sample):
        while self.streaming:
            print("----------------")
            print("%f"%(sample.id))
            print(sample.channel_data)
            print(sample.aux_data)
            print("----------------")


    def saveData(self, sample):
        start = timeit.default_timer()
        while self.streaming:
            step = timeit.default_timer()
            timestamp = step - start
            data_str = parse_eeg_data(sample.id, sample.channel_data, sample.aux_data, timestamp)
            self.f.write(data_str)

        self.f.close()


    def startEEGStreaming(self, save=False):
        self.streaming = True
        if save==True:
            self.board.start_streaming(self.saveData)
        else:
            self.board.start_streaming(self.printData)


    def stopEEGStreaming(self):
        self.streaming = False
        self.board.stop()