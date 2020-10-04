# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\SL_MkIII\session.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import find_if
from ableton.v2.control_surface.components import SessionComponent as SessionComponentBase

class SessionComponent(SessionComponentBase):

    def _update_stop_clips_led(self, index):
        super(SessionComponent, self)._update_stop_clips_led(index)
        self._update_stop_all_clips_button()

    def _update_stop_all_clips_button(self):
        button = self._stop_all_button
        if button:
            value_to_send = self._stop_clip_disabled_value
            tracks = self.song.tracks
            if find_if(lambda x: x.playing_slot_index >= 0 and x.fired_slot_index != -2, tracks):
                value_to_send = self._stop_clip_value
            elif find_if(lambda x: x.fired_slot_index == -2, tracks):
                value_to_send = self._stop_clip_triggered_value
            button.set_light(value_to_send)
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/SL_MkIII/session.pyc
