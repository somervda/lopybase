from network import LoRa
import socket
import time
import ubinascii
import pycom
import struct
import sys

# Initialise LoRa in LORAWAN mode.
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
pycom.heartbeat(False)

print("Device EUI:", ubinascii.hexlify(LoRa().mac()).upper())

pycom.rgbled(0xff8f00)  # dark orange
time.sleep(1)
pycom.rgbled(0x000000)  # off
time.sleep(1)

# Set the power to 20db for US915
# You can also set the default dr value but I found that was problematic
# You need to turn on adr (auto dynamic range) at this point it it is to be used
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.US915, adr=False, tx_power=20)

# create an OTAA authentication parameters, change them to the provided credentials
app_eui = ubinascii.unhexlify('70B3D57ED0030CD0')
app_key = ubinascii.unhexlify('0EBC5B22864A8506DAC60B95CC270212')
# uncomment to use LoRaWAN application provided dev_eui

# remove all US915 the channels

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

# join a network using OTAA (Over the Air Activation)
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)
# uncomment below to use LoRaWAN application provided dev_eui
# lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)

# wait until the module has joined the network
print('Joining', end='')
while not lora.has_joined():
    time.sleep(2.5)
    pycom.rgbled(0xff8f00)  # dark orange
    time.sleep(.5)
    pycom.rgbled(0x000000)  # off
    print('.', end='')

print('')
print('Joined')
pycom.rgbled(0x006400)  # dark green
time.sleep(2)
pycom.rgbled(0x000000)  # off
time.sleep(.5)
# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate see https://docs.exploratory.engineering/lora/dr_sf/
#  For data > 11 bytes the DR must be > 0
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 3)

# make the socket blocking
# (waits for the data to be sent and for the 2 receive windows to expire)
loop_count = 0

# struct sensor_data_struct
# {
#   uint32_t count;
#   uint32_t hall;
#   uint16_t data1;
#   uint8_t data2;
#   uint8_t data3;
#   uint32_t data4;
# };


while loop_count < 200:
    pycom.rgbled(0x00008b)  # dark blue
    time.sleep(.5)
    s.setblocking(True)
    sensor_data = struct.pack('IIHI', 10, 513, 17, 400)
    print("sensor_data", sensor_data, " Size:", struct.calcsize('IIHI'))
    # send some data
    print("Sending data:", loop_count)

    s.send(sensor_data)
    pycom.rgbled(0x000000)  # off
    time.sleep(.5)
    s.setblocking(False)

    # make the socket non-blocking
    # (because if there's no data received it will block forever...)
    # s.setblocking(False)

    # # get any data received (if any...)
    # data = s.recv(64)
    # print(data)
    time.sleep(10)
    loop_count += 1
lora.power_mode(LoRa.SLEEP)
