import unittest

from midihardware.devices import *
from midihardware.utils import *


class TestMIDIOutputDevice(unittest.TestCase):

    def test_initializer(self):
        od = MIDIOutputDevice(channel=1, outport=None)
        self.assertEqual(1, od.channel)
        self.assertTrue(isinstance(od.tuning, EqualTemperament))

class TestMIDIInputDevice(unittest.TestCase):

    def test_initializer(self):
        idev = MIDIInputDevice(inport=None, routes={'a': 'b'})
        self.assertEqual(idev.routes, {'a': 'b'})


MIDDLE_C_HZ = 261.6255653005986

class TestEqualTemperament(unittest.TestCase):

    def test_default_maps(self):
        et = EqualTemperament()

        self.assertEqual(0, et.pitch_to_note('C-1'))
        self.assertEqual(60, et.pitch_to_note('C4'))
        self.assertEqual(69, et.pitch_to_note('A4'))
        self.assertEqual(127, et.pitch_to_note('G9'))

        self.assertEqual('C-1', et.note_to_pitch(0))
        self.assertEqual('C4', et.note_to_pitch(60))
        self.assertEqual('A4', et.note_to_pitch(69))
        self.assertEqual('G9', et.note_to_pitch(127))

    def test_conversions(self):
        et = EqualTemperament()

        self.assertEqual(440.0, et.note_to_frequency(69))
        self.assertEqual(MIDDLE_C_HZ, et.note_to_frequency(60))
        self.assertEqual(440.0, et.pitch_to_frequency('A4'))
        self.assertEqual(MIDDLE_C_HZ, et.pitch_to_frequency('C4'))
        self.assertEqual(69, et.frequency_to_note(440.0))
        self.assertEqual(60, et.frequency_to_note(MIDDLE_C_HZ))
        self.assertEqual('A4', et.frequency_to_pitch(440.0))
        self.assertEqual('C4', et.frequency_to_pitch(MIDDLE_C_HZ))

    def test_alt_temperament(self):
        et = EqualTemperament(pitches=['apple', 'banana', 'pear', 'orange'], ref='apple4', fref=345.0)

        self.assertEqual(345.0, et.pitch_to_frequency('apple4'))

