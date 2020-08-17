import struct
import pycom
import time
from network import LoRa


def blink(seconds, rgb):
    pycom.rgbled(rgb)
    time.sleep(seconds)
    pycom.rgbled(0x000000)  # off


def setUSFrequencyPlan(lora):
    """ Sets the frequency plan that matches the TTN gateway in the USA """
    # remove all US915 channels
    for channel in range(0, 72):
        lora.remove_channel(channel)

    # set all channels to the same frequency (must be before sending the OTAA join request)
    ttn_start_frequency = 903900000
    ttn_step_frequency = 200000
    ttn_ch8_frequency = 904600000

    # Set up first 8 US915 TTN uplink channels
    for channel in range(0, 9):
        if (channel == 8):
            channel_frequency = ttn_ch8_frequency
            # DR3 = SF8/500kHz
            channel_dr_min = 4
            channel_dr_max = 4
        else:
            channel_frequency = ttn_start_frequency + \
                (channel * ttn_step_frequency)
            # DR0 = SF10/125kHz
            channel_dr_min = 0
            # DR3 = SF7/125kHz
            channel_dr_max = 3
        lora.add_channel(channel, frequency=channel_frequency,
                         dr_min=channel_dr_min, dr_max=channel_dr_max)
        print("Added channel", channel, channel_frequency,
              channel_dr_min, channel_dr_max)


def join(app_eui, app_key, useADR):
    """ Join the Lorawan network using OTAA. new lora session is returned """
    # Set the power to 20db for US915
    # You can also set the default dr value but I found that was problematic
    # You need to turn on adr (auto data rate) at this point if it is to be used
    # only use adr for static devices (Not moving)
    # see https://lora-developers.semtech.com/library/tech-papers-and-guides/understanding-adr/
    lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.US915,
                adr=useADR, tx_power=20)
    setUSFrequencyPlan(lora)

    print('Joining', end='')
    lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)
    # wait until the module has joined the network
    while not lora.has_joined():
        time.sleep(2.5)
        blink(.5, 0xff8f00)  # dark orange
        print('.', end='')
    print('')
    print('Joined')
    blink(2, 0x006400)  # dark green
    return lora


def send(lora, socket, port, payload, useADR):
    """ send data to the lorawan gateway on selected port """
    blink(.5, 0x00008b)  # dark blue
    socket.setblocking(True)
    socket.bind(port)
    print("Sending data:", payload.pack(), " Size:", payload.calcsize())
    socket.send(payload.pack())
    # Give send a extra second to be returned before switching
    #  the socket blocking mode (May not need this)
    time.sleep(1)
    socket.setblocking(False)
    lora.nvram_save()


class gps_payload:
    """ Class for managing the GPS payload data that is transmitted to the lorawan service
    update the class properties and struct definition for the particular use case """
    longitude = 0
    latitude = 0
    pack_format = "ff"

    def __init__(self, longitude, latitude):
        self.longitude = longitude  # Float
        self.latitude = latitude  # Float

    # see format options here https://docs.python.org/2/library/struct.html#format-characters
    # Noter: use single precision float f for GPS Lng/Lat to get locations down to a meter
    def pack(self):
        return struct.pack(self.pack_format, self.longitude, self.latitude)

    def calcsize(self):
        return struct.calcsize(self.pack_format)


class sensor_payload:
    """ Class for managing the sensor payload data that is transmitted to the lorawan service
    update the class properties and struct definition for the particular use case """
    celsius = 0
    humidity = 0
    waterlevel = 0
    voltage = 0
    pack_format = "bBBB"

    def __init__(self, celsius, humidity, waterlevel, voltage):
        self.celsius = celsius  # In +/- celsius
        self.humidity = humidity  # In percentage
        self.waterlevel = waterlevel  # in centimeters
        self.voltage = voltage  # In tenths of a volt

    # see format options here https://docs.python.org/2/library/struct.html#format-characters
    def pack(self):
        return struct.pack(self.pack_format,  self.celsius, self.humidity, self.waterlevel, self.voltage)

    def calcsize(self):
        return struct.calcsize(self.pack_format)
