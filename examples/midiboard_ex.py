import time
import mido
from midihardware.devices import Prophet6

PROPHET_PORT = 1
MIDIBOARD_PORT = 2

ops = mido.get_output_names()
ips = mido.get_input_names()

with mido.open_output(ops[PROPHET_PORT]) as outport:
    with mido.open_input(ips[MIDIBOARD_PORT]) as inport:
        try:
            outport.reset()
            prophet = Prophet6(outport=outport) 
            for msg in inport:
                prophet.send(msg)
        except KeyboardInterrupt:
            outport.reset()
