import ubinascii

# create an OTAA authentication parameters
app_eui = ubinascii.unhexlify('70B3D57ED0030CD0')
app_key = ubinascii.unhexlify('0EBC5B22864A8506DAC60B95CC270212')

#  Use adr (automatic data rate), note adr does
#  not play well with deepsleep for some reason
#  It may have something to do with the adr being sent from the gateway and
# not being saved after a deepsleep, there are some rules about not stepping between more than one dr
# at a time?
useADR = False
