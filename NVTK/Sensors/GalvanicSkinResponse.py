"""
This code needs to be run either directly on the raspberry pi or via SSH
"""

import math
import sys
import time
from grove.adc import ADC


class GroveGSRSensor:

    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()

    @property
    def GSR(self):
        value = self.adc.read(self.channel)
        return value

Grove = GroveGSRSensor

#
# def main():
#     if len(sys.argv) < 2:
#         print('Usage: {} adc_channel'.format(sys.argv[0]))
#         sys.exit(1)
#
#     sensor = GroveGSRSensor(int(sys.argv[1]))
#
#     print('Detecting...')
#     while True:
#         print('GSR value: {0}'.format(sensor.GSR))
#         time.sleep(.3)

class GSRSensor():
    """
    This class is currently a placeholder to represent the format the GSR class
    will eventually take. Once the sensor is aquired and implemented then the
    class will be updated to be functional.
    """
    def __init__(self):

    def StartSensor(self):

    def StreamData(self):

    def RecordData(self):