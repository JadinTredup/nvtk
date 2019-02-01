"""
The grove GSR sensor can be added to either an arduino or a raspberry pi. As of right now,
the only implementatio supported is the Arduino version.
"""
import multiprocessing as mp
import serial
import timeit
STD_PORT = '/dev/ttyACM2'

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
        print("File created")
        self.f = open(fn, 'w+')


    def StreamData(self):
        self.streaming = True

        while self.streaming == True:
            start = timeit.default_timer()
            value = self.ser.readline()
            print(value)
            stop = timeit.default_timer()
            print(stop - start)

    def ReadValue(self):
        value = self.ser.readline()
        value = int(value)
        return value


    def RecordData(self):
        self.recording = True
        start = timeit.default_timer()
        while self.recording == True:
            step = timeit.default_timer()
            dt = step - start
            timestamp = str(dt) + ', '
            value = self.ser.readline()
            print(value)
            value = int(value)
            value_str = str(value) + '\n'
            final_entry = timestamp + value_str
            self.f.write(final_entry)
            if dt > 10:
                self.recording = False

        self.f.close()

    def Stop(self):
        if self.recording == True:
            self.recording = False

        if self.streaming == True:
            self.streaming = False