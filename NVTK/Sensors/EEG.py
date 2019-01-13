from openbci import cyton as bci
from NVTK.utils.EEGUtils import parse_eeg_data


class EEGMonitor(object):
    """
    This is a high-level wrapper for the OpenBCI Cyton
    object. This is meant to shorten many of the initialization
    steps that are all repeatable for these experiments
    """

    # Initialization functions
    def __init__(self, port_name=STD_PORT, daisy_board=True, save_fn=None):

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

    def printData(self, sample):
        while self.streaming:
            print("----------------")
            print("%f"%(sample.id))
            print(sample.channel_data.type)
            print(sample.aux_data)
            print("----------------")

    def saveData(self, sample):
        while self.streaming:
            data_string = parse_eeg_data(sample.id, sample.channel_data, sample.aux_data)
            self.save_file.write(data_string)

    def startEEGStreaming(self, save_fn=None):
        self.streaming = True
        if save_fn is not None:
            self.save_file = open(save_fn, 'w')
            self.board.start_streaming(self.saveData)
        else:
            self.board.start_streaming(self.logData)

    def stopEEGStreaming(self):
        self.streaming = False
        self.board.stop()
        self.save_file.close()
