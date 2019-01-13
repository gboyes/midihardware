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

    val1 = round(abs(math.sin(0.05*t)) * 40) + 40
    val2 = round(abs(math.sin(0.03*t)) * 80) + 20
    c1 = prophet.control_map['low_pass_freq']
    c2 = prophet.control_map['low_pass_resonance'] 

    prophet.control_change(c1, val1) 
    prophet.control_change(c2, val2) 
    params['t'] = t+1

def mod2(params):
    t = params['t']
    prophet = params['prophet']

    val1 = round(abs(math.sin(0.05*t)) * 40) + 40
    val2 = round(abs(math.sin(0.03*t)) * 80) + 20
    val3 = round(abs(math.sin(0.01*t)) * 80) + 20
    val4 = round(abs(math.sin(0.09*t)) * 80) + 20

    prophet.osc_1(val1, val2, val3, val4)
    params['t'] = t+1
    
def mod3(params):
    t = params['t']
    prophet = params['prophet']

    val1 = round(abs(math.sin(0.15*t)) * 40) + 40
    val2 = round(abs(math.sin(0.23*t)) * 80) + 20
    val3 = round(abs(math.sin(0.11*t)) * 80) + 20
    val4 = round(abs(math.sin(0.29*t)) * 80) + 20
    val5 = round(abs(math.sin(0.19*t)) * 80) + 20

    prophet.osc_2(val1, val2, val3, val4, val5)
    params['t'] = t+1


with mido.open_output(ops[PROPHET_PORT]) as outport:
    try:
        outport.reset()
        prophet = Prophet6(outport=outport) 

        scale = [45, 54, 60, 62, 64, 67, 71, 72]
        durs = [0.25, 0.5, 1, 2, 4, 0.125]
        spb = 2 

        mgen = ThrottledGenerator(delta=spb, num=100,
                gen=lambda p: 
                prophet.make_note(random.choice(scale), 80, random.choice(durs)))
        mcont = ThrottledGenerator(delta=3, num=35,
                gen=mod1, prophet=prophet, t=0)

        mosc = ThrottledGenerator(delta=5, num=20,
                gen=mod2, prophet=prophet, t=0)
        
        mosc1 = ThrottledGenerator(delta=7, num=9,
                gen=mod3, prophet=prophet, t=0)


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
                
            m2 = False
            try:
                mosc.next()
            except StopIteration:
                m2 = True

            m3 = False
            try:
                mosc1.next()
            except StopIteration:
                m3 = True
            
            if m0 and m1 and m2 and m3:
                break

        outport.reset()
    except KeyboardInterrupt:
        outport.reset()
        print('bye')
