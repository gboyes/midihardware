import time
import mido
from midihardware.devices import OctatrackMk1

OCT_PORT = 0

ips = mido.get_input_names()

with mido.open_input(ips[OCT_PORT]) as inport:
    try:
        octa = OctatrackMk1(inport=inport)
        while True:
            pass
    except KeyboardInterrupt:
        print('bye')
