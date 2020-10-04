# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ATOM\channel_strip.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import liveobj_valid
from ableton.v2.control_surface.components import ChannelStripComponent as ChannelStripComponentBase

class ChannelStripComponent(ChannelStripComponentBase):
    empty_color = b'Mixer.EmptyTrack'

    def _update_select_button(self):
        if liveobj_valid(self._track) and self.song.view.selected_track == self._track:
            self.select_button.color = b'Mixer.Selected'
        else:
            self.select_button.color = b'DefaultButton.Off'
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/ATOM/channel_strip.pyc
