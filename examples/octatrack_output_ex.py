import time
import mido
from midihardware.devices import OctatrackMk1

OCT_PORT = 0

ops = mido.get_output_names()

with mido.open_output(ops[OCT_PORT]) as outport:
    try:
        octa = OctatrackMk1(outport=outport)
        
        print('Starting Sequencer')
        octa.start_sequencer()
        time.sleep(1.0)
        
        print('Stopping Sequencer')
        octa.stop_sequencer()
        time.sleep(1.0)

        for i in range(8):
            octa.trigger_sample(i)
            time.sleep(0.1)
        octa.stop_sequencer()

        #for i in range(8):
        #    octa.play_audio_track(i)
        #    time.sleep(1.0)
        #octa.stop_sequencer()

        for t in range(8):
            octa.active_track_down()

        for t in range(8):
            for i in range(-12, 13):
                octa.pitch_sample(i)
                time.sleep(0.2)
            octa.active_track_up()
        octa.stop_sequencer()

    except KeyboardInterrupt:
        outport.reset()
        print('bye')
