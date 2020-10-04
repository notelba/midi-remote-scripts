# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\iRig_Keys_IO\mixer.py
# Compiled at: 2020-05-05 13:23:28
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import forward_property, liveobj_valid
from ableton.v2.control_surface.components import MixerComponent as MixerComponentBase
from ableton.v2.control_surface.control import ButtonControl
from .scroll import ScrollComponent

class MixerComponent(MixerComponentBase):
    track_scroll_encoder = forward_property(b'_track_scrolling')(b'scroll_encoder')
    selected_track_arm_button = ButtonControl()

    def __init__(self, *a, **k):
        super(MixerComponent, self).__init__(*a, **k)
        self._track_scrolling = ScrollComponent(parent=self)
        self._track_scrolling.can_scroll_up = self._can_select_prev_track
        self._track_scrolling.can_scroll_down = self._can_select_next_track
        self._track_scrolling.scroll_up = self._select_prev_track
        self._track_scrolling.scroll_down = self._select_next_track

    @selected_track_arm_button.pressed
    def selected_track_arm_button(self, _):
        selected_track = self.song.view.selected_track
        if liveobj_valid(selected_track) and selected_track.can_be_armed:
            new_value = not selected_track.arm
            for track in self.song.tracks:
                if track.can_be_armed:
                    if track == selected_track or track.is_part_of_selection and selected_track.is_part_of_selection:
                        track.arm = new_value
                    elif self.song.exclusive_arm and track.arm:
                        track.arm = False

    def _can_select_prev_track(self):
        return self.song.view.selected_track != self._provider.tracks_to_use()[0]

    def _can_select_next_track(self):
        return self.song.view.selected_track != self._provider.tracks_to_use()[(-1)]

    def _select_prev_track(self):
        selected_track = self.song.view.selected_track
        tracks = self._provider.tracks_to_use()
        assert selected_track in tracks
        index = list(tracks).index(selected_track)
        self.song.view.selected_track = tracks[(index - 1)]

    def _select_next_track(self):
        selected_track = self.song.view.selected_track
        tracks = self._provider.tracks_to_use()
        assert selected_track in tracks
        index = list(tracks).index(selected_track)
        self.song.view.selected_track = tracks[(index + 1)]
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/iRig_Keys_IO/mixer.pyc
