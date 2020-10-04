# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\novation\instrument_control.py
# Compiled at: 2020-07-14 15:33:46
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import listens
from ableton.v2.control_surface import PercussionInstrumentFinder
from ableton.v2.control_surface.components import TargetTrackComponent
from .colors import Rgb
from .util import is_song_recording

def track_can_record(track):
    return track.can_be_armed and (track.arm or track.implicit_arm)


class InstrumentControlMixin(object):
    target_track_class = TargetTrackComponent

    def _create_components(self):
        super(InstrumentControlMixin, self)._create_components()
        self._target_track = self.target_track_class(name=b'Target_Track')
        self._drum_group_finder = self.register_disconnectable(PercussionInstrumentFinder(device_parent=self._target_track.target_track))
        self.__on_drum_group_changed.subject = self._drum_group_finder
        self.__on_target_track_changed.subject = self._target_track
        self.__on_session_record_changed.subject = self.song
        self.__on_record_mode_changed.subject = self.song
        self._set_feedback_velocity()

    @listens(b'target_track')
    def __on_target_track_changed(self):
        self._target_track_changed()

    def _target_track_changed(self):
        track = self._target_track.target_track
        self._drum_group_finder.device_parent = track
        self._drum_group.set_parent_track(track)
        self.__on_target_track_arm_changed.subject = track
        self.__on_target_track_implicit_arm_changed.subject = track
        self._update_controlled_track()

    @listens(b'instrument')
    def __on_drum_group_changed(self):
        self._drum_group_changed()

    def _drum_group_changed(self):
        raise NotImplementedError

    @listens(b'session_record')
    def __on_session_record_changed(self):
        self._set_feedback_velocity()

    @listens(b'record_mode')
    def __on_record_mode_changed(self):
        self._set_feedback_velocity()

    @listens(b'arm')
    def __on_target_track_arm_changed(self):
        self._set_feedback_velocity()

    @listens(b'implicit_arm')
    def __on_target_track_implicit_arm_changed(self):
        self._set_feedback_velocity()

    def _update_controlled_track(self):
        if self._is_instrument_mode():
            self.set_controlled_track(self._target_track.target_track)
        else:
            self.release_controlled_track()

    def _is_instrument_mode(self):
        raise NotImplementedError

    def _set_feedback_velocity(self):
        track = self._target_track.target_track
        if is_song_recording(self.song) and track_can_record(track):
            feedback_velocity = Rgb.RED.midi_value
        else:
            feedback_velocity = Rgb.GREEN.midi_value
        self._c_instance.set_feedback_velocity(int(feedback_velocity))
        self._feedback_velocity_changed(feedback_velocity)

    def _feedback_velocity_changed(self, feedback_velocity):
        pass
# okay decompiling /home/deniz/data/projects/midiremote/Live 10.1.18/novation/instrument_control.pyc
