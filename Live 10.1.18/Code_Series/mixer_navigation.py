# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Code_Series\mixer_navigation.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.components import SessionNavigationComponent, SessionRingScroller

class WrappingSessionRingTrackPager(SessionRingScroller):

    def can_scroll_up(self):
        return True

    def can_scroll_down(self):
        return True

    def do_scroll_up(self):
        width = self._session_ring.num_tracks
        track_offset = self._session_ring.track_offset
        new_track_offset = track_offset - width
        if new_track_offset < 0:
            new_track_offset = (len(self._session_ring.tracks_to_use()) - 1) / width * width
        self._session_ring.set_offsets(new_track_offset, self._session_ring.scene_offset)

    def do_scroll_down(self):
        new_track_offset = self._session_ring.track_offset + self._session_ring.num_tracks
        if new_track_offset >= len(self._session_ring.tracks_to_use()):
            new_track_offset = 0
        self._session_ring.set_offsets(new_track_offset, self._session_ring.scene_offset)


class MixerNavigationComponent(SessionNavigationComponent):
    track_pager_type = WrappingSessionRingTrackPager
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Code_Series/mixer_navigation.pyc
