# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad_X\channel_strip.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import liveobj_valid
from novation.channel_strip import ChannelStripComponent as ChannelStripComponentBase

class ChannelStripComponent(ChannelStripComponentBase):

    def update(self):
        super(ChannelStripComponent, self).update()
        self._update_static_color_control()

    def _update_static_color_control(self):
        valid_track = liveobj_valid(self._track)
        color_value = self._static_color_value if valid_track else 0
        if valid_track and self._send_controls:
            send_index = next((i for i, x in enumerate(self._send_controls) if x), None)
            if send_index is not None and send_index >= len(self._track.mixer_device.sends):
                color_value = 0
        self.static_color_control.value = color_value
        return
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Launchpad_X/channel_strip.pyc
