# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Axiom_DirectLink\ShiftableSessionComponent.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.SessionComponent import SessionComponent
from _Framework.ButtonElement import ButtonElement

class ShiftableSessionComponent(SessionComponent):
    """ Special session class that reassigns controls based on a shift button """

    def __init__(self, num_tracks, num_scenes):
        self._shift_button = None
        self._clip_slot_buttons = None
        SessionComponent.__init__(self, num_tracks, num_scenes)
        return

    def disconnect(self):
        SessionComponent.disconnect(self)
        if self._shift_button != None:
            self._shift_button.remove_value_listener(self._shift_value)
            self._shift_button = None
        self._clip_slot_buttons = None
        return

    def set_shift_button(self, shift_button):
        assert shift_button == None or shift_button.is_momentary()
        if self._shift_button != None:
            self._shift_button.remove_value_listener(self._shift_value)
        self._shift_button = shift_button
        if self._shift_button != None:
            self._shift_button.add_value_listener(self._shift_value)
        return

    def set_clip_slot_buttons(self, buttons):
        assert buttons == None or isinstance(buttons, tuple) and len(buttons) == self._num_tracks
        self._clip_slot_buttons = buttons
        self._shift_value(0)
        return

    def on_selected_track_changed(self):
        SessionComponent.on_selected_track_changed(self)
        selected_track = self.song().view.selected_track
        tracks = self.tracks_to_use()
        if selected_track in tracks:
            track_index = list(tracks).index(selected_track)
            new_offset = track_index - track_index % self._num_tracks
            assert new_offset / self._num_tracks == int(new_offset / self._num_tracks)
            self.set_offsets(new_offset, self.scene_offset())

    def _shift_value(self, value):
        assert self._shift_button != None
        assert value in range(128)
        for index in range(self._num_tracks):
            slot = self.selected_scene().clip_slot(index)
            if value == 0 or self._clip_slot_buttons == None:
                slot.set_launch_button(None)
            else:
                slot.set_launch_button(self._clip_slot_buttons[index])

        return

    def _bank_right_value(self, value):
        if not value in range(128):
            raise AssertionError
            assert self._bank_right_button != None
            if self.is_enabled() and (value is not 0 or not self._bank_right_button.is_momentary()):
                self.set_offsets(self._track_offset + self._num_tracks, self.scene_offset())
        return

    def _bank_left_value(self, value):
        if not isinstance(value, int):
            raise AssertionError
            assert self._bank_left_button != None
            if self.is_enabled() and (value is not 0 or not self._bank_left_button.is_momentary()):
                self.set_offsets(max(0, self._track_offset - self._num_tracks), self.scene_offset())
        return
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Axiom_DirectLink/ShiftableSessionComponent.pyc
