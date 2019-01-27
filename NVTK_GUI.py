import PySimpleGUI as sg
from collections import namedtuple
# from NVTK.Sensors.GalvanicSkinResponse import GSRSensor
# from NVTK.Sensors.EyeTracker import PupilLabs
from NVTK.GUI.Windows import IntroductionWindow, RunSystem

# Green & tan color scheme
sg.ChangeLookAndFeel('GreenTan')
sg.SetOptions(text_justification='right')
font = 'Helvetica'

InitInfo = namedtuple('InitInfo', 'EEG GSR EyeTracking Test Record Experiment Display FileDir FileName')

def Intro():
    main_window = IntroductionWindow()
    selection = main_window.RunWindow()
    return selection

def SystemInitialization():
    system_window = RunSystem()
    trial_info = system_window.RunWindow()
    return trial_info

if __name__ == '__main__':
    selection = Intro()
    print(selection)

    if selection == 'Run System':
        trial_info = SystemInitialization()