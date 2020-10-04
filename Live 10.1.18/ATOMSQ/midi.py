# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ATOMSQ\midi.py
# Compiled at: 2020-06-08 15:00:06
from __future__ import absolute_import, print_function, unicode_literals
NATIVE_MODE_ON_MESSAGE = (143, 0, 1)
NATIVE_MODE_OFF_MESSAGE = (143, 0, 0)
RED_MIDI_CHANNEL = 1
GREEN_MIDI_CHANNEL = 2
BLUE_MIDI_CHANNEL = 3
USER_MODE_START_CHANNEL = 10
SYSEX_START_BYTE = 240
SYSEX_END_BYTE = 247
SYSEX_HEADER = (
 SYSEX_START_BYTE, 0, 1, 6, 34)
DISPLAY_HEADER = SYSEX_HEADER + (18, )
LOWER_FIRMWARE_TOGGLE_HEADER = SYSEX_HEADER + (19, )
UPPER_FIRMWARE_TOGGLE_HEADER = SYSEX_HEADER + (20, )
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/ATOMSQ/midi.pyc
