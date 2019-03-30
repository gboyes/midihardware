import time
import mido
from midihardware.devices import MIDIInputDevice

BCF_PORT = 1

ips = mido.get_input_names()

with mido.open_input(ips[BCF_PORT]) as inport:
    try:
        bcf = MIDIInputDevice(inport=inport)
        while True:
            time.sleep(0.01)
    except KeyboardInterrupt:
        print('bye')
