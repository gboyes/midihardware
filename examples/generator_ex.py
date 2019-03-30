import time
import math
import random

import mido

from midihardware.devices import Prophet6
from midihardware.utils import ThrottledGenerator

PROPHET_PORT = 1

ops = mido.get_output_names()

def mod1(params):
    t = params['t']
    prophet = params['prophet']

    note = round(abs(math.sin(0.3*t)) * 50) + 10
    vel = round(abs(math.sin(0.15*t)) * 50) + 30

    val1 = round(abs(math.sin(0.08*t)) * 50) + 30
    val2 = round(abs(math.sin(0.06*t)) * 50) + 20
    c1 = prophet.controller('low_pass_freq')
    c2 = prophet.controller('low_pass_resonance')

    prophet.control_change(c1, val1) 
    prophet.control_change(c2, val2) 
    prophet.make_note(note, vel, 0.5)
    params['t'] = t+1

with mido.open_output(ops[PROPHET_PORT]) as outport:
    try:
        outport.reset()
        prophet = Prophet6(outport=outport) 

        scale = [34, 64, 52, 44, 22, 37, 63]
        durs = [2, 4, 8]
        spb = 0.125 

        mgen = ThrottledGenerator(delta=1,
                gen=lambda p: 
                prophet.make_note(random.choice(scale), 
                    100, random.choice(durs)))

        mcont = ThrottledGenerator(delta=spb,
                gen=mod1, prophet=prophet, t=0)

        while True:
            m0 = False
            try:
                mgen.next()
            except StopIteration:
                m0 = True

            m1 = False
            try:
                mcont.next()
            except StopIteration:
                m1 = True
                
            if m0 and m1:
                break

        outport.reset()
    except KeyboardInterrupt:
        outport.reset()
