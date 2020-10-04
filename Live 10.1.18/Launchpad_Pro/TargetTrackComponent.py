# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad_Pro\TargetTrackComponent.py
# Compiled at: 2020-07-14 15:33:45
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.SubjectSlot import Subject, subject_slot, subject_slot_group
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent

class TargetTrackComponent(ControlSurfaceComponent, Subject):
    """
    TargetTrackComponent handles determining the track to target for
    note mode-related functionality and notifying listeners.
    """
    __subject_events__ = ('target_track', )
    _target_track = None
    _armed_track_stack = []

    def __init__(self, *a, **k):
        super(TargetTrackComponent, self).__init__(*a, **k)
        self._on_tracks_changed.subject = self.song()
        self._on_tracks_changed()

    @property
    def target_track(self):
        return self._target_track

    def on_selected_track_changed(self):
        if not self._armed_track_stack:
            self._set_target_track()

    @subject_slot(b'tracks')
    def _on_tracks_changed(self):
        tracks = filter(lambda t: t.can_be_armed and t.has_midi_input, self.song().tracks)
        self._on_arm_changed.replace_subjects(tracks)
        self._on_frozen_state_changed.replace_subjects(tracks)
        self._refresh_armed_track_stack(tracks)

    @subject_slot_group(b'arm')
    def _on_arm_changed(self, track):
        if track in self._armed_track_stack:
            self._armed_track_stack.remove(track)
        if track.arm:
            self._armed_track_stack.append(track)
            self._set_target_track(track)
        else:
            self._set_target_track()

    @subject_slot_group(b'is_frozen')
    def _on_frozen_state_changed(self, track):
        if track in self._armed_track_stack:
            self._armed_track_stack.remove(track)
        if track == self._target_track:
            self._set_target_track()

    def _set_target_track(self, target=None):
        new_target = self._target_track
        if target is None:
            if self._armed_track_stack:
                new_target = self._armed_track_stack[(-1)]
            else:
                new_target = self.song().view.selected_track
        else:
            new_target = target
        if self._target_track != new_target:
            self._target_track = new_target
        self.notify_target_track()
        return

    def _refresh_armed_track_stack(self, all_tracks):
        for track in self._armed_track_stack:
            if track not in all_tracks:
                self._armed_track_stack.remove(track)

        for track in all_tracks:
            if track.arm and track not in self._armed_track_stack:
                self._armed_track_stack.append(track)

        self._set_target_track()
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/Launchpad_Pro/TargetTrackComponent.pyc
