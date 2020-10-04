# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\SL_MkIII\caching_control_element.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import depends
from ableton.v2.control_surface import ControlElement
from .sysex import SET_PROPERTY_MSG_HEADER

class CachingControlElement(ControlElement):

    @depends(message_cache=None)
    def __init__(self, message_cache=None, *a, **k):
        super(CachingControlElement, self).__init__(*a, **k)
        self._message_cache = message_cache

    def send_midi(self, midi_event_bytes, **k):
        self._message_cache(midi_event_bytes[len(SET_PROPERTY_MSG_HEADER):-1])
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/SL_MkIII/caching_control_element.pyc
