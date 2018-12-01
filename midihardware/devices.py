import threading

import mido


class MIDIDevice(object):
    def __init__(self, channel=None, outport=None, inport=None):
        self.channel = channel
        self.outport = outport
        self.inport = inport

    def make_note(self, note, velocity, duration):
        self.note_on(note, velocity)
        timer = threading.Timer(duration, self.note_off, args=[note, velocity])
        timer.start()

    def note_on(self, note, velocity):
        msg = mido.Message('note_on', channel=self.channel, note=note, 
                velocity=velocity) 
        self.outport.send(msg)

    def note_off(self, note, velocity):
        msg = mido.Message('note_off', channel=self.channel, note=note, 
                velocity=velocity) 
        self.outport.send(msg)

    def polytouch(self, note, value):
        msg = mido.Message('polytouch', channel=self.channel, note=note, 
                value=value) 
        self.outport.send(msg)

    def pitchwheel(self, pitch):
        msg = mido.Message('pitchwheel', channel=self.channel, pitch=pitch) 
        self.outport.send(msg)

    def aftertouch(self, value):
        msg = mido.Message('aftertouch', channel=self.channel, value=value)
        self.outport.send(msg)

    def control_change(self, control, value):
        msg = mido.Message('control_change', channel=self.channel, 
                control=control, value=value)
        self.outport.send(msg)

    def program_change(self, program):
        msg = mido.Message('program_change', channel=self.channel, 
                program=program)
        self.outport.send(msg)


class DRM1mk3(MIDIDevice):
    DEFAULT_CHANNEL = 9
    DEFAULT_MAPPING = {'kick': 36, 'drum_1': 48, 'drum_2': 41,
                       'multi': 58, 'snare': 40, 'hi_hat_1': 49,
                       'cymbal_1': 51, 'hi_hat_2': 42, 'cymbal_2': 44,
                       'clap': 39}

    def __init__(self, channel=None, outport=None, inport=None, mapping=None):
        super().__init__(channel=channel or DRM1mk3.DEFAULT_CHANNEL, 
                outport=outport, inport=inport)
        self.mapping = mapping or DRM1mk3.DEFAULT_MAPPING

    def trigger(self, name, velocity):
        self.note_on(self.mapping[name], velocity)


class Prophet6(MIDIDevice):
    DEFAULT_CHANNEL = 5

    def __init__(self, channel=None, outport=None, inport=None):
        super().__init__(channel=channel or Prophet6.DEFAULT_CHANNEL, 
                outport=outport, inport=inport)


class TX802(MIDIDevice):
    DEFAULT_CHANNEL = 7

    def __init__(self, channel=None, outport=None, inport=None):
        super().__init__(channel=channel or TX802.DEFAULT_CHANNEL, 
                outport=outport, inport=inport)


class MicroKORG(MIDIDevice):
    DEFAULT_CHANNEL = 0

    def __init__(self, channel=None, outport=None, inport=None):
        super().__init__(channel=channel or MicroKORG.DEFAULT_CHANNEL, 
                outport=outport, inport=inport)
