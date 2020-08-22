# lopybase

Basic lopy4 example for testing pycom lopy4 lorawan capabilities

This includes code for joining a TTN (The Things Network) LoraWan network, and use of a deepsleep to minimize power usage between uploading sensor data. A video explaining some of this is at https://youtu.be/5pBcGdR8pR4

I have created the lorahelper.py library to separate commonally used functions like join and send,
encapsulate the US915 frequency plan setup, and create and example of using payload classes to manage the data being sent to TTN network.

I have started on a jupyter document with information I have gathered on power usage in various hardware scenarios (Work in progress) see [lopy4 power usage](lopy4%20battery%20usage.ipynb)
