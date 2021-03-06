import os
import multiprocessing as mp
import PySimpleGUI as sg
from NVTK.Sensors.EEG import EEGMonitor
from NVTK.Sensors.GalvanicSkinResponse import ArduinoGSR

class DataCollection():

    def __init__(self, eeg=True, gsr=True, eye_tracking=False, description=None, save_dir=None):

        if eeg == True:
            self.eeg = EEGMonitor()

        if gsr == True:
            self.gsr = ArduinoGSR()

        self.SetFileNames(save_dir)
        self.WriteInfo(description)


    def SetFileNames(self, save_dir):
        self.info_file = os.path.join(save_dir, 'info.txt')
        self.eeg_file = os.path.join(save_dir, 'eeg.txt')
        self.gsr_file = os.path.join(save_dir, 'gsr.txt')


    def WriteInfo(self, description):
        f = open(self.info_file, 'w+')
        f.write(str(description))
        f.close()

    def RunTrial(self):
        self.eeg_proc = mp.Process(target=self.eeg.startEEGStreaming(save=True))
        self.gsr_proc = mp.Process(target=self.gsr.RecordData())
        self.eeg_proc.start()
        self.gsr_proc.start()
