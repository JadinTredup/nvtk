from tkinter import *
from random import randint
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, FigureCanvasAgg
from matplotlib.figure import Figure
import matplotlib.backends.tkagg as tkagg
import tkinter as TK
from collections import namedtuple

InitInfo = namedtuple('InitInfo', 'EEG GSR EyeTracking Test Record Experiment Display FileDir FileName')

class IntroductionWindow():

    def __init__(self):
        self.CreateLayout()

    def CreateLayout(self):
        font = 'Helvetica'
        self.layout = [[sg.Text('Nonverbal Toolkit', font=(font, 16), justification='center')],
                       [sg.Text('What would you like to do?', font=(font, 16), justification='center')],
                       [sg.InputOptionMenu(('Run Experiments', 'Free Record', 'Data Analysis'))],
                       [sg.Submit(), sg.Cancel()]]

    def RunWindow(self):
        main_window = sg.Window('Nonverbal Toolkit', font=(font, 12)).Layout(self.layout)
        RUNNING = True

        # Start main loop
        while RUNNING:
            event, values = main_window.Read()
            if event == 'Submit':
                RUNNING = False
                selection = values[0]

        return selection


class RunSystem():

    def __init__(self):
        self.CreateLayout()

    def CreateLayout(self):
        font = 'Helvetica'
        self.layout = [[sg.Text('Nonverbal Toolkit', font=(font, 16), justification='center')],
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


class TrialDescription():

    def __init__(self):
        self.CreateLayout()

    def CreateLayout(self):
        font = 'Helvetica'
        self.layout = [[sg.Text('Enter information about trial', font=(font, 16), justification='center')],
                       [sg.Text('Save Directory:', size=(12, 1)), sg.In()],
                       [sg.Multiline(size=(35, 3))],
                       [sg.Submit(), sg.Cancel()]]

    def RunWindow(self):
        main_window = sg.Window('Nonverbal Toolkit', font=(font, 12)).Layout(self.layout)
        RUNNING = True

        # Start main loop
        while RUNNING:
            event, values = main_window.Read()
            if event == 'Submit':
                RUNNING = False
                save_dir = values[0]
                decription = values[1]

        return description, save_dir