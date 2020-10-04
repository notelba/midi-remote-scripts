# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Alesis_V\Alesis_V.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
import Live
from _Framework.ControlSurface import ControlSurface
from _Framework.Layer import Layer
from _Framework.EncoderElement import EncoderElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.InputControlElement import MIDI_CC_TYPE
from _Framework.DeviceComponent import DeviceComponent

class Alesis_V(ControlSurface):

    def __init__(self, *a, **k):
        super(Alesis_V, self).__init__(*a, **k)
        with self.component_guard():
            encoders = ButtonMatrixElement(rows=[
             [ EncoderElement(MIDI_CC_TYPE, 0, identifier + 20, Live.MidiMap.MapMode.absolute, name=b'Encoder_%d' % identifier) for identifier in xrange(4)
             ]])
            device = DeviceComponent(name=b'Device', is_enabled=False, layer=Layer(parameter_controls=encoders), device_selection_follows_track_selection=True)
            device.set_enabled(True)
            self.set_device_component(device)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Alesis_V/Alesis_V.pyc
