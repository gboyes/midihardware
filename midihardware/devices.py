import threading
import mido


class MIDIDevice(object):
    def __init__(self, channel=None, outport=None, inport=None, input_routes=None):
        self.channel = channel
        self.outport = outport
        self.inport = inport
        self.input_routes = input_routes or {}

        if self.inport:
            self.inport.callback = self.input_handler

    def send(self, msg):
        _msg = msg.copy(channel=self.channel)
        self.outport.send(_msg)

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

    def input_handler(self, msg):
        pass


class DRM1mk3(MIDIDevice):
    DEFAULT_CHANNEL = 9
    DEFAULT_INSTRUMENT_MAP = {'kick': 36, 'drum_1': 48, 'drum_2': 41,
                       'multi': 58, 'snare': 40, 'hi_hat_1': 49,
                       'cymbal_1': 51, 'hi_hat_2': 42, 'cymbal_2': 44,
                       'clap': 39}

    def __init__(self, channel=None, outport=None, instrument_map=None):
        super().__init__(channel=channel or DRM1mk3.DEFAULT_CHANNEL, 
                outport=outport)
        self.instrument_map = instrument_map or DRM1mk3.DEFAULT_INSTRUMENT_MAP

    def trigger(self, instrument, velocity):
        self.note_on(self.instrument_map[instrument], velocity)


class Prophet6(MIDIDevice):
    DEFAULT_CHANNEL = 5
    DEFAULT_CONTROL_MAP = {'bank_select_msb': 0, 'mod_wheel': 1,
            'bpm': 3, 'foot_controller': 4, 'glide_mode': 5, 
            'data_entry_msb': 6, 'midi_volume': 7, 'sub_osc_level': 8,
            'distortion_amt': 9, 'data_entry_lsb': 38, 'volume_lsb': 39,
            'vca_env_amt': 40, 'vca_env_vel_amt': 41, 'vca_env_attack': 43,
            'vca_env_decay': 44, 'vca_env_sustain': 45, 'vca_env_release': 46,
            'low_pass_env_amt': 47, 'filter_env_attack': 50, 
            'filter_env_decay': 51, 'filter_env_sustain': 52,
            'filter_env_release': 53, 'high_pass_env_amt': 54, 
            'arp_on_off': 58, 'arp_mode': 59, 'arp_range': 60,
            'arp_time_signature': 62, 'damper_pedal': 64, 'glide_on_off': 65,
            'osc_1_freq': 67, 'osc_1_level': 69, 'osc_1_shape': 70,
            'osc_1_pulse_width': 71, 'brightness': 74, 'osc_2_freq': 75,
            'osc_2_freq_fine': 76, 'osc_2_level': 77, 'osc_2_shape': 78,
            'osc_2_pulse_width': 79, 'data_increment': 96,
            'data_decrement': 97, 'nrpn_param_lsb': 98, 'nrpn_param_msb': 99,
            'rpn_param_lsb': 100, 'rpn_param_msb': 101, 'low_pass_freq': 102,
            'low_pass_resonance': 103, 'low_pass_key_amt': 104,
            'low_pass_vel_on_off': 105, 'high_pass_freq': 106, 
            'high_pass_resonance': 107, 'high_pass_key_amt': 108,
            'high_pass_vel_on_off': 109, 'all_sound_off': 120,
            'reset_controllers': 121, 'local_control_on_off': 122,
            'all_notes_off': 123, 'omni_mode_off': 124, 'omni_mode_on': 125,
            'mono_mode_on': 126, 'poly_mode_on': 127}

    def __init__(self, channel=None, outport=None, inport=None,
            control_map=None, input_routes=None):
        super().__init__(channel=channel or Prophet6.DEFAULT_CHANNEL, 
                outport=outport, inport=inport, input_routes=input_routes)
        self.control_map = control_map or DEFAULT_CONTROL_MAP
        self.control_parser = {v: k for k, v in self.control_map.items()}
        self.control_state = {}

    def input_handler(self, msg):
        if msg.type == 'control_change':
            self.control_state[self.control_parser[msg.control]] = msg.value

    def osc_1(self, freq, level, shape, pulse_width):
        imap = zip(['osc_1_freq', 'osc_1_level', 'osc_1_shape',
            'osc_1_pulse_width'], [freq, level, shape, pulse_width])
        for m in imap:
            self.control_state[m[0]] = m[1]
            self.control_change(self.control_map[m[0]], m[1])


class TX802(MIDIDevice):
    DEFAULT_CHANNEL = 7
    DEFAULT_CONTROL_MAP = {'modulation_wheel': 1, 'breath_control': 2,
            'foot_control': 4, 'portamento_time': 5, 'volume': 7,
            'sustain_switch': 64, 'portamento_switch': 65}
    def __init__(self, channel=None, outport=None, control_map=None):
        super().__init__(channel=channel or TX802.DEFAULT_CHANNEL, 
                outport=outport)
        self.control_map = control_map or TX802.DEFAULT_CONTROL_MAP


class MicroKORG(MIDIDevice):
    DEFAULT_CHANNEL = 0
    def __init__(self, channel=None, outport=None, inport=None, 
            input_routes=None):
        super().__init__(channel=channel or MicroKORG.DEFAULT_CHANNEL, 
                outport=outport, inport=inport, input_routes=input_routes)


class OctatrackMk1(MIDIDevice):
    DEFAULT_CHANNEL = 10
    def __init__(self, channel=None, outport=None, inport=None,
            control_map=None, input_routes=None):
        super().__init__(channel=channel or OctatrackMk1.DEFAULT_CHANNEL, 
                outport=outport, inport=inport, input_routes=input_routes)

    def stop_sequencer(self):
        self.note_on(33, 127)

    def start_sequencer(self):
        self.note_on(34, 127)

    def restart_sequencer(self):
        self.note_on(35, 127)

    def play_audio_track(self, track):
        BASE = 24
        self.note_on(BASE+track, 127) 

    def play_midi_track(self, track):
        BASE = 48
        self.note_on(BASE+track, 127) 

    def trigger_sample(self, track):
        BASE = 36
        self.note_on(BASE+track, 127) 

    def pitch_sample(self, pitch):
        CENTER = 84
        if pitch < -12:
            pitch = -12
        elif pitch > 12:
            pitch = 12
        self.note_on(CENTER+pitch, 127) 

    def active_track_up(self):
        self.note_on(69, 127)

    def active_track_down(self):
        self.note_on(68, 127)
