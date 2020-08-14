import struct
import pycom
import time


def blink(seconds, rgb):
    pycom.rgbled(rgb)  # dark orange
    time.sleep(seconds)
    pycom.rgbled(0x000000)  # off


class gps_payload:
    """ Class for managing the GPS payload data that is transmitted to the lorawan service
    update the class properties and struct definition for the particular use case """
    longitude = 0
    latitude = 0

    def __init__(self, longitude, latitude):
        self.longitude = longitude  # Float
        self.latitude = latitude  # Float

    # see format options here https://docs.python.org/2/library/struct.html#format-characters
    # Noter: use single precision float f for GPS Lng/Lat to get locations down to a meter
    def pack(self):
        return struct.pack('ff', self.longitude, self.latitude)

    def calcsize(self):
        return struct.calcsize('ff')


class sensor_payload:
    """ Class for managing the sensor payload data that is transmitted to the lorawan service
    update the class properties and struct definition for the particular use case """
    celsius = 0
    humidity = 0
    waterlevel = 0
    voltage = 0

    def __init__(self, celsius, humidity, waterlevel, voltage):
        self.celsius = celsius  # In +/- celsius
        self.humidity = humidity  # In percentage
        self.waterlevel = waterlevel  # in centimeters
        self.voltage = voltage  # In tenths of a volt

    # see format options here https://docs.python.org/2/library/struct.html#format-characters
    def pack(self):
        return struct.pack('bBBB',  self.celsius, self.humidity, self.waterlevel, self.voltage)

    def calcsize(self):
        return struct.calcsize('bBBB')
