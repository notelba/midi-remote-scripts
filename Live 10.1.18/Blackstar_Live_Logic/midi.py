# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Blackstar_Live_Logic\midi.py
# Compiled at: 2020-07-20 20:22:59
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.midi import SYSEX_START, SYSEX_END
SYSEX_HEADER = (
 SYSEX_START, 0, 32, 114)
NUMERIC_DISPLAY_COMMAND = (0, )
LIVE_INTEGRATION_MODE_ID = (
 SYSEX_START,
 0,
 0,
 116,
 1,
 0,
 77,
 67,
 1,
 0,
 7,
 1,
 0)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Blackstar_Live_Logic/midi.pyc
