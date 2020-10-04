# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\SL_MkIII\midi_message_cache.py
# Compiled at: 2020-07-14 15:33:46
from __future__ import absolute_import, print_function, unicode_literals
from .sysex import NUM_SET_PROPERTY_HEADER_BYTES

class MidiMessageCache(object):

    def __init__(self, *a, **k):
        super(MidiMessageCache, self).__init__(*a, **k)
        self._messages = []

    def __call__(self, message):
        self._messages = filter(lambda m: m[:NUM_SET_PROPERTY_HEADER_BYTES] != message[:NUM_SET_PROPERTY_HEADER_BYTES], self._messages)
        self._messages.append(message)

    @property
    def messages(self):
        return self._messages

    def clear(self):
        self._messages = []
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/SL_MkIII/midi_message_cache.pyc
