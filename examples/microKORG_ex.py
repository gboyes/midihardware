import time
import mido
from midihardware.devices import MicroKORG

PROPHET_PORT = 1 # THRU

ops = mido.get_output_names()

with mido.open_output(ops[PROPHET_PORT]) as outport:
    try:
        outport.reset()
        micro = MicroKORG(outport=outport) 

        scale = [60, 62, 64, 65, 67, 69, 71, 72]
        scale += scale[::-1]
        for note in scale:
            micro.make_note(note, 88, 0.1)
            time.sleep(0.2)
        outport.reset()
    except KeyboardInterrupt:
        outport.reset()
        print('bye')
