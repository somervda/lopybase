import struct


class payload:
    """ Class for managing the payload data that is transmitted to the lorawan service
    update the class properties and struct definition for the particular use case """
    count = 1
    hall = 0

    def __init__(self, count, hall):
        self.count = count
        self.hall = hall

    # see format options here https://docs.python.org/2/library/struct.html#format-characters
    def pack(self):
        return struct.pack('HH', self.count, self.hall)

    def calcsize(self):
        return struct.calcsize('HH')
