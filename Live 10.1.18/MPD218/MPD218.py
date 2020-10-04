# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MPD218\MPD218.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from _MPDMkIIBase.MPDMkIIBase import MPDMkIIBase
PAD_CHANNEL = 9
PAD_IDS = [
 [
  48, 49, 50, 51], [44, 45, 46, 47], [40, 41, 42, 43], [36, 37, 38, 39]]

class MPD218(MPDMkIIBase):

    def __init__(self, *a, **k):
        super(MPD218, self).__init__(PAD_IDS, PAD_CHANNEL, *a, **k)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/MPD218/MPD218.pyc
