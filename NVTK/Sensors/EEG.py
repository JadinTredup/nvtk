import serial
from openbci import cyton as bci

class EEGMonitor(object):
    """
    This is a high-level wrapper for the OpenBCI Cyton
    object. This is meant to shorten many of the initialization
    steps that are all repeatable for these experiments
    """

    # Initialization functions
    def __init__(self, port_name=STD_PORT, daisy_board=True):

        self.board = bci.OpenBCICyton(port=port_name,
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


    #def logData(self, sample):

    def startEEGStreaming(self):
        self.streaming = True
        self.board.start_streaming(self.logData)

    def stopEEGStreaming(self):
        self.streaming = False
        self.board.stop()