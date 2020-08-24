from lopyhelper import gps_payload, sensor_payload, blink, setUSFrequencyPlan, join, send
from network import LoRa
import socket
import time
import ubinascii
import pycom
import config
import machine


# Basic setup, get the Device EUI for use in TTN device config.
pycom.heartbeat(False)
print("Device EUI:", ubinascii.hexlify(LoRa().mac()).upper())
print("adr=", config.useADR)
blink(1, 0xff8f00)  # dark orange

# Continue session if waking up from deep sleep, else start a new lorawan session
# Note: Comment out one of the next 2 lines - when doing development , in most
# cases I can use the nvram_save() info and skip the join. In production
# only the deepsleep restore should use the saved lora info

# if machine.reset_cause() == machine.DEEPSLEEP_RESET
if True:
    lora = LoRa(mode=LoRa.LORAWAN)
    lora.nvram_restore()
    if lora.has_joined():
        print("Using existing session.")
    else:
        print("No existing session.")
        lora = join(config.app_eui, config.app_key, config.useADR)
else:
    lora = join(config.app_eui, config.app_key, config.useADR)


# ***************************************************************************
# *** Example sending data and using the deepsleep to reduce power usage ****
# ***************************************************************************

# create a LoRa socket
lora_socket = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
# set the LoRaWAN data rate see https://docs.exploratory.engineering/lora/dr_sf/
#  For data > 11 bytes the DR must be > 0 , also adr info seems to be lost between
#  deepsleeps , only fix seems to manually force the DR
lora_socket.setsockopt(socket.SOL_LORA, socket.SO_DR, 3)

# Initialize data for the lorawan send loop
sensor_data = sensor_payload(-23, 70, 2, 126)
gps_data = gps_payload(-75.30223, 40.17467)

# send sensor data, note keep the payload size below 11 bytes if possable for
# most data rate options (Example splits data into 2 data objects and sends)

#  Send location
send(lora, lora_socket, 1, gps_data, config.useADR)

#  Send sensor data
send(lora, lora_socket, 2, sensor_data, config.useADR)

print("Sleeping....")
blink(.2, 0xff0000)  # dark orange
time.sleep(.2)
blink(.2, 0xff0000)  # dark orange
machine.deepsleep(300 * 1000)
