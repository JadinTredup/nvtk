"""
The grove GSR sensor can be added to either an arduino or a raspberry pi. As of right now,
the only implementatio supported is the Arduino version.
"""
import serial
import timeit
STD_PORT = '/dev/ttyACM0'

class ArduinoGSR():
    """
    This class is currently a placeholder to represent the format the GSR class
    will eventually take. Once the sensor is aquired and implemented then the
    class will be updated to be functional.
    """
    def __init__(self, serial_port=None, save_fn=None):
        self.streaming = False
        self.recording = False
        if serial_port==None:
            serial_port = STD_PORT

        self.ser = serial.Serial(serial_port, 9600)
        self.values = []

        if save_fn is None:
            save_fn = 'GSR-Temp.txt'

        self.InitSaveFile(save_fn)


    def InitSaveFile(self, fn):
        self.f = open(fn, 'w+')


    def StreamData(self):
        self.streaming = True

        while self.streaming == True:
            start = timeit.default_timer()
            value = self.ser.readline()
            value = int(value)
            print(value)
            stop = timeit.default_timer()
            print(stop - start)

    def ReadValue(self):
        value = self.ser.readline()
        value = int(value)
        return value


    def RecordData(self):
        self.recording = True

        while self.recording == True:
            value = self.ser.readline
            value = int(value)
            value_str = str(value) + '\n'
            self.f.write(value_str)

        self.f.close()

    def StopData(self):
        if self.recording == True:
            self.recording = False

        if self.streaming == True:
            self.streaming = False