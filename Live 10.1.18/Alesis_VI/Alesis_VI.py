# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Alesis_VI\Alesis_VI.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ControlSurface import ControlSurface
from _Framework.MidiMap import make_encoder, MidiMap as MidiMapBase
from _Framework.InputControlElement import MIDI_CC_TYPE
from _Framework.ButtonElement import ButtonElement
from _Framework.Layer import Layer
from _Framework.TransportComponent import TransportComponent
from _Framework.MixerComponent import MixerComponent

class MidiMap(MidiMapBase):

    def __init__(self, *a, **k):
        super(MidiMap, self).__init__(*a, **k)
        self.add_momentary_button(b'Stop', 0, 118, MIDI_CC_TYPE)
        self.add_momentary_button(b'Play', 0, 119, MIDI_CC_TYPE)
        self.add_momentary_button(b'Loop', 0, 115, MIDI_CC_TYPE)
        self.add_momentary_button(b'Record', 0, 114, MIDI_CC_TYPE)
        self.add_momentary_button(b'Forward', 0, 117, MIDI_CC_TYPE)
        self.add_momentary_button(b'Backward', 0, 116, MIDI_CC_TYPE)
        self.add_matrix(b'Volume_Encoders', make_encoder, 0, [
         range(20, 32) + [35, 41, 46, 47]], MIDI_CC_TYPE)

    def add_momentary_button(self, name, channel, number, midi_message_type):
        assert name not in self.keys()
        self[name] = ButtonElement(True, midi_message_type, channel, number, name=name)


class Alesis_VI(ControlSurface):

    def __init__(self, *a, **k):
        super(Alesis_VI, self).__init__(*a, **k)
        with self.component_guard():
            midimap = MidiMap()
            transport = TransportComponent(name=b'Transport', is_enabled=False, layer=Layer(play_button=midimap[b'Play'], stop_button=midimap[b'Stop'], loop_button=midimap[b'Loop'], record_button=midimap[b'Record'], seek_forward_button=midimap[b'Forward'], seek_backward_button=midimap[b'Backward']))
            mixer_size = len(midimap[b'Volume_Encoders'])
            mixer = MixerComponent(mixer_size, name=b'Mixer', is_enabled=False, layer=Layer(volume_controls=midimap[b'Volume_Encoders']))
            transport.set_enabled(True)
            mixer.set_enabled(True)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Alesis_VI/Alesis_VI.pyc
