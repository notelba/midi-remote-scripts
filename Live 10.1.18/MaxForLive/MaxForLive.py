# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MaxForLive\MaxForLive.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import ControlSurface
from ableton.v2.control_surface.input_control_element import InputControlElement, MIDI_NOTE_TYPE, MIDI_CC_TYPE, MIDI_PB_TYPE
STATUS_TO_TYPE = {144: MIDI_NOTE_TYPE, 176: MIDI_CC_TYPE, 224: MIDI_PB_TYPE}

class MaxForLive(ControlSurface):

    def __init__(self, *a, **k):
        super(MaxForLive, self).__init__(*a, **k)
        self._registered_control_names = []
        self._registered_messages = []

    def register_midi_control(self, name, status, number):
        message = (
         status, number)
        if not (isinstance(status, int) and status & 240 in (144, 176, 224) and isinstance(number, int) and 0 <= number <= 127):
            raise RuntimeError(b'register_midi_control requires parameters: name, status byte, note/CC number\n    name:\n        as used for grab/release\n    status byte:\n        0x9n for note-on/off\n        0xBn for control change\n        0xEn for pitch bend\n        where n is the channel in range 0x0..0xF\n    note/CC number:\n        0...127 (ignored for pitch bend)\n')
        if name in self._registered_control_names:
            raise RuntimeError(b"a control called '%s' has already been registered" % name)
        if message in self._registered_messages:
            raise RuntimeError(b'a control with status %d and note/CC number %d has already been registered' % message)
        with self.component_guard():
            element = InputControlElement(msg_type=STATUS_TO_TYPE[(status & 240)], channel=status & 15, identifier=number, name=name)
            self._registered_control_names.append(name)
            self._registered_messages.append(message)
        return element
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/MaxForLive/MaxForLive.pyc
