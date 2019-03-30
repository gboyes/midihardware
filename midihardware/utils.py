import math
import time


MIDI_MAX = 127


class EqualTemperament():
    def __init__(self, pitches=['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'], ref='A4', fref=440.0):
      
        self.tones = len(pitches)
        self._ref = ref
        self._fref = fref
        self._note_map = {'{}{}'.format(pitches[i%self.tones], i//self.tones - 1): i
                for i in range(MIDI_MAX+1)} # octave starts at -1 by convention 
        self._pitch_map = {v:k for k,v in self._note_map.items()}

    def pitch_to_note(self, pitch):
        return self._note_map[pitch]

    def note_to_pitch(self, note):
        return self._pitch_map[note]

    def note_to_frequency(self, note):
        return 2**((note-self._note_map[self._ref])/float(self.tones)) * self._fref

    def pitch_to_frequency(self, pitch):
        return self.note_to_frequency(self.pitch_to_note(pitch))

    def frequency_to_note(self, frequency):
        return self.tones * math.log2(frequency/self._fref) + self.pitch_to_note(self._ref)

    def frequency_to_pitch(self, frequency):
        return self.note_to_pitch(int(self.frequency_to_note(frequency)))

class ThrottledGenerator():
    def __init__(self, delta=None, num=None, gen=None, **genargs):
        self.delta = delta or 0
        self.last = 0
        self.genargs = genargs
        self.gen = gen
        self.num = num
        self.count = 0
    
    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        if self.num and self.count >= self.num:
            raise StopIteration

        t = time.time()
        if t - self.last > self.delta:
            self.last = t
            self.count += 1
            return self.gen(self.genargs) 
        else:
            return None


