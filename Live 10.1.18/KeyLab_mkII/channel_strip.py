# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\KeyLab_mkII\channel_strip.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import liveobj_valid
from ableton.v2.control_surface.control import TextDisplayControl
from KeyLab_Essential.channel_strip import ChannelStripComponent as ChannelStripComponentBase

class ChannelStripComponent(ChannelStripComponentBase):
    track_name_display = TextDisplayControl(b' ')

    def set_track_name_display(self, display):
        self.track_name_display.set_control_element(display)
        self._update_track_name_display()

    def set_track(self, track):
        super(ChannelStripComponent, self).set_track(track)
        self._update_track_name_display()

    def _update_track_name_display(self):
        track = self._track
        self.track_name_display[0] = track.name if liveobj_valid(track) else b''
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/KeyLab_mkII/channel_strip.pyc
