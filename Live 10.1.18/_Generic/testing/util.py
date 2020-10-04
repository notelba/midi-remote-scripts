# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Generic\testing\util.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
import Live
from ableton.v2.base import const, nop
from ableton.v2.testing import count_calls

class MockControlSurface(object):
    instance_identifier = const(0)
    request_rebuild_midi_map = count_calls()
    show_message = nop
    send_midi = nop

    def __init__(self, *a, **k):
        super(MockControlSurface, self).__init__(*a, **k)
        self._song = Live.Song.Song(num_tracks=4, num_returns=2)

    def song(self):
        return self._song
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/_Generic/testing/util.pyc
