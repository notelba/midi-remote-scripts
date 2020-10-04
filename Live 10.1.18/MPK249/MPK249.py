# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MPK249\MPK249.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ControlSurface import ControlSurface
from _Framework.Layer import Layer
from _Framework.DrumRackComponent import DrumRackComponent
from _Framework.TransportComponent import TransportComponent
from _Framework.MixerComponent import MixerComponent
from _Framework.MidiMap import MidiMap as MidiMapBase
from _Framework.MidiMap import make_button, make_encoder, make_slider
from _Framework.InputControlElement import MIDI_NOTE_TYPE, MIDI_CC_TYPE

class MidiMap(MidiMapBase):

    def __init__(self, *a, **k):
        super(MidiMap, self).__init__(*a, **k)
        self.add_button(b'Play', 0, 118, MIDI_CC_TYPE)
        self.add_button(b'Record', 0, 119, MIDI_CC_TYPE)
        self.add_button(b'Stop', 0, 117, MIDI_CC_TYPE)
        self.add_button(b'Loop', 0, 114, MIDI_CC_TYPE)
        self.add_button(b'Forward', 0, 116, MIDI_CC_TYPE)
        self.add_button(b'Backward', 0, 115, MIDI_CC_TYPE)
        self.add_matrix(b'Sliders', make_slider, 0, [[12, 13, 14, 15, 16, 17, 18, 19]], MIDI_CC_TYPE)
        self.add_matrix(b'Encoders', make_encoder, 0, [[22, 23, 24, 25, 26, 27, 28, 29]], MIDI_CC_TYPE)
        self.add_matrix(b'Arm_Buttons', make_button, 0, [
         [
          32, 33, 34, 35, 36, 37, 38, 39]], MIDI_CC_TYPE)
        self.add_matrix(b'Drum_Pads', make_button, 1, [
         [
          81, 83, 84, 86], [74, 76, 77, 79], [67, 69, 71, 72], [60, 62, 64, 65]], MIDI_NOTE_TYPE)


class MPK249(ControlSurface):

    def __init__(self, *a, **k):
        super(MPK249, self).__init__(*a, **k)
        with self.component_guard():
            midimap = MidiMap()
            drum_rack = DrumRackComponent(name=b'Drum_Rack', is_enabled=False, layer=Layer(pads=midimap[b'Drum_Pads']))
            drum_rack.set_enabled(True)
            transport = TransportComponent(name=b'Transport', is_enabled=False, layer=Layer(play_button=midimap[b'Play'], record_button=midimap[b'Record'], stop_button=midimap[b'Stop'], seek_forward_button=midimap[b'Forward'], seek_backward_button=midimap[b'Backward'], loop_button=midimap[b'Loop']))
            transport.set_enabled(True)
            mixer_size = len(midimap[b'Sliders'])
            mixer = MixerComponent(mixer_size, name=b'Mixer', is_enabled=False, layer=Layer(volume_controls=midimap[b'Sliders'], pan_controls=midimap[b'Encoders'], arm_buttons=midimap[b'Arm_Buttons']))
            mixer.set_enabled(True)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/MPK249/MPK249.pyc
