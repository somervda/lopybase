import struct


class data:
    count = 1
    hall = 0

    def __init__(self, count, hall):
        self.count = count
        self.hall = hall

    def pack(self):
        return struct.pack('II', self.count, self.hall)

    def calcsize(self):
        return struct.calcsize('II')
