"""
The grove GSR sensor can be added to either an arduino or a raspberry pi. As of right now,
the only implementatio supported is the Arduino version.
"""
import serial
STD_PORT = '/dev/ttyACM0'

class ArduinoGSR():
    """
    This class is currently a placeholder to represent the format the GSR class
    will eventually take. Once the sensor is aquired and implemented then the
    class will be updated to be functional.
    """
    def __init__(self, serial_port=None):
        if serial_port==None:
            serial_port = STD_PORT

        self.ser = serial.Serial(serial_port, 9600)
        self.values = []


    def StreamData(self):
        value = self.ser.readline
        value = int(value)
        print(value)


    def RecordData(self):
        value = self.ser.readline
        value = int(value)
        values.append(value)
        print(value)