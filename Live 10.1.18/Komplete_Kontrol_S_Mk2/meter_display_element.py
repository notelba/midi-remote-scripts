# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Komplete_Kontrol_S_Mk2\meter_display_element.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import task
from ableton.v2.control_surface import ControlElement, midi
METERS_PER_SEGMENT = 2
CLEAR_VALUE = 0

class MeterDisplayElement(ControlElement):

    def __init__(self, header, num_segments, *a, **k):
        super(MeterDisplayElement, self).__init__(*a, **k)
        self._header = header
        self._clear_values = [ CLEAR_VALUE for _ in xrange(num_segments * METERS_PER_SEGMENT) ]
        self._meter_values = list(self._clear_values)
        self._last_sent_message = None
        self._send_message_task = self._tasks.add(task.run(self._send_message))
        self._send_message_task.kill()
        return

    def update_meter_display(self, display_offset, values):
        self._meter_values[display_offset] = values[0]
        self._meter_values[display_offset + 1] = values[1]
        self._request_send_message()

    def reset(self):
        self._meter_values = list(self._clear_values)
        self._request_send_message()

    def send_midi(self, midi_bytes):
        if midi_bytes != self._last_sent_message:
            super(MeterDisplayElement, self).send_midi(midi_bytes)
            self._last_sent_message = midi_bytes

    def _request_send_message(self):
        self._send_message_task.restart()

    def _send_message(self, *a):
        self.send_midi(self._header + tuple(self._meter_values) + (midi.SYSEX_END,))
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Komplete_Kontrol_S_Mk2/meter_display_element.pyc
