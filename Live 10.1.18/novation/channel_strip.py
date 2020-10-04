# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\novation\channel_strip.py
# Compiled at: 2020-05-05 13:23:29
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import listens, liveobj_valid
from ableton.v2.control_surface.components import ChannelStripComponent as ChannelStripComponentBase
from ableton.v2.control_surface.control import SendValueControl
from .util import get_midi_color_value_for_track

class ChannelStripComponent(ChannelStripComponentBase):
    empty_color = b'Mixer.EmptyTrack'
    track_color_control = SendValueControl()
    static_color_control = SendValueControl()

    def __init__(self, *a, **k):
        super(ChannelStripComponent, self).__init__(*a, **k)
        self._static_color_value = 0
        self._track_color_value = 0

    def set_static_color_value(self, value):
        if value is not None:
            self._static_color_value = value
            self._update_static_color_control()
        return

    def set_track(self, track):
        super(ChannelStripComponent, self).set_track(track)
        self.__on_track_color_changed.subject = track if liveobj_valid(track) else None
        self.__on_track_color_changed()
        self._update_static_color_control()
        return

    @listens(b'color')
    def __on_track_color_changed(self):
        self._track_color_value = get_midi_color_value_for_track(self._track)
        self._track_color_changed()

    def _track_color_changed(self):
        self.track_color_control.value = self._track_color_value

    def _update_static_color_control(self):
        self.static_color_control.value = self._static_color_value if liveobj_valid(self._track) else 0
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/novation/channel_strip.pyc
