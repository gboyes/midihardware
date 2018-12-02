import time
import mido
from midihardware.devices import MIDIDevice

BCF_PORT = 1

ips = mido.get_input_names()

with mido.open_input(ips[BCF_PORT]) as inport:
    try:
        bcf = MIDIDevice(inport=inport)
        while True:
            pass
    except KeyboardInterrupt:
        print('bye')
