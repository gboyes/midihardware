import time
import mido
from midihardware.devices import DRM1mk3

DRM_PORT = 2

ops = mido.get_output_names()

with mido.open_output(ops[DRM_PORT]) as outport:
    drm = DRM1mk3(outport=outport) 

    for k in drm.mapping.keys():
        drm.trigger(k, 127)
        time.sleep(1.0)
