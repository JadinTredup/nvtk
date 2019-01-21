from tkinter import *
from random import randint
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, FigureCanvasAgg
from matplotlib.figure import Figure
import matplotlib.backends.tkagg as tkagg
import tkinter as TK
from collections import namedtuple

InitInfo = namedtuple('InitInfo', 'EEG GSR EyeTracking Test Record Experiment Display FileDir FileName')

class MainWindow():

    def __init__(self):
        self.CreateLayout()

    def CreateLayout(self):
        font = 'Helvetica'
        self.layout = [[sg.Text('Nonverbal Toolkit v0.1', font=(font, 16), justification='center')],
                [sg.Text('Sensors', font=(font, 14), justification='left')],
                    [sg.Checkbox('EEG', size=(12,1), default=True), sg.Checkbox('GSR', size=(12,1)), sg.Checkbox('Eye-Tracking', size=(12,1), default=True)],
                [sg.Text('_'*100, size=(65,1))],
                [sg.Text('Modules', font=(font, 14), justification='left')],
                    [sg.Radio('Test Sensors', 'module', size=(12,1)), sg.Radio('Free Recording', 'module', size=(12,1)), sg.Radio('Experiments', 'module', size=(12,1))],
                [sg.Text('_'*100, size=(65,1))],
                [sg.Text('Other Flags', font=(font,14), justification='left')],
                    [sg.Checkbox('Display Monitor', default=True)],
                [sg.Text('_'*100, size=(65,1))],
                [sg.Text('Save Data?', font=(font, 14), justification='left')],
                    [sg.Text('File Location:', size=(12,1)), sg.In()],
                    [sg.Text('File Name:', size=(12,1)), sg.In()],
                [sg.Submit(), sg.Cancel()]]

    def RunWindow(self):
        main_window = sg.Window('Nonverbal Toolkit', font=(font, 12)).Layout(self.layout)
        RUNNING = True

        # Start main loop
        while RUNNING:
            event, values = main_window.Read()
            if event == 'Submit':
                RUNNING = False
                trial_info = InitInfo(EEG=values[0], GSR=values[1], EyeTracking=values[2], Test=values[3],
                                      Record=values[4],
                                      Experiment=values[5], Display=values[6], FileDir=values[7], FileName=values[8])

        return trial_info

class DataMonitor():

    def __init__(self, eeg=None, gsr=None, eye_tracker=None, font=None):

        if eeg is not None:
            self.eeg_channels = eeg.channel_num
            self.eeg = True
            self.eeg_data = []
        else:
            self.eeg = False

        if gsr is not None:
            self.gsr = True
        else:
            self.gsr = False

        if eye_tracker is not None:
            self.eye_tracker = True
        else:
            self.eye_tracker = False

        if font == None:
            self.font = 'Helvetica'
        else:
            self.font = font

    def CreateElements(self):
        self.header = sg.Text('Nonverbal Toolkit - Data Monitor', font=(self.font, 16), justification='center')

        if self.eeg:
            self.eeg_title = sg.Text('EEG Data', font=(self.font, 16), justification='left')
            self.eeg_channel_elements = []
            for i in range(self.eeg_channels):
                key = 'eeg' + str(i)
                element = sg.Canvas(size=(1280,50), key=key)
                self.eeg_channel_elements.append(element)

        if self.eye_tracker:
            self.eye_title = sg.Text('Eye-Tracking Monitor', font=(self.font, 16), justification='left')
            self.eye_stream = sg.Canvas(size=(640, 480), key='eye')
            self.world_stream = sg.Canvas(size=(640, 480), key='world')

        if self.gsr:
            self.gsr_title = sg.Text('GSR Monitor', font=(self.font, 16), justification='left')

    def PlotEEG(self, sample):

        fig = Figure()
        ax1 = fig.add_subplot(12, 1, 1)

        ax2 = fig.add_subplot(12, 1, 2, sharex=ax1)

        ax3 = fig.add_subplot(12, 1, 3, sharex=ax1)

        ax4 = fig.add_subplot(12, 1, 4, sharex=ax1)

        ax5 = fig.add_subplot(12, 1, 5, sharex=ax1)

        ax6 = fig.add_subplot(12, 1, 6, sharex=ax1)

        ax7 = fig.add_subplot(12, 1, 7, sharex=ax1)

        ax8 = fig.add_subplot(12, 1, 8, sharex=ax1)

        ax9 = fig.add_subplot(12, 1, 9, sharex=ax1)

        ax10 = fig.add_subplot(12, 1, 10, sharex=ax1)

        ax11 = fig.add_subplot(12, 1, 11, sharex=ax1)

        ax12 = fig.add_subplot(12, 1, 12, sharex=ax1)

    def FormatEEGData(self, sample):
        self.eeg_data = np.delete(self.eeg_data, 0, 1)
        self.eeg_data = np.append(self.eeg_data, sample)

    def InitEEGArray(self):
        self.eeg_data = np.zeros((self.eeg_channels,1250))