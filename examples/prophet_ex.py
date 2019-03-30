import time
import mido
from midihardware.devices import Prophet6

PROPHET_PORT = 1

ops = mido.get_output_names()

with mido.open_output(ops[PROPHET_PORT]) as outport:
    try:
        outport.reset()
        prophet = Prophet6(outport=outport) 

        scale = [60, 62, 64, 65, 67, 69, 71, 72]
        scale += scale[::-1]
        for note in scale:
            prophet.make_note(note, 88, 0.1)
            time.sleep(0.2)

        time.sleep(2.0)
        outport.reset()
    except KeyboardInterrupt:
        outport.reset()
