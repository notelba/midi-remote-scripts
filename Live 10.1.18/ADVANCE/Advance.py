# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ADVANCE\Advance.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
import Live
from _Framework.ControlSurface import ControlSurface
from _Framework.Layer import Layer
from _Framework.DeviceComponent import DeviceComponent
from _Framework.DrumRackComponent import DrumRackComponent
from _Framework.TransportComponent import TransportComponent
from _Framework.InputControlElement import MIDI_CC_TYPE, MIDI_NOTE_TYPE
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ButtonElement import ButtonElement
from _Framework.EncoderElement import EncoderElement
PAD_CHANNEL = 1
PAD_IDS = (
 (81, 83, 84, 86), (74, 76, 77, 79), (67, 69, 71, 72), (60, 62, 64, 65))

def make_encoder(identifier, name):
    return EncoderElement(MIDI_CC_TYPE, 0, identifier, Live.MidiMap.MapMode.absolute, name=name)


def make_button(identifier, name, msg_type=MIDI_NOTE_TYPE, channel=PAD_CHANNEL):
    return ButtonElement(True, msg_type, channel, identifier, name=name)


class Advance(ControlSurface):

    def __init__(self, *a, **k):
        super(Advance, self).__init__(*a, **k)
        with self.component_guard():
            encoders = ButtonMatrixElement(rows=[
             [ make_encoder(index + 22, b'Encoder_%d' % index) for index in xrange(8)
             ]])
            pads = ButtonMatrixElement(rows=[ [ make_button(identifier, b'Pad_%d_%d' % (col, row)) for col, identifier in enumerate(row_ids) ] for row, row_ids in enumerate(PAD_IDS)
                                            ])
            device = DeviceComponent(is_enabled=False, layer=Layer(parameter_controls=encoders), device_selection_follows_track_selection=True)
            device.set_enabled(True)
            self.set_device_component(device)
            drums = DrumRackComponent(is_enabled=False, layer=Layer(pads=pads))
            drums.set_enabled(True)
            play_button = make_button(118, b'Play_Button', MIDI_CC_TYPE, 0)
            stop_button = make_button(117, b'Stop_Button', MIDI_CC_TYPE, 0)
            record_button = make_button(119, b'Record_Button', MIDI_CC_TYPE, 0)
            loop_button = make_button(114, b'Loop_Button', MIDI_CC_TYPE, 0)
            transport = TransportComponent(is_enabled=False, layer=Layer(play_button=play_button, stop_button=stop_button, record_button=record_button, loop_button=loop_button))
            transport.set_enabled(True)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/ADVANCE/Advance.pyc
