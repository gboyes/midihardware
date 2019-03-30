import time
import mido
from midihardware.devices import TX802

TX_PORT = 3

ops = mido.get_output_names()

with mido.open_output(ops[TX_PORT]) as outport:
    try:
        outport.reset()
        tx = TX802(outport=outport) 

        scale = [60, 62, 64, 65, 67, 69, 71, 72]
        scale += scale[::-1]
        for note in scale:
            tx.make_note(note, 88, 0.1)
            time.sleep(0.2)

        time.sleep(2.0)
        outport.reset()
    except KeyboardInterrupt:
        outport.reset()
