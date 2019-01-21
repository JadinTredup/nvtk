import PySimpleGUI as sg
from collections import namedtuple
# from NVTK.Sensors.GalvanicSkinResponse import GSRSensor
# from NVTK.Sensors.EyeTracker import PupilLabs
from NVTK.GUI.Windows import MainWindow

# Green & tan color scheme
sg.ChangeLookAndFeel('GreenTan')
sg.SetOptions(text_justification='right')
font = 'Helvetica'

InitInfo = namedtuple('InitInfo', 'EEG GSR EyeTracking Test Record Experiment Display FileDir FileName')

if __name__ == '__main__':
    main_window = MainWindow()
    trial_info = main_window.RunWindow()
    print(trial_info)