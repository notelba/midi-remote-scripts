# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ATOMSQ\channel_strip.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import liveobj_valid
from ableton.v2.control_surface.components import ChannelStripComponent as ChannelStripComponentBase
from .control import DisplayControl

class ChannelStripComponent(ChannelStripComponentBase):
    track_name_display = DisplayControl()

    def _update_track_name_data_source(self):
        self.track_name_display.message = self._track.name if liveobj_valid(self._track) else b' - '
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/ATOMSQ/channel_strip.pyc
